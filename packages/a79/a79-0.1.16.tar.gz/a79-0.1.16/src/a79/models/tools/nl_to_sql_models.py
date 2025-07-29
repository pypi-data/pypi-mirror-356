import typing as t

from pydantic import BaseModel, Field, field_validator

from common_py.sql.model import SQADatabaseConfig
from external.a79.src.a79.models.tools import ToolOutput


class SourceSelectionInput(BaseModel):
    """Input model for source/table selection"""

    query: str = Field(
        description="Natural language query to analyze for table selection"
    )
    num_tables: int = Field(
        default=3, ge=1, description="Number of most relevant tables to return"
    )
    database_config: SQADatabaseConfig = Field(
        description="Database configuration for connecting to the target database"
    )

    @classmethod
    @field_validator("database_config", mode="before")
    def validate_database_config(cls, v: t.Any) -> SQADatabaseConfig:
        """Transform dict to SQADatabaseConfig and validate configuration"""
        # If it's already an SQADatabaseConfig, use it directly
        if isinstance(v, SQADatabaseConfig):
            config = v
        # If it's a dict, transform to SQADatabaseConfig
        elif isinstance(v, dict):
            try:
                config = SQADatabaseConfig(**v)
            except Exception as e:
                raise ValueError(f"Invalid database configuration: {str(e)}")
        else:
            raise ValueError(
                "database_config must be a dictionary or SQADatabaseConfig object"
            )

        # Basic validation checks
        if not config.database:
            raise ValueError("Database name is required")

        if config.dialect.value not in [
            "postgresql",
            "mysql",
            "sqlite",
            "trino",
            "mssql",
            "oracle",
            "snowflake",
        ]:
            raise ValueError(f"Unsupported database dialect: {config.dialect.value}")

        # For non-SQLite databases, validate credentials
        if config.dialect.value != "sqlite":
            if not config.credentials:
                raise ValueError(
                    "Database credentials are required for non-SQLite databases"
                )
            if not config.credentials.host:
                raise ValueError("Database host is required")
            if not config.credentials.username:
                raise ValueError("Database username is required")
            if not config.credentials.password:
                raise ValueError("Database password is required")

        return config


class SourceSelectionOutput(ToolOutput):
    """Output model for source/table selection"""

    relevant_tables: list[dict[str, t.Any]] = Field(
        description="List of tables selected with relevance scores and reasoning"
    )
    explanation: str = Field(
        description="Overall explanation of the table selection process"
    )
    table_definitions: list[dict[str, t.Any]] = Field(
        description="Detailed definitions of the selected tables"
    )


class NLToSQLInput(BaseModel):
    """Input model for NL-to-SQL conversion"""

    query: str = Field(description="Natural language query to convert to SQL")
    num_tables_to_filter_for_sql_generation: int = Field(
        default=3,
        ge=1,
        description="Number of most relevant tables to select for SQL generation",
    )
    sample_rows: t.Optional[dict[str, list[dict[str, t.Any]]]] = Field(
        default=None,
        description="Optional sample data to provide context for SQL generation",
    )
    database_config: SQADatabaseConfig = Field(
        description="Database configuration for connecting to the target database"
    )

    @classmethod
    @field_validator("database_config", mode="before")
    def validate_database_config(cls, v: t.Any) -> SQADatabaseConfig:
        """Transform dict to SQADatabaseConfig and validate configuration"""
        # If it's already an SQADatabaseConfig, use it directly
        if isinstance(v, SQADatabaseConfig):
            config = v
        # If it's a dict, transform to SQADatabaseConfig
        elif isinstance(v, dict):
            try:
                config = SQADatabaseConfig(**v)
            except Exception as e:
                raise ValueError(f"Invalid database configuration: {str(e)}")
        else:
            raise ValueError(
                "database_config must be a dictionary or SQADatabaseConfig object"
            )

        # Basic validation checks
        if not config.database:
            raise ValueError("Database name is required")

        if config.dialect.value not in [
            "postgresql",
            "mysql",
            "sqlite",
            "trino",
            "mssql",
            "oracle",
            "snowflake",
        ]:
            raise ValueError(f"Unsupported database dialect: {config.dialect.value}")

        # For non-SQLite databases, validate credentials
        if config.dialect.value != "sqlite":
            if not config.credentials:
                raise ValueError(
                    "Database credentials are required for non-SQLite databases"
                )
            if not config.credentials.host:
                raise ValueError("Database host is required")
            if not config.credentials.username:
                raise ValueError("Database username is required")
            if not config.credentials.password:
                raise ValueError("Database password is required")

        return config


class NLToSQLOutput(ToolOutput):
    """Output model for NL-to-SQL conversion"""

    sql_query: str = Field(description="Generated PostgreSQL query")
    dialect_sql_query: t.Optional[str] = Field(
        default=None, description="Query converted to target database dialect"
    )
    explanation: str = Field(description="Explanation of the generated SQL query")
    table_selection_explanation: str = Field(
        description="Explanation of why specific tables were selected"
    )
    selected_tables: list[dict[str, t.Any]] = Field(
        description="List of tables that were selected for the query"
    )
    database_name: str = Field(description="Name of the database used")
