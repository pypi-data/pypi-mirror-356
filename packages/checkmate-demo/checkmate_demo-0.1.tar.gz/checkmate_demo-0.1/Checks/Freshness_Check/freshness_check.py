import time
import datetime
from croniter import croniter
from Checks.base import BaseCheck
from Query_builder.PSQL_queries import QueryBuilder
from jinja2 import Template

class FreshnessCheck(BaseCheck):
    def __init__(self, config_obj, connector, check_config, data_source, logger, check_interval = 30):
        self.connector = connector
        self.config = config_obj
        self.table = check_config["table"]
        self.database = check_config["database"]
        self.schema = check_config["schema"]
        self.check_name = "freshness_check"
        self.cron_schedule = check_config["expected_refresh_schedule"]
        self.check_window = check_config["time_tolerance_minutes"]
        self.check_interval = check_interval
        self.check_modes = ['row_count'] #Row count is default check
        self.checksum_columns = None
        self.updated_at_column = None
        self.data_source = data_source
        self.logger = logger

        polling_modes = check_config.get("polling_modes")
        if polling_modes:
            for item in polling_modes:
                if isinstance(item, dict):
                    self.check_modes.extend(item.keys())
                    if 'checksum' in item.keys():
                        self.checksum_columns = item.get('checksum')
                    elif 'update_column' in item.keys():
                        self.updated_at_column = item.get('update_column')

        logger.info(f"Creating freshness tracking SP in schema - {self.schema} if it does not exist already..")
        if self.data_source == 'rds':
            with open('Checks/Freshness_Check/tracking_sp_template_rds.sql', 'r') as f:
                template = Template(f.read()).render({"schema_name": self.schema})
        elif self.data_source == 'redshift':
            with open('Checks/Freshness_Check/tracking_sp_template_redshift.sql', 'r') as f:
                template = Template(f.read()).render({"schema_name": self.schema})
        self.connector.execute_non_query(template)

        logger.info(f"Creating freshness tracking table in schema - {self.schema} if it does not exist already..")
        create_table_query = QueryBuilder.create_tracking_table_if_not_exists(self.schema)
        self.connector.execute_non_query(create_table_query)

    def call_populate_sp(self, check_id, data_source, checksum_columns_mod):
        try:
            if data_source == 'rds':
                query = QueryBuilder.call_tracker_sp_query_rds(check_id, self.database,  self.schema, self.table, self.updated_at_column, checksum_columns_mod)
            elif data_source == 'redshift':
                query = QueryBuilder.call_tracker_sp_query_redshift(check_id, self.database,  self.schema, self.table, self.updated_at_column, checksum_columns_mod)
            self.connector.execute_non_query(query)
        except Exception as e:
            print(f"Failed to call stored procedure: {e}")
            raise e
        
    def query_tracking_table(self, mode):
        try:
            if mode == 'checksum':
                col_name = 'table_checksum'
            elif mode == 'update_column':
                col_name = 'max_updated_at'
            else:
                col_name = mode
            
            query = QueryBuilder.tracking_table_snapshot_query(self.database, self.schema, self.table, col_name)
            result = self.connector.run_query(query)[0][col_name]
            return result
        except Exception as e:
            print(f"Failed to query tracking table: {e}")
            raise e
        
    def get_next_cron_window(self):
        now = datetime.datetime.now()
        iter = croniter(self.cron_schedule, now)
        prev_run = iter.get_prev(datetime.datetime)
        next_run = iter.get_next(datetime.datetime)

        prev_run_end = prev_run + datetime.timedelta(minutes=self.check_window)
        if now < prev_run_end:
            start_window = prev_run - datetime.timedelta(minutes=self.check_window)
            end_window = prev_run_end
        else:
            start_window = next_run - datetime.timedelta(minutes=self.check_window)
            end_window = next_run + datetime.timedelta(minutes=self.check_window)

        return start_window, end_window

    def run(self, check_id, alerting_enabled):
        
        start_window, end_window = self.get_next_cron_window()
        print(f"Monitoring refresh for {self.database}.{self.schema}.{self.table} between {start_window} and {end_window} using modes: {self.check_modes}")

        # Use timezone-aware datetime for consistency
        now = datetime.datetime.now()
        
        # Take initial snapshots closer to start time to minimize race conditions
        wait_until_start = max(0, (start_window - now).total_seconds() - 60)  # Start snapshots 1 min before window
        if wait_until_start > 0:
            self.logger.info(f"Waiting {wait_until_start} seconds before taking initial snapshots...")
            time.sleep(wait_until_start)

        # Take initial snapshots
        before_snapshots = {}

        checksum_columns_mod = None

        if self.data_source == 'rds':
            checksum_columns_mod = self.checksum_columns
        elif self.data_source == 'redshift':
            if self.checksum_columns:
                checksum_columns_mod = ",".join(self.checksum_columns)

        self.call_populate_sp(check_id, self.data_source, checksum_columns_mod)

        for mode in self.check_modes:
            before_snapshots[mode] = self.query_tracking_table(mode)
            self.logger.info(f"Initial {mode} snapshot: {before_snapshots[mode]}")

        # Wait for monitoring window to start
        now = datetime.datetime.now()
        remaining_wait = (start_window - now).total_seconds()
        if remaining_wait > 0:
            self.logger.info(f"Waiting {remaining_wait} seconds for monitoring window to start...")
            time.sleep(remaining_wait)

        refreshed = False
        check_interval = getattr(self, 'check_interval', 30)  # Make configurable
        current_snapshots = before_snapshots.copy()
        last_check_time = datetime.datetime.now()

        self.logger.info("Starting monitoring window...")
        while True:
            now = datetime.datetime.now()
            if now >= end_window:
                self.logger.info("Monitoring window ended")
                break
                
            print(f"Polling for changes... (remaining: {(end_window - now).total_seconds():.0f}s)")
            time.sleep(check_interval)

            try:
                # Call inserting sp
                self.call_populate_sp(check_id, self.data_source, checksum_columns_mod)
                
                # Check all modes for changes
                mode_refreshed = False
                for mode in self.check_modes:
                    current_snapshot = self.query_tracking_table(mode)
                    self.logger.info(f"Current {mode} snapshot: {current_snapshot}")

                    if current_snapshot != before_snapshots[mode]:
                        print(f"Detected change in {mode} at {datetime.datetime.now()}")
                        refreshed = True
                        mode_refreshed = True
                        current_snapshots[mode] = current_snapshot

                # If any mode detected a refresh, stop monitoring
                if mode_refreshed:
                    print("Refresh detected, stopping monitoring")
                    break
                    
            except Exception as poll_error:
                print(f"Error during polling: {poll_error}")
                # Continue monitoring unless it's a critical error
                continue

        status = "pass" if refreshed else "fail"
        
        result = {
            "check_name": self.check_name,
            "table": self.table,
            "database": self.database,
            "schema": self.schema,  # Added missing schema
            "cron_schedule": self.cron_schedule,
            "check_status": status,
            "alert_status": alerting_enabled,
            "previous_snapshots": {k: str(v) for k, v in before_snapshots.items()},
            "current_snapshots": {k: str(v) for k, v in current_snapshots.items()},
            "monitoring_window": {
                "start": start_window.isoformat(),
                "end": end_window.isoformat()
            },
            "checked_at": datetime.datetime.now().isoformat(),
            "run_id": check_id
        }

        if not refreshed:
            self.logger.info(f"No changes detected in {self.database}.{self.schema}.{self.table} for any mode during monitoring window!")
        else:
            self.logger.info(f"Successfully detected refresh in {self.database}.{self.schema}.{self.table}")

        return result