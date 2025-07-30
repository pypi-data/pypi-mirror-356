import boto3
from botocore.exceptions import ClientError
from typing import Optional, List, Dict

class GlueConnector:
    """
    Wraps AWS Glue Data Catalog calls, optionally targeting a custom CatalogId
    (e.g. the S3‐Tables federated catalog) instead of the account default.
    """

    def __init__(self, glue_database: str, session: boto3.Session, catalog_id: Optional[str] = None):
        self.glue_database = glue_database
        self.glue_client = session.client("glue")
        self.catalog_id = catalog_id

    def fetch_schema_for_table(self, table_name: str) -> Dict[str, str]:
        """
        Returns a mapping of column_name → sql_type (both lowercase)
        for the given table, using the configured CatalogId if provided.
        """
        print(f"[GlueConnector] Fetching schema for {table_name}...")
        params = {
            "DatabaseName": self.glue_database,
            "Name":          table_name,
        }
        if self.catalog_id:
            params["CatalogId"] = self.catalog_id

        try:
            resp = self.glue_client.get_table(**params)
        except ClientError as e:
            print(f"[GlueConnector] Error fetching schema for {table_name}: {e}")
            raise

        cols = resp["Table"]["StorageDescriptor"]["Columns"]
        return {col["Name"].lower(): col["Type"].lower() for col in cols}

    def list_partitions(self, table_name: str) -> List[Dict]:
        """
        Fetch partition keys and values for a table, using the configured CatalogId if provided.
        """
        paginator = self.glue_client.get_paginator("get_partitions")
        paginate_kwargs = {
            "DatabaseName": self.glue_database,
            "TableName":    table_name,
        }
        if self.catalog_id:
            paginate_kwargs["CatalogId"] = self.catalog_id

        try:
            pages = paginator.paginate(**paginate_kwargs)
        except ClientError as e:
            print(f"[GlueConnector] Error listing partitions for {table_name}: {e}")
            raise

        parts: List[Dict] = []
        for page in pages:
            parts.extend(page.get("Partitions", []))
        return parts
