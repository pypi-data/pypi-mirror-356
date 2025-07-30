from pyiceberg.catalog import load_catalog, Catalog

def get_iceberg_catalog(config: dict) -> Catalog:
    """Initializes and returns the PyIceberg REST Catalog."""
    print("[IcebergConnector] Authenticating to S3 Tables Iceberg catalog...")
    catalog = load_catalog("wwi_s3tables", **config)
    print("✅ Connected to Iceberg catalog.")
    return catalog