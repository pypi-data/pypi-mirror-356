# Placeholder for table_profiler.py

from .base_profiler import BaseProfiler
from typing import Dict, List
import traceback
from logger.custom_logs import LoggerConfigurator

# Configure logger
logger_configurator = LoggerConfigurator()
logger = logger_configurator.get_logger()

class TableProfiler(BaseProfiler):
    def profile(self, database: str, schema: str, table: str) -> Dict:
        """Wrapper to maintain compatibility with BaseProfiler."""
        try:
            return self.profile_table(database, schema, table)
        except Exception as e:
            logger.error(f"{str(e)}\n{traceback.format_exc()}")

    def get_table_list(self, database: str, schema: str) -> List[Dict]:
        """Get list of tables in schema"""
        query = self.executor.render_query(
            "get_tables.sql.j2",
            {"database_name": database, "schema_name": schema}
        )
        return self.executor.execute(query)
    
    def get_column_metadata(self, database: str, schema: str, table: str) -> List[Dict]:
        """Get column metadata for a table"""
        query = self.executor.render_query(
            "get_columns.sql.j2",
            {"database_name": database, "schema_name": schema, "table_name": table}
        )
        return self.executor.execute(query)
    
    def profile_table(self, database: str, schema: str, table: str) -> Dict:
        """Profile an entire table"""
        columns = self.get_column_metadata(database, schema, table)
        row_count = self._get_row_count(database, schema, table)
        
        profile = {
            "database": database,
            "schema": schema,
            "table": table,
            "row_count": row_count,
            "columns": {}
        }
        
        for col in columns:
            profile["columns"][col["column_name"]] = {
                "data_type": col["data_type"],
                "is_nullable": col["is_nullable"]
            }
        
        return profile
    
    def _get_row_count(self, database: str, schema: str, table: str) -> int:
        """Get row count for a table"""
        query = self.executor.render_query(
            "table_row_count.sql.j2",
            {"database_name": database, "schema_name": schema, "table_name": table}
        )
        result = self.executor.execute(query)
        return result[0]["count"] if result else 0