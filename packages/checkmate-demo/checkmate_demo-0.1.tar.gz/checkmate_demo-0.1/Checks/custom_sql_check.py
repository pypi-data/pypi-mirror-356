from Checks.base import BaseCheck
import datetime
from simpleeval import simple_eval, InvalidExpression
from collections import deque

class CustomSQLCheck(BaseCheck):
    def __init__(self, connector, check_config, batch_size: int = 1000, sample_size: int = 5):
        self.connector = connector
        self.check_config = check_config
        self.batch_size = batch_size
        self.sample_size = sample_size

    def run(self,check_id,alerting_enabled, logger):
        # Prepare summary counters and sample deque
        total_rows = 0
        violating_count = 0
        sample_rows = deque(maxlen=self.sample_size)
        check_name = self.check_config["name"]
        database = self.check_config["database"]
        schema = self.check_config["schema"]
        table = self.check_config["table"]

        sql_query = self.check_config["query"]
        condition = self.check_config["threshold"]["acceptable_condition"]

        logger.info(f"Evaluating condition - '{condition}' on '{database}.{schema}.{table}' against results of below query as part of custom SQL check: \n {sql_query} ")

        # Fetch and process in batches
        for batch in self.connector.run_query_batch(sql_query, batch_size=self.batch_size):
            # batch is expected as list of dicts [{col1: val1, col2: val2, ...}, ...]
            for row in batch:
                total_rows += 1
                try:
                    ok = simple_eval(condition, names=row)
                except InvalidExpression as e:
                    raise ValueError(f"Invalid condition '{condition}': {e}")
                except Exception as e:
                    # Treat evaluation errors as violations
                    ok = False

                if not ok:
                    violating_count += 1
                    # capture first few violations
                    if len(sample_rows) < self.sample_size:
                        sample_rows.append(row)

        if violating_count:
            result = {
                "check_name": check_name,
                "database": database,
                "schema": schema,
                "table": table,
                "query": sql_query,
                "check_status": "fail",
                "result_summary": {
                    "rows_checked": total_rows,
                    "violations_sample": list(sample_rows),
                    "violation_count": violating_count
                },
                "threshold_condition": condition,
                "alert_status" : alerting_enabled,
                "checked_at": datetime.datetime.now().isoformat(),
                "run_id": check_id
            }
        else:
            result = {
                "check_name": check_name,
                "database": database,
                "schema": schema,
                "table": table,
                "query": sql_query,
                "check_status": "pass",
                "threshold_condition": condition,
                "alert_status" : alerting_enabled,
                "checked_at": datetime.datetime.now().isoformat(),
                "run_id": check_id
            }
            
        return result
