import traceback
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from concurrent.futures import ThreadPoolExecutor, as_completed
from Checks.Freshness_Check.freshness_check import FreshnessCheck
from Notification.notification_service import NotificationService 
from Connectors.credential_manager import CredentialManager
from audit.results_auditing import  ResultAuditor
from Connectors.connector_factory import ConnectorFactory
from logger.custom_logs import LoggerConfigurator
import signal
import threading
import sys

class FreshnessMonitor:
    def __init__(self, full_config, check_cfg, connector, check_id, alerting_enabled, auditing_enabled, data_source):
        self.connector = connector
        self.check_cfg = check_cfg
        self.check_id = check_id
        self.alerting_enabled = alerting_enabled
        self.full_config = full_config
         # Use BackgroundScheduler instead of BlockingScheduler
        self.scheduler = BackgroundScheduler({'apscheduler.timezone': 'Asia/Calcutta'})
        self.scheduler.add_listener(self._scheduler_listener, 
                          EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        
        # Thread pool for running checks
        self.executor = ThreadPoolExecutor(max_workers=10, thread_name_prefix="FreshnessCheck")

        logger_configurator = LoggerConfigurator()
        self.logger = logger_configurator.get_logger()
        
        # Shutdown coordination
        self.shutdown_flag = threading.Event()
        self.main_thread = None
        self.running_futures = set()
        self._lock = threading.Lock()
        self.data_source = data_source

        if alerting_enabled:
            alert_cred_manager = CredentialManager(full_config)
            smtp_creds = webhook_url = None
            for channel in full_config['alerts']['channels']:
                if channel['type'] == 'email':
                    smtp_creds = alert_cred_manager.get_smtp_credentials('email')
                if channel['type'] == 'slack':
                    webhook_url = alert_cred_manager.get_slack_webhook_url('slack')
            self.notification_service = NotificationService(full_config, smtp_creds, webhook_url)

        if auditing_enabled:
            audit_connector = ConnectorFactory.get_connector(full_config, usage='audit')
            self.result_auditor = ResultAuditor(audit_connector)

    
    def _run_check(self):
        """Run freshness check in background thread."""
        future = None
        try:
            # Submit the actual check to thread pool
            future = self.executor.submit(self._execute_check)
            
            # Track running futures for graceful shutdown
            with self._lock:
                self.running_futures.add(future)
            
            # Wait for completion (non-blocking for scheduler)
            result = future.result(timeout=3600)  # 1 hour timeout
            print(f"Freshness Check completed - Status: {result.get('check_status', 'unknown')}")

            if self.alerting_enabled and result.get('check_status') == 'fail':
                notified_result = self.notification_service.notify(result)
                if notified_result.get('alert_sent') == 'yes':
                    self.logger.info(f"Alert sent for Freshness check via: {notified_result['alerted_via']}")
            else:
                notified_result = { **result, 'alert_sent': False,'alerted_via': None }
            
            if self.full_config['audit']['enabled'] == True:
                if notified_result:
                    self.result_auditor.insert_check_results([notified_result],self.data_source)
                    self.logger.info(f"Results saved to RDS audit table!")

            
        except Exception as e:
            self.logger.error(f"{str(e)}\n{traceback.format_exc()}")
            print(f"Error occurred: {str(e)}, Check logs for more details")
            raise e
        finally:
            # Clean up completed future
            if future:
                with self._lock:
                    self.running_futures.discard(future)

    def _execute_check(self):
        """Actually execute the freshness check."""
        try:
            check = FreshnessCheck(config_obj = self.full_config, check_config=self.check_cfg, connector=self.connector, data_source = self.data_source,\
                                   logger = self.logger)
            result = check.run(self.check_id, self.alerting_enabled)
            self.logger.info(f"Freshness Check result: {result}")
            return result
        except Exception as e:
            self.logger.error(f"{str(e)}\n{traceback.format_exc()}")
            print(f"Error occurred: {str(e)}, Check logs for more details")
            raise


    def _scheduler_listener(self, event):
        if event.code == EVENT_JOB_EXECUTED:
            self.logger.info(f"Job {event.job_id} executed successfully")
        elif event.code == EVENT_JOB_ERROR:
            self.logger.info(f"Job {event.job_id} failed with exception: {event.exception}")

    def start(self):
        """Start the perpetual monitor with proper background execution."""
        try:
            # Store reference to main thread
            self.main_thread = threading.current_thread()
            
            # Set up signal handlers for graceful shutdown
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)

            # Add the job to scheduler
            cron_config = self._parse_cron(self.check_cfg["expected_refresh_schedule"])
            job = self.scheduler.add_job(
                self._run_check,  # Run the wrapper method directly
                'cron',
                id=f'freshness_check_{self.check_id}',
                max_instances=1,  # Prevent overlapping runs
                coalesce=True,    # Combine missed runs
                **cron_config
            )

            self.logger.info(f"Scheduled job: {job}")
            
            # Start the scheduler (non-blocking)
            self.scheduler.start()
            print("Freshness monitor started successfully.")
            print(f"Next run scheduled at: {job.next_run_time}")

            # Keep main thread alive but responsive
            self._wait_for_shutdown()
            
        except Exception as e:
            print(f"Failed to start freshness monitor: \n")
            self.logger.error(f"{str(e)}\n{traceback.format_exc()}")
            raise

    def _parse_cron(self, cron_expr: str):
        """Convert cron expression to APScheduler kwargs."""
        try:
            parts = cron_expr.strip().split()
            if len(parts) < 5:
                raise ValueError(f"Invalid cron expression: {cron_expr}")
                
            return {
                "minute": parts[0],
                "hour": parts[1],
                "day": parts[2],
                "month": parts[3],
                "day_of_week": parts[4],
            }
        except Exception as e:
            print(f"Error parsing cron expression '{cron_expr}': {e}")
            raise

    def _wait_for_shutdown(self):
        """Keep main thread alive while monitoring for shutdown signal."""
        try:
            while not self.shutdown_flag.is_set():
                # Use wait with timeout to remain responsive to signals
                self.shutdown_flag.wait(timeout=1.0)
                
        except KeyboardInterrupt:
            self.logger.info("KeyboardInterrupt received in main loop")
            self._initiate_shutdown()

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        print(f"Received signal {signum}, initiating graceful shutdown...")
        self._initiate_shutdown()

    def _initiate_shutdown(self):
        """Initiate graceful shutdown process."""
        if self.shutdown_flag.is_set():
            return  # Already shutting down
            
        print("Starting graceful shutdown...")
        self.shutdown_flag.set()
        
        try:
            # Stop scheduler from accepting new jobs
            if self.scheduler.running:
                self.logger.info("Pausing scheduler...")
                self.scheduler.pause()
            
            # Wait for running checks to complete
            self._wait_for_running_checks()
            
            # Shutdown scheduler
            self.logger.info("Shutting down scheduler...")
            self.scheduler.shutdown(wait=True)
            
            # Shutdown executor
            self.logger.info("Shutting down executor...")
            self.executor.shutdown(wait=True)
            
            self.executor.shutdown(wait=False)
            
            print("Graceful shutdown completed")
            
        except Exception as e:
            print(f"Error during shutdown: \n")
            self.logger.error(f"{str(e)}\n{traceback.format_exc()}")
        finally:
            # Force exit if we're in the main thread
            if threading.current_thread() == self.main_thread:
                sys.exit(0)

    def _wait_for_running_checks(self, timeout=60):
        """Wait for running checks to complete with timeout."""
        if not self.running_futures:
            return
            
        self.logger.info(f"Waiting for {len(self.running_futures)} running checks to complete...")
        
        try:
            # Wait for all futures to complete
            completed_futures = as_completed(self.running_futures, timeout=timeout)
            for future in completed_futures:
                try:
                    result = future.result(timeout=1)
                    self.logger.info("Check completed during shutdown")
                except Exception as e:
                    self.logger.error(f"Check failed during shutdown: {e}")
                    
        except Exception as e:
            print(f"Timeout waiting for checks to complete: {e}")
            # Cancel remaining futures
            with self._lock:
                for future in self.running_futures:
                    future.cancel()
    
    def stop(self):
        """Public method to stop the monitor."""
        self._initiate_shutdown()