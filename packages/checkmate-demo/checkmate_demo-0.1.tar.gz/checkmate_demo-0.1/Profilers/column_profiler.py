from .base_profiler import BaseProfiler
from typing import Dict
import traceback
from logger.custom_logs import LoggerConfigurator

# Configure logger
logger_configurator = LoggerConfigurator()
logger = logger_configurator.get_logger()


class ColumnProfiler(BaseProfiler):
    def profile(self, database: str, schema: str, table: str, column: str, dtype: str) -> Dict:
        try:
            """Implements abstract method."""
            return self.profile_column(database, schema, table, column, dtype)
        except Exception as e:
            logger.error(f"{str(e)}\n{traceback.format_exc()}")


    def profile_column(self, database: str, schema: str, table: str, column: str, dtype: str) -> Dict:
        """Profile a single column"""
        profile = {}

        # Basic stats (nulls, distinct counts)
        query = self.executor.render_query(
            "column_basic_stats.sql.j2",
            {
                "database_name": database,
                "schema_name": schema,
                "table_name": table,
                "column_name": column
            }
        )
        basic_stats = self.executor.execute(query)
        if basic_stats:
            profile.update(basic_stats[0])

        # Type-specific stats
        if dtype.lower() in ["int", "bigint", "numeric", "float", "double"]:
            query = self.executor.render_query(
                "column_numeric_stats.sql.j2",
                {
                    "database_name": database,
                    "schema_name": schema,
                    "table_name": table,
                    "column_name": column
                }
            )
            numeric_stats = self.executor.execute(query)
            if numeric_stats:
                profile.update(numeric_stats[0])

        elif dtype.lower() in ["varchar", "character varying", "text", "char", "string"]:
            query = self.executor.render_query(
                "column_text_stats.sql.j2",
                {
                    "database_name": database,
                    "schema_name": schema,
                    "table_name": table,
                    "column_name": column
                }
            )
            text_stats = self.executor.execute(query)
            if text_stats:
                profile.update(text_stats[0])

        return profile