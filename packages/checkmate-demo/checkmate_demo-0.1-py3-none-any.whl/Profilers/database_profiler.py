# database_profiler.py
import uuid
import datetime
from typing import Dict, List, Optional, Union
from .base_profiler import BaseProfiler
from .table_profiler import TableProfiler
from .column_profiler import ColumnProfiler
import traceback
from logger.custom_logs import LoggerConfigurator

# Configure logger
logger_configurator = LoggerConfigurator()
logger = logger_configurator.get_logger()

class DatabaseProfiler(BaseProfiler):
    def __init__(self, executor):
        super().__init__(executor)
        self.table_profiler = TableProfiler(executor)
        self.column_profiler = ColumnProfiler(executor)
    
    def profile(self, 
               database: str,
               schema: str, 
               tables: Optional[Union[List[str], str]] = None,
               columns: Optional[Union[List[str], str]] = None) -> Dict:
        """
        Profile database, tables, or columns based on provided parameters.
        Follows a hierarchical approach:
        - When no tables specified: profile entire database
        - When tables specified but no columns: profile specified tables
        - When both tables and columns specified: profile specific columns
        
        Args:
            database: Database name (mandatory)
            schema: Database schema name (mandatory)
            tables: Single table name or list of table names
            columns: Single column name or list of column names
            
        Returns:
            Dictionary containing profiling results with consistent structure
        """
        try:
            # Validate mandatory parameters
            if not database or not schema:
                raise ValueError("Both database and schema must be specified")
                
            # Normalize inputs
            tables = self._normalize_to_list(tables)
            columns = self._normalize_to_list(columns)
            
            # Validate inputs
            if columns and not tables:
                raise ValueError("Cannot specify columns without specifying table(s)")
            if columns and len(tables) > 1:
                raise ValueError("Cannot specify columns across multiple tables")
                
            # Determine profiling level
            if not tables:
                return self._profile_database(database, schema)
            elif not columns:
                return self._profile_tables(database, schema, tables)
            else:
                return self._profile_columns(database, schema, tables[0], columns)
        except Exception as e:
            logger.error(f"{str(e)}\n{traceback.format_exc()}")

    def _normalize_to_list(self, input_val: Optional[Union[List[str], str]]) -> List[str]:
        """Helper to normalize str or List[str] to List[str]"""
        if input_val is None:
            return []
        return [input_val] if isinstance(input_val, str) else input_val

    def _profile_database(self, database: str, schema: str) -> Dict:
        """Profile entire database"""
        tables = [t["table_name"] for t in self.table_profiler.get_table_list(database, schema)]
        return self._profile_tables(database, schema, tables)

    def _profile_tables(self, database: str, schema: str, tables: List[str]) -> Dict:
        """Profile multiple tables with all their columns"""
        results = self._create_results_header()
        
        for table in tables:
            table_profile = self._profile_single_table(database, schema, table)
            results["results"][f"{database}.{schema}.{table}"] = table_profile
        
        return results

    def _profile_single_table(self, database: str, schema: str, table: str) -> Dict:
        """Profile single table with all its columns"""
        table_profile = self.table_profiler.profile_table(database, schema, table)
        
        for col_name, col_meta in table_profile["columns"].items():
            table_profile["columns"][col_name].update(
                self.column_profiler.profile_column(
                    database, schema, table, col_name, col_meta["data_type"]
                )
            )
        
        return table_profile

    def _profile_columns(self, database: str, schema: str, table: str, columns: List[str]) -> Dict:
        """Profile specific columns in a table"""
        results = self._create_results_header()
        table_profile = self._profile_single_table(database, schema, table)
        
        # Filter to only requested columns
        filtered_columns = {
            col: table_profile["columns"][col] 
            for col in columns 
            if col in table_profile["columns"]
        }
        
        if not filtered_columns:
            raise ValueError(f"None of specified columns found in {database}.{schema}.{table}")
        
        results["results"][f"{database}.{schema}.{table}"] = {
            **table_profile,
            "columns": filtered_columns
        }
        
        return results

    def _create_results_header(self) -> Dict:
        """Create standard results header with metadata"""
        return {
            "run_id": str(uuid.uuid4()),
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "results": {}
        }