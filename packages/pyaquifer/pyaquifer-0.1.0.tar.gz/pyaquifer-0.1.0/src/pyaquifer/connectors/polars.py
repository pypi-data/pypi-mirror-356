import base64
from typing import Dict, Optional

import polars as pl
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


class PolarsConnector:
    """
    Connector for Polars DataFrames using Iceberg REST + Glue metadata.
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
        # Pass CatalogId through to GlueConnector
        self.glue = GlueConnector(
            glue_database,
            self.session,
            catalog_id=glue_catalog_id,
        )

        # 2) Buckets
        self.input_bucket_arn = input_bucket_arn
        self.output_bucket_arn = output_bucket_arn or input_bucket_arn

        # 3) Iceberg REST catalog config for reads
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

        # 4) S3Tables client for namespace operations
        self.s3tables = self.session.client("s3tables", region_name=region_name)
    def create_namespace(self, namespace: str) -> None:
        try:
            self.s3tables.create_namespace(
                tableBucketARN=self.output_bucket_arn, namespace=[namespace]
            )
            print(f"[PolarsConnector] Namespace '{namespace}' created.")
        except self.s3tables.exceptions.ConflictException:
            print(f"[PolarsConnector] Namespace '{namespace}' already exists.")

    def load_table(self, namespace: str, table_name: str) -> pl.DataFrame:
        ident = f"{namespace}.{table_name}"
        print(f"[PolarsConnector] Loading {ident} via Iceberg REST…")

        # 1) Pull from Iceberg → Arrow → eager Polars DF
        scan = self.catalog.load_table(ident).scan()
        arrow_tbl = scan.to_arrow()
        df = pl.from_arrow(arrow_tbl)

        # lowercase all column names
        df = df.rename({c: c.lower() for c in df.columns})

        # 2) Fetch Glue schema
        glue_schema: Dict[str, str] = self.glue.fetch_schema_for_table(table_name)

        # 3) Encode binary columns
        for col, t in glue_schema.items():
            if t == "binary" and col in df.columns:
                df = df.with_columns([
                    pl.col(col)
                      .map_elements(
                          lambda x: base64.b64encode(x).decode("ascii") if x is not None else None,
                          return_dtype=pl.Utf8
                      )
                      .alias(col)
                ])

        # 4) Cast according to Glue types
        for col, t in glue_schema.items():
            if col not in df.columns:
                continue

            if t in ("date", "timestamp"):
                dtype = pl.Utf8
            elif "int" in t:
                dtype = pl.Int64
            elif any(k in t for k in ("decimal", "double", "float")):
                dtype = pl.Float64
            else:
                dtype = pl.Utf8

            df = df.with_columns([
                pl.col(col).cast(dtype).alias(col)
            ])

        print(f"[PolarsConnector] Loaded {ident}: {df.shape}")
        return df

    def write_table(self, namespace: str, table_name: str, df: pl.DataFrame) -> None:
        # sanitize namespace & table name to lowercase
        namespace = namespace.lower()
        tbl       = table_name.lower()

        # lowercase all column names
        df = df.lazy().with_columns(
            [pl.col(c).alias(c.lower()) for c in df.columns]
        ).collect()

        ident = f"{namespace}.{tbl}"
        print(f"[PolarsConnector] Writing {ident} to Iceberg…")

        # ensure namespace exists
        self.create_namespace(namespace)

        # build Iceberg schema from Arrow
        arrow_tbl = df.to_arrow()
        fields = []
        for idx, field in enumerate(arrow_tbl.schema, start=1):
            pa_type = field.type
            if pa.types.is_integer(pa_type):
                ice_type = LongType()
            elif pa.types.is_floating(pa_type):
                ice_type = DoubleType()
            elif pa.types.is_timestamp(pa_type):
                ice_type = TimestampType()
            elif pa.types.is_boolean(pa_type):
                ice_type = BooleanType()
            elif pa.types.is_date(pa_type):
                ice_type = DateType()
            else:
                ice_type = StringType()
            fields.append(NestedField(idx, field.name, ice_type, required=False))
        schema = Schema(*fields)

        # drop & recreate table metadata
        try:
            self.catalog.drop_table(ident)
            print(f"[PolarsConnector] Dropped existing {ident}.")
        except Exception:
            pass

        table = self.catalog.create_table(ident, schema)
        print(f"[PolarsConnector] Created Iceberg table {ident}.")

        # cast timestamp cols to microseconds
        for i, field in enumerate(arrow_tbl.schema):
            if pa.types.is_timestamp(field.type):
                col = arrow_tbl.column(field.name).cast(pa.timestamp("us"))
                arrow_tbl = arrow_tbl.set_column(i, field.name, col)

        # overwrite with the new data
        table.overwrite(arrow_tbl)
        print(f"[PolarsConnector] Successfully wrote data to {ident}.")