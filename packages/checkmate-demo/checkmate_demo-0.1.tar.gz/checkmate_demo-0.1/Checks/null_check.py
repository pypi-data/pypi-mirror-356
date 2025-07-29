from Checks.base import BaseCheck
from Query_builder.PSQL_queries import QueryBuilder
import datetime

class NullCheck(BaseCheck):
    def run(self,check_id,alerting_enabled, logger):
        results = []
        for column in self.config['columns']:
            query = QueryBuilder.null_check_query(self.config['database'], self.config['schema'], self.config['table'], column)
            null_pct = self.connector.run_query(query)[0]['null_pct']
            threshold_value = float(self.config.get('threshold')['max_null_percentage'])
            status = "fail" if null_pct > threshold_value else "pass"
            results.append({
                "check_name": "null_check",
                "database": self.config['database'],
                "schema": self.config['schema'],
                "table": self.config['table'],
                "column": column,
                "null_percentage": float(null_pct),
                "threshold_value": threshold_value,
                "check_status" : status,
                "alert_status" : alerting_enabled,
                "checked_at": datetime.datetime.now().isoformat(),
                "run_id": check_id
            })
        return results
