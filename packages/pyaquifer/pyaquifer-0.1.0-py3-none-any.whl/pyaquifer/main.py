from typing import Any
import pandas as pd  # only needed for type hints when engine is pandas

from .config import JobConfig, Engine
from .connectors.pandas import PandasConnector
from .connectors.polars import PolarsConnector
from .connectors.duckdb import DuckDBConnector


class Aquifer:
    """
    Core class for the pyaquifer pipeline.
    Dispatches load/transform/write to the chosen engine connector.
    """

    def __init__(self, config: JobConfig):
        self.config = config

        if config.engine is Engine.PANDAS:
            self.connector = PandasConnector(
                region_name       = config.region_name,
                aws_profile_name  = config.aws_profile_name,
                input_bucket_arn  = config.input_bucket_arn,
                glue_database     = config.glue_database,
                output_bucket_arn = config.resolved_output_bucket_arn,
            )
        elif config.engine is Engine.POLARS:
            self.connector = PolarsConnector(
                region_name       = config.region_name,
                aws_profile_name  = config.aws_profile_name,
                input_bucket_arn  = config.input_bucket_arn,
                glue_database     = config.glue_database,
                output_bucket_arn = config.resolved_output_bucket_arn,
            )
        elif config.engine is Engine.DUCKDB:
            self.connector = DuckDBConnector(
                region_name       = config.region_name,
                aws_profile_name  = config.aws_profile_name,
                input_bucket_arn  = config.input_bucket_arn,
                glue_database     = config.glue_database,
                output_bucket_arn = config.resolved_output_bucket_arn,
            )
        else:
            raise ValueError(f"Unsupported engine: {config.engine}")

    def load(self, table_name: str) -> Any:
        """
        Load one table from the input namespace into the selected engine's DataFrame.
        """
        return self.connector.load_table(self.config.iceberg_namespace, table_name)

    def transform(self, df: Any, **kwargs: Any) -> Any:
        """
        Apply user-defined transformations to the DataFrame.
        Default implementation is a no-op.
        """
        return df

    def write(self, table_name: str, df: Any) -> None:
        """
        Persist a transformed DataFrame back to Iceberg in the output namespace.
        """
        self.connector.write_table(
            self.config.output_namespace,
            table_name,
            df,
        )
