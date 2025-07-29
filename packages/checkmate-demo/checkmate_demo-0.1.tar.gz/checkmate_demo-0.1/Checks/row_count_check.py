from Checks.base import BaseCheck
from Query_builder.PSQL_queries import QueryBuilder
import datetime

class RowCountCheck(BaseCheck):
    def run(self,check_id,alerting_enabled, logger):
        result = {}
        query = QueryBuilder.row_count_check_query(self.config['database'], self.config['schema'], self.config['table'])
        row_cnt = self.connector.run_query(query)[0]['row_cnt']
        threshold_value = self.config.get('threshold')['expected_range']
        min_expected = threshold_value.get("min", 0)
        max_expected = threshold_value.get("max", float("inf"))
        status = "fail" if not (min_expected <= row_cnt <= max_expected) else "pass"
        result = {
            "check_name": "row_count_check",
            "database": self.config['database'],
            "schema": self.config['schema'],
            "table": self.config['table'],
            "current_row_count": row_cnt,
            "threshold_value": threshold_value,
            "check_status" : status,
            "alert_status" : alerting_enabled,
            "checked_at": datetime.datetime.now().isoformat(),
            "run_id": check_id
        }
        return result