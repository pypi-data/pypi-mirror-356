import base64
from typing import Dict, Optional

import pandas as pd
import boto3
from pyiceberg.catalog import Catalog
from pyiceberg.schema import Schema, NestedField
from pyiceberg.types import (
    LongType,
    DoubleType,
    TimestampType,
    StringType,
    BooleanType,
    DateType,
)
import pyarrow as pa

from .glue import GlueConnector
from .iceberg import get_iceberg_catalog


class PandasConnector:
    """
    Connector for pandas DataFrames using Iceberg REST + Glue metadata.
    Supports loading and writing tables in S3 Tables Iceberg catalog.
    """

    def __init__(
        self,
        region_name: str,
        aws_profile_name: str,
        input_bucket_arn: str,
        glue_database: str,
        glue_catalog_id: Optional[str] = None,   # ← new parameter
        output_bucket_arn: Optional[str] = None,
    ):
        # 1) AWS session & Glue
        self.session = boto3.Session(
            profile_name=aws_profile_name,
            region_name=region_name,
        )
        # Pass the explicit CatalogId into GlueConnector
        self.glue = GlueConnector(
            glue_database,
            self.session,
            catalog_id=glue_catalog_id,
        )

        # 2) Store input and output bucket ARNs
        self.input_bucket_arn = input_bucket_arn
        self.output_bucket_arn = output_bucket_arn or input_bucket_arn

        # 3) Iceberg REST catalog config (reads always from input bucket)
        creds = self.session.get_credentials().get_frozen_credentials()
        props = {
            "type":                "rest",
            "uri":                 f"https://s3tables.{region_name}.amazonaws.com/iceberg",
            "warehouse":           input_bucket_arn,
            "rest.sigv4-enabled":  "true",
            "rest.signing-name":   "s3tables",
            "rest.signing-region": region_name,
            "client.access-key-id":     creds.access_key,
            "client.secret-access-key": creds.secret_key,
            "client.region":            region_name,
        }
        if creds.token:
            props["client.session-token"] = creds.token

        # Instantiate Iceberg catalog
        self.catalog: Catalog = get_iceberg_catalog(props)

        # 4) S3Tables namespace client for output bucket
        self.s3tables = self.session.client("s3tables", region_name=region_name)

    def create_namespace(self, namespace: str) -> None:
        """
        Create the namespace in the output S3 Tables bucket if it does not already exist.
        """
        try:
            self.s3tables.create_namespace(
                tableBucketARN=self.output_bucket_arn,
                namespace=[namespace]
            )
            print(f"[PandasConnector] Namespace '{namespace}' created in bucket {self.output_bucket_arn}.")
        except self.s3tables.exceptions.ConflictException:
            print(f"[PandasConnector] Namespace '{namespace}' already exists in bucket {self.output_bucket_arn}.")

    def load_table(self, namespace: str, table_name: str) -> pd.DataFrame:
        ident = f"{namespace}.{table_name}"
        print(f"[PandasConnector] Loading {ident} via Iceberg REST…")
        scan = self.catalog.load_table(ident).scan()
        df = scan.to_pandas()
        df.columns = df.columns.str.lower()

        # Glue schema mapping
        glue_schema: Dict[str, str] = self.glue.fetch_schema_for_table(table_name)

        # Encode binary columns
        binary_cols = [c for c, t in glue_schema.items() if t == "binary"]
        if binary_cols:
            print(f"[PandasConnector] Encoding binary cols: {binary_cols}")
            for col in binary_cols:
                df[col] = df[col].apply(
                    lambda x: base64.b64encode(x).decode("ascii")
                    if isinstance(x, (bytes, bytearray))
                    else None
                )

        # Dtype mapping (dates/timestamps as strings to avoid timezone and bounds issues)
        dtype_map: Dict[str, str] = {}
        for col, sql_type in glue_schema.items():
            if sql_type in ("date", "timestamp"):
                dtype_map[col] = "string"
            elif "bigint" in sql_type or sql_type == "int":
                dtype_map[col] = "Int64"
            elif any(k in sql_type for k in ("decimal", "double", "float")):
                dtype_map[col] = "float64"
            else:
                dtype_map[col] = "string"

        print(f"[PandasConnector] Casting columns to pandas dtypes…")
        df = df.astype(dtype_map)
        print(f"[PandasConnector] Loaded {ident}: {df.shape}")
        return df

    def write_table(self, namespace: str, table_name: str, df: pd.DataFrame) -> None:
        # sanitize namespace & table name to lowercase
        namespace = namespace.lower()
        sanitized_table = table_name.lower()

        # lowercase all column names for Athena compatibility
        df = df.copy()
        df.columns = df.columns.str.lower()

        ident = f"{namespace}.{sanitized_table}"
        print(f"[PandasConnector] Writing {ident} to Iceberg…")

        # Ensure namespace exists in output bucket
        self.create_namespace(namespace)

        # Build Iceberg schema from DataFrame dtypes
        fields = []
        for idx, (col, dtype) in enumerate(df.dtypes.items(), start=1):
            if pd.api.types.is_integer_dtype(dtype):
                ice_type = LongType()
            elif pd.api.types.is_float_dtype(dtype):
                ice_type = DoubleType()
            elif pd.api.types.is_datetime64_any_dtype(dtype):
                ice_type = TimestampType()
            elif pd.api.types.is_bool_dtype(dtype):
                ice_type = BooleanType()
            elif pd.api.types.is_object_dtype(dtype) and pa.types.is_date(pa.array(df[col]).type):
                ice_type = DateType()
            else:
                ice_type = StringType()
            fields.append(NestedField(idx, col, ice_type, required=False))
        schema = Schema(*fields)

        # Drop existing table in output catalog if present
        try:
            self.catalog.drop_table(ident)
            print(f"[PandasConnector] Dropped existing table {ident}.")
        except Exception:
            pass

        # Create new table in output catalog
        table = self.catalog.create_table(ident, schema)
        print(f"[PandasConnector] Created Iceberg table {ident}.")

        # Convert DataFrame to PyArrow Table and cast timestamps
        arrow_table = pa.Table.from_pandas(df, preserve_index=False)
        for i, field in enumerate(arrow_table.schema):
            if pa.types.is_timestamp(field.type):
                col = arrow_table.column(field.name).cast(pa.timestamp('us'))
                arrow_table = arrow_table.set_column(i, field.name, col)

        # Overwrite data in output catalog
        table.overwrite(arrow_table)
        print(f"[PandasConnector] Successfully wrote data to {ident}.")

        
