from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
import re

class Engine(str, Enum):
    PANDAS = "pandas"
    POLARS = "polars"
    DUCKDB = "duckdb"

@dataclass
class JobConfig:
    # ─── Required (no defaults) ────────────────────────────────────────────────
    region_name: str                    # AWS region, e.g. "eu-north-1"
    input_bucket_arn: str               # S3 Tables bucket ARN to read from
    iceberg_namespace: str              # Iceberg namespace (on S3 Tables)
    glue_database: str                  # AWS Glue database name
    output_namespace: str               # Iceberg namespace for writes

    # ─── Optional (with defaults) ─────────────────────────────────────────────
    glue_catalog_id: Optional[str] = None   # << new
    aws_profile_name: str = field(
        default="default",
        metadata={"help": "AWS CLI profile name"}
    )
    output_bucket_arn: Optional[str] = field(
        default=None,
        metadata={"help": (
            "S3 Tables bucket ARN to write to; "
            "if None, falls back to input_bucket_arn"
        )}
    )
    tables_to_load: List[str] = field(
        default_factory=list,
        metadata={"help": "List of tables to load from the input namespace"}
    )
    engine: Engine = field(
        default=Engine.PANDAS,
        metadata={"help": "Compute engine to use (pandas, polars, duckdb)"}
    )

    def __post_init__(self):
        # Validate the bucket ARNs (both old and new style)
        patterns = [
            r"^arn:aws:s3:[^:]+:\d{12}:table/[^/]+$",
            r"^arn:aws:s3tables:[^:]+:\d{12}:bucket/[^/]+$",
        ]
        for attr in ("input_bucket_arn", "output_bucket_arn"):
            val = getattr(self, attr)
            if val and not any(re.match(p, val) for p in patterns):
                raise ValueError(f"{attr} is not a valid S3 Tables ARN: {val}")

    @property
    def resolved_output_bucket_arn(self) -> str:
        """Returns the bucket ARN to write to (fallback to input_bucket_arn)."""
        return self.output_bucket_arn or self.input_bucket_arn
