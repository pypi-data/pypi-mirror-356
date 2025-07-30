import base64
from typing import Dict, Optional, Union

import duckdb
import pandas as pd
import boto3
import pyarrow as pa

from pyiceberg.catalog import Catalog
from pyiceberg.schema import Schema, NestedField
from pyiceberg.types import (
    LongType,
    DoubleType,
    TimestampType,
    StringType,
    BooleanType,
    DateType,
    DecimalType,
)

from .glue import GlueConnector
from .iceberg import get_iceberg_catalog


class DuckDBConnector:
    """
    Connector for DuckDB using Iceberg REST + Glue metadata.
    Supports loading and writing tables in S3 Tables Iceberg catalog via Arrow.
    """

    def __init__(
        self,
        region_name: str,
        aws_profile_name: str,
        input_bucket_arn: str,
        glue_database: str,
        output_bucket_arn: Optional[str] = None,
    ):
        # AWS session & Glue
        self.session = boto3.Session(
            profile_name=aws_profile_name,
            region_name=region_name,
        )
        self.glue = GlueConnector(glue_database, self.session)

        # Buckets
        self.input_bucket_arn = input_bucket_arn
        self.output_bucket_arn = output_bucket_arn or input_bucket_arn

        # Iceberg REST catalog
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

        self.catalog: Catalog = get_iceberg_catalog(props)
        self.s3tables = self.session.client("s3tables", region_name=region_name)

        # In‐memory DuckDB connection
        self.con = duckdb.connect()

    def create_namespace(self, namespace: str) -> None:
        try:
            self.s3tables.create_namespace(
                tableBucketARN=self.output_bucket_arn,
                namespace=[namespace],
            )
            print(f"[DuckDBConnector] Namespace '{namespace}' created in {self.output_bucket_arn}")
        except self.s3tables.exceptions.ConflictException:
            print(f"[DuckDBConnector] Namespace '{namespace}' already exists")

    def load_table(self, namespace: str, table_name: str) -> duckdb.DuckDBPyRelation:
        ident = f"{namespace}.{table_name}"
        print(f"[DuckDBConnector] Loading {ident} via Iceberg REST…")

        # 1) read arrow
        scan = self.catalog.load_table(ident).scan()
        arrow_tbl: pa.Table = scan.to_arrow()
        arrow_tbl = arrow_tbl.rename_columns([c.lower() for c in arrow_tbl.column_names])

        # 2) register as a DuckDB view (new API: Connection.register)
        view = f"{table_name.lower()}_arrow"
        # DuckDBPyConnection.register takes (name, Arrow Table or Pandas DF)
        self.con.register(view, arrow_tbl)
        print(f"[DuckDBConnector] Registered Arrow table as view '{view}'")

        # 3) pull it back as a relation
        rel = self.con.table(view)

        # 4) (optional) encode binary columns via SQL UDF or post‐processing:
        #    Skipping here for brevity; you could .arrow() + base64.encode if needed.

        return rel

    def write_table(
        self,
        namespace: str,
        table_name: str,
        data: Union[duckdb.DuckDBPyRelation, pa.Table, pd.DataFrame],
    ) -> None:
        """
        Persist a DuckDB relation, Arrow table, or Pandas DataFrame
        back to Iceberg under <namespace>.<table_name>.
        """
        # 1) sanitize & namespace
        namespace = namespace.lower()
        table_name = table_name.lower()
        ident = f"{namespace}.{table_name}"
        print(f"[DuckDBConnector] Writing {ident} to Iceberg…")
        self.create_namespace(namespace)

        # 2) normalize to PyArrow Table
        if hasattr(data, "arrow"):
            arrow_tbl = data.arrow()
        elif isinstance(data, pa.Table):
            arrow_tbl = data
        else:
            arrow_tbl = pa.Table.from_pandas(data, preserve_index=False)

        # 3) encode any binary columns to Base64 strings
        import base64
        bin_cols = [
            (i, f.name)
            for i, f in enumerate(arrow_tbl.schema)
            if pa.types.is_binary(f.type) or pa.types.is_large_binary(f.type)
        ]
        for i, name in bin_cols:
            arr = arrow_tbl.column(name).to_pylist()
            b64 = pa.array(
                [base64.b64encode(v).decode("ascii") if v is not None else None for v in arr],
                pa.string()
            )
            arrow_tbl = arrow_tbl.set_column(i, name, b64)

        # 4) cast decimal columns to float64
        for i, f in enumerate(arrow_tbl.schema):
            if pa.types.is_decimal(f.type):
                arrow_tbl = arrow_tbl.set_column(
                    i,
                    f.name,
                    arrow_tbl.column(f.name).cast(pa.float64())
                )

        # 5) build Iceberg schema, mapping decimals → DoubleType
        fields = []
        for idx, field in enumerate(arrow_tbl.schema, start=1):
            t = field.type
            if pa.types.is_integer(t):
                ice = LongType()
            elif pa.types.is_floating(t):
                ice = DoubleType()
            elif pa.types.is_timestamp(t):
                ice = TimestampType()
            elif pa.types.is_boolean(t):
                ice = BooleanType()
            elif pa.types.is_date(t):
                ice = DateType()
            else:
                ice = StringType()
            fields.append(NestedField(idx, field.name, ice, required=False))
        schema = Schema(*fields)

        # 6) drop & recreate table metadata
        try:
            self.catalog.drop_table(ident)
            print(f"[DuckDBConnector] Dropped existing table {ident}")
        except Exception:
            pass
        table = self.catalog.create_table(ident, schema)
        print(f"[DuckDBConnector] Created Iceberg table {ident}")

        # 7) ensure timestamps are µs‐precision
        for i, f in enumerate(arrow_tbl.schema):
            if pa.types.is_timestamp(f.type):
                arrow_tbl = arrow_tbl.set_column(
                    i,
                    f.name,
                    arrow_tbl.column(f.name).cast(pa.timestamp("us"))
                )

        # 8) overwrite
        table.overwrite(arrow_tbl)
        print(f"[DuckDBConnector] Successfully wrote data to {ident}")
