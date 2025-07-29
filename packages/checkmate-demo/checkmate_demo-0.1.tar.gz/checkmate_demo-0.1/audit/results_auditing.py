from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
from Connectors.base import BaseConnector
from Connectors.credential_manager import CredentialManager
from Connectors.rds_connector import RDSConnector
from Error.errorHandler import DatabaseOperationError
from Query_builder.PSQL_queries import QueryBuilder
from sqlalchemy.exc import SQLAlchemyError, DBAPIError
import logging
from datetime import datetime
import json
import uuid
from decimal import Decimal
import traceback
class ResultAuditor:
 def __init__(self, rds_connector):
    self.connector = rds_connector
    if not self.connector.engine:
       self.connector.connect()
    # Create tables
    self.create_profiling_result_table()  # Corrected method name
    self.create_check_result_table()

 def create_profiling_result_table(self):
     try:
         create_query = QueryBuilder.create_profiling_result_table()
         self.connector.execute_non_query(create_query)
     except Exception as e:
            self.logger.error(f"Failed to create audit result table: {e}")
            raise e

 def create_check_result_table(self):
     try:
         create_query = QueryBuilder.create_check_result_table()
         self.connector.execute_non_query(create_query)
     except Exception as e:
            self.logger.error(f"Failed to create audit result table: {e}")
            raise e

 def insert_profiling_results(self, results: dict, data_source):
     def convert_decimal(obj):
         if isinstance(obj, Decimal):
             return float(obj)
         raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

    #  if not self.connector.engine:
    #      try:
    #          self.connector.connect()
    #      except Exception as e:
    #          raise DatabaseOperationError("Failed to connect to the database") from e
         
     insert_sql = QueryBuilder.insert_profiling_results_query()
     run_id = results.get('run_id')
     profiled_at = results.get('timestamp')
     if profiled_at:
         profiled_at = datetime.fromisoformat(profiled_at.replace("Z", "+00:00"))

     all_tables = results.get('results', {})

     try:
         with self.connector.engine.begin() as conn:
             for fq_table_name, table_info in all_tables.items():
                 database_name = table_info.get('database')
                 schema_name = table_info.get('schema')
                 table_name = table_info.get('table')
                 columns = table_info.get('columns', {})

                 for col_name, col_stats in columns.items():
                     stats = {
                         "distinct_count": col_stats.get("distinct_count"),
                         "avg_length": float(col_stats.get("avg_length", 0)),
                         "max_length": col_stats.get("max_length"),
                         "min_length": col_stats.get("min_length"),
                         "empty_count": col_stats.get("empty_count"),
                     }

                     # Fix nullable type: convert "YES"/"NO" to boolean
                     nullable = col_stats.get("is_nullable", False)
                     if isinstance(nullable, str):
                         nullable = nullable.strip().upper() == "YES"

                     data = {
                         "run_id": run_id,
                         "profiled_at": profiled_at,
                         "database_name": database_name,
                         "schema_name": schema_name,
                         "table_name": table_name,
                         "column_name": col_name,
                         "data_type": col_stats.get("data_type"),
                         "nullable": nullable,
                         "non_null_count": col_stats.get("non_null_count", 0),
                         "null_count": col_stats.get("null_count", 0),
                         "stats": json.dumps(stats, default=convert_decimal),
                         "data_source": data_source
                     }

                     try:
                         conn.execute(text(insert_sql), data)
                     except Exception as e:
                         print("Insert failed for row:", data)
                         print("Error:", str(e))
                         raise DatabaseOperationError("Database error during profiling results insert") from e

     except SQLAlchemyError as e:
         print("Actual SQLAlchemy error:", str(e))
         raise DatabaseOperationError("SQLAlchemy error during profiling results insert") from e
     except Exception as e:
         print("Insert failed for row:", data)
         print("Error:", str(e))
         raise DatabaseOperationError("Unhandled error during profiling results insert") from e

 def insert_check_results(self, check_results: list, data_source):
    """
    Save static check results (flat list of dicts) to db.audit_checks.
    """
    # if not self.connector.engine:
    #     try:
    #         self.connector.connect()
    #     except Exception as e:
    #         raise DatabaseOperationError("Failed to connect to the database") from e

    #create_checks_sql=QueryBuilder.create_check_result_table()
    insert_sql = QueryBuilder.insert_check_results_query()

    try:
        with self.connector.engine.begin() as conn:
            #conn.execute(text(create_checks_sql))
            for check in check_results:
                checked_at = check.get("checked_at")
                if checked_at:
                    checked_at = datetime.fromisoformat(str(checked_at).replace("Z", "+00:00"))

                # Convert 'enabled' / 'disabled' string to boolean
                alert_status = check.get("alert_status", False)
                # if isinstance(alert_status, str):
                #     alert_status = alert_status.lower() == "enabled"

                # Fields to exclude from check_metadata (already stored in other columns)
                exclude_keys = {
                    "run_id", "check_name", "checked_at", "database",
                    "schema", "table", "column", "check_status",
                    "alert_status", "alert_sent", "alerted_via"
                }

                # Constructing check_metadata by excluding already stored fields
                check_metadata = {
                    k: v for k, v in check.items() if k not in exclude_keys
                }

                alert_channel = json.dumps([k for k,v in check.get('alerted_via').items()], default=str) if check.get('alerted_via') else None
                alert_recipient =  json.dumps(check.get('alerted_via'), default=str) if check.get('alerted_via') else None

                data = {
                    "run_id": check.get("run_id"),
                    "check_name": check.get("check_name"),
                    "checked_at": checked_at,
                    "database_name": check.get("database"),
                    "schema_name": check.get("schema"),
                    "table_name": check.get("table"),
                    "column_name": check.get("column"),
                    "check_status": check.get("check_status"),
                    "alert_status": alert_status,
                    "alert_sent": check.get("alert_sent", False),
                    "alert_channel": alert_channel,
                    "alert_recipient": alert_recipient,
                    "check_metadata": json.dumps(check_metadata, default=str),
                    "data_source": data_source
                }

                try:
                    conn.execute(text(insert_sql), data)
                except Exception as e:
                    # logger.error("DBAPIError: %s | Row: %s", str(e), data)
                    raise DatabaseOperationError("Database error during check results insert") from e

    except SQLAlchemyError as e:
        # logger.error("SQLAlchemyError: %s", str(e))
        raise DatabaseOperationError("SQLAlchemy error during check results insert") from e
    except Exception as e:
        # logger.exception("Unhandled exception during check results insert")
        self.logger.error(f"{str(e)}\n{traceback.format_exc()}")
        raise DatabaseOperationError("Unhandled error during check results insert") from e