from Checks.null_check import NullCheck
from Checks.pii_check import PiiChecker
from Checks.row_count_check import RowCountCheck
from Checks.custom_sql_check import CustomSQLCheck
from Notification.notification_service import NotificationService 
from Connectors.credential_manager import CredentialManager
from audit.results_auditing import  ResultAuditor
from Connectors.connector_factory import ConnectorFactory
from logger.custom_logs import LoggerConfigurator
import traceback

CHECK_MAPPING = {
     "null_check": NullCheck,
    "pii_check": PiiChecker,
     "row_count_check" : RowCountCheck,
     "custom_sql_check" : CustomSQLCheck
}

class CheckRunner:
    def __init__(self, full_config, connector, check_id, alerting_enabled, auditing_enabled, data_source):
        self.full_config = full_config
        self.connector = connector
        self.check_id = check_id
        self.alerting_enabled = alerting_enabled
        self.auditing_enabled = auditing_enabled
        self.data_source = data_source
        try:
            logger_configurator = LoggerConfigurator()
            self.logger = logger_configurator.get_logger()
            self.logger.info("Initializing auditing and alerting services..")
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
        except Exception as e:
            self.logger.error(f"{str(e)}\n{traceback.format_exc()}")
            print(f"Error occurred: {str(e)}, Check logs for more details")
            raise e
        

    def run_all(self):
        try:
            notified_results = []
            print("Starting checks on data as per config YAML..")
            for check_cfg in self.full_config['checks']:
                check_name = check_cfg['name']
                check_class = CHECK_MAPPING.get(check_name)
                if check_class:
                    check_instance = check_class(self.connector, check_cfg)
                    check_result = check_instance.run(self.check_id, self.alerting_enabled, self.logger)
                    self.logger.info(f"{check_name} completed! \n Results: {check_result}")
                    results_to_process = check_result if isinstance(check_result, list) else [check_result]
                    for result in results_to_process:
                        if self.alerting_enabled and result.get('check_status') == 'fail':
                            notified_result = self.notification_service.notify(result)
                            notified_results.append(notified_result)
                            if notified_result.get('alert_sent') == 'yes':
                                self.logger.info(f"Alert sent for {check_name} via: {notified_result['alerted_via']}!")
                        else:
                            notified_result = { **result, 'alert_sent': False,'alerted_via': None }
                            notified_results.append(notified_result)
                else:
                    if check_name == 'freshness_check':
                        continue
                    else:
                        self.logger.warning(f"No mapping configured for specified check - {check_name}!")
            
            if self.auditing_enabled:
                if notified_results:
                    self.result_auditor.insert_check_results(notified_results, self.data_source)
                    self.logger.info(f"Results saved to RDS audit table!")
            print("All checks completed!")
            return notified_results
        except Exception as e:
            self.logger.error(f"{str(e)}\n{traceback.format_exc()}")
            print(f"Error occurred: {str(e)}, Check logs for more details")
            raise e

    def run_selected(self, selected_check_names):
        try:
            notified_results = []
            print("Starting checks on data as per config YAML..")
            for check_cfg in self.full_config['checks']:
                check_name = check_cfg['name']
                if check_name in selected_check_names:
                    check_class = CHECK_MAPPING.get(check_name)
                    if check_class:
                        check_instance = check_class(self.connector, check_cfg)
                        check_result = check_instance.run(self.check_id, self.alerting_enabled, self.logger)
                        self.logger.info(f"{check_name} completed! \n Results: {check_result}")
                        results_to_process = check_result if isinstance(check_result, list) else [check_result]
                        for result in results_to_process:
                            if self.alerting_enabled and result.get('check_status') == 'fail':
                                notified_result = self.notification_service.notify(result)
                                notified_results.append(notified_result)
                                if notified_result.get('alert_sent') == 'yes':
                                    self.logger.info(f"Alert sent for {check_name} via: {notified_result['alerted_via']}!")
                            else:
                                notified_result = { **result, 'alert_sent': False,'alerted_via': None }
                                notified_results.append(notified_result)
                    else:
                        self.logger.warning(f"No mapping configured for specified check - {check_name}!")
            if self.auditing_enabled:
                if notified_results:
                    self.result_auditor.insert_check_results(notified_results, self.data_source)
                    self.logger.info(f"Results saved to RDS audit table!")
            print("All checks completed!")
            return notified_results
        except Exception as e:
            self.logger.error(f"{str(e)}\n{traceback.format_exc()}")
            print(f"Error occurred: {str(e)}, Check logs for more details")
            raise e



