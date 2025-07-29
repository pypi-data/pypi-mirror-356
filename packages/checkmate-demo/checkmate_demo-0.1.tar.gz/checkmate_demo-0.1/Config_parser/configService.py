import yaml
import boto3
import os
from io import StringIO
from datetime import datetime
from botocore.exceptions import NoCredentialsError, ClientError, BotoCoreError
from typing import Dict, List, Optional, Any
from Error.errorHandler import (
    ConfigLoadError,
    ConfigValidationError,
    MissingSectionError,
    InvalidChecksError
)
from logger.custom_logs import LoggerConfigurator
import sys

class ConfigLoader:
    _instance = None
    _config = None

    logger_configurator = LoggerConfigurator()
    logger = logger_configurator.get_logger()

    REQUIRED_STRUCTURE = {
        "data_source": {
            "required_keys": ["type", "connection"],
            "nested": {
                "connection": {
                    "required_keys": ["environment"]
                }
            }
        },
        "checks": {
            "validation_function": "validate_checks"  # Special handling
        },
        "rule_mining": {
            "required_keys": ["enabled", "intensity", "enabled_checks"],
            "validation_function": "validate_rule_mining"  # Special handling for rule_mining
        }
    }
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
            # Initialize config directory for rule mining
            cls._instance.config_dir = "config"
            os.makedirs(cls._instance.config_dir, exist_ok=True)
        return cls._instance

    def load_config(self, file_path, aws_access_key=None, aws_secret_key=None):
        def is_s3_path(path):
            return path.startswith("s3://")

        def read_local_yaml(path):
            try:
                with open(path, 'r') as file:
                    return yaml.safe_load(file)
            except Exception as e:
                raise ConfigLoadError(f"Error reading local YAML file: {e}")

        def read_s3_yaml(path):
            try:
                s3 = boto3.client(
                    's3',
                    aws_access_key_id=aws_access_key,
                    aws_secret_access_key=aws_secret_key
                ) if aws_access_key else boto3.client('s3')

                bucket, key = path.replace("s3://", "").split("/", 1)
                obj = s3.get_object(Bucket=bucket, Key=key)
                return yaml.safe_load(StringIO(obj['Body'].read().decode('utf-8')))
            except (ClientError, NoCredentialsError, BotoCoreError) as e:
                raise ConfigLoadError(f"Error reading S3 YAML file: {e}")

        try:
            self._config = read_s3_yaml(file_path) if is_s3_path(file_path) else read_local_yaml(file_path)
            self._validate_yaml_config()
            return self._config
        except (ConfigLoadError, ConfigValidationError, MissingSectionError, InvalidChecksError) as e:
            print(e)
            sys.exit(0)
            #self._config = {}

    def get_config(self):
        return self._config if self._config is not None else {}
    
    def save_config(self, config_data: Dict, filename: str = None) -> str:
        """Save configuration to YAML file (returns filepath) - for rule mining integration"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"auto_generated_config_{timestamp}.yaml"
        filepath = os.path.join(self.config_dir, filename)
        with open(filepath, 'w') as f:
            yaml.dump(config_data, f, default_flow_style=False, indent=2, sort_keys=False)
        return filepath

    def load_external_config(self, filepath: str) -> Dict:
        """Load an external YAML config (returns dict) - for rule mining integration"""
        try:
            with open(filepath, 'r') as f:
                config = yaml.safe_load(f)
                # Validate if it contains rule mining section
                if 'rule_mining' in config:
                    self._validate_rule_mining_config(config)
                return config
        except Exception as e:
            raise ConfigLoadError(f"Error loading external config: {e}")

    def get_user_confirmation(self, auto_config_path: str, original_config_path: str) -> bool:
        """
        Prompt user to choose between auto_generated vs original YAML - for rule mining integration
        """
        print("\n" + "="*60)
        print("RULE MINING COMPLETED")
        print("="*60)
        print(f"Auto-generated config created at: {auto_config_path}")
        print(f"Original config available at:    {original_config_path}")
        print("="*60)
        while True:
            print("\nAuto-config generation complete. Please review the generated file.")
            response = input("Use the auto-generated configuration? (Y/N): ").strip().upper()
            if response in ['Y', 'YES']:
                return True
            elif response in ['N', 'NO']:
                return False
            else:
                print("Please enter Y or N")

    def merge_rule_mining_config(self, rule_mining_config: Dict) -> Dict:
        """
        Merge rule mining configuration with existing config
        """
        if self._config is None:
            self._config = {}
        
        # Merge rule mining config into existing config
        merged_config = self._config.copy()
        if 'rule_mining' in rule_mining_config:
            merged_config['rule_mining'] = rule_mining_config['rule_mining']
        
        # Validate the merged configuration
        temp_config = self._config
        self._config = merged_config
        try:
            self._validate_rule_mining_config(merged_config)
            return merged_config
        except Exception as e:
            self._config = temp_config
            raise e

    def _validate_config_section(self, section_path, requirements):
        """Validate a single configuration section with dynamic environment-aware logic"""
        errors = []
        current = self._config
	
        # Navigate through nested sections
        for section in section_path.split('.'):
            if section not in current:
                raise MissingSectionError(section_path)
            current = current[section]
	
        # Environment-aware validation
        if isinstance(current, dict) and "environment" in current:
            environment = current["environment"]

            if environment == "secrets_manager":
                for key in ["secret_arn", "region"]:
                    if key not in current:
                        raise MissingSectionError(f"{section_path}.{key}")
            elif environment == "env_variable":
                for key in ["host", "port", "database", "user", "password"]:
                    if key not in current:
                        raise MissingSectionError(f"{section_path}.{key}")
            else:
                raise ConfigValidationError(
                    f"{section_path}.environment value '{environment}' is not supported"
                )
        else:
            # Default key validation
            for key in requirements.get("required_keys", []):
                if key not in current:
                    raise MissingSectionError(section_path + "." + key)
	
        # Recursively check nested sections
        for nested_section, nested_reqs in requirements.get("nested", {}).items():
            if nested_section in current:
                nested_path = f"{section_path}.{nested_section}" if section_path else nested_section
                self._validate_config_section(nested_path, nested_reqs)

    @staticmethod
    def _validate_checks(checks_config):
        """Special validation for checks section"""
        CHECK_REQUIREMENTS = {
            "null_check": {"required": ["columns", "threshold"], "threshold": ["max_null_percentage"]},
            "pii_check": {"required": []},
            "row_count_check": {"required": ["threshold"], "threshold": ["expected_range"]},
            "custom_sql_check": {"required": ["query", "threshold"], "threshold": ["acceptable_condition"]},
            "freshness_check": {"required": ["expected_refresh_schedule", "time_tolerance_minutes"]}
        }
        allowed_freshness_modes = {'checksum', 'update_column'}
        for i, check in enumerate(checks_config, 1):
            check_name = check.get("name")
            if not check_name:
                raise InvalidChecksError(f"Name is not defined in config for check {i}!")

            if check_name not in CHECK_REQUIREMENTS:
                raise InvalidChecksError(f"{check_name} is not valid, please check the allowed check names!")

            # Validate common fields
            common_fields = ["database", "schema", "table"]
            for field in common_fields:
                if field not in check:
                    raise InvalidChecksError(f"{field} is missing or misspelt for {check_name} in config!")

            # Validate type-specific fields
            for field in CHECK_REQUIREMENTS[check_name]["required"]:
                if field not in check:
                    raise InvalidChecksError(f"{field} is missing or misspelt for {check_name} in config!")

            # Validate threshold fields if present
            if "threshold" in CHECK_REQUIREMENTS[check_name]:
                for field in CHECK_REQUIREMENTS[check_name]["threshold"]:
                    if field not in check["threshold"]:
                        raise InvalidChecksError(
                            f"{field} is missing or misspelt in threshold section for {check_name} in config!")

            if check_name == 'freshness_check':
                polling_modes = check.get("polling_modes")
                if polling_modes is None:
                    print(f"Polling modes is missing or misspelt for {check_name} in config! {check_name} will default to polling based on row count..")
                else:
                    modes = [item if isinstance(item, str) else list(item.keys())[0] for item in polling_modes]
                    if not all(item in allowed_freshness_modes for item in modes):
                        raise InvalidChecksError(
                                f"Polling modes has a key that is not supported for {check_name} in config!")

    @staticmethod
    def _validate_rule_mining(rule_mining_config):
        """Special validation for rule_mining section"""
        # Validate enabled field is boolean
        if not isinstance(rule_mining_config.get("enabled"), bool):
            raise ConfigValidationError("rule_mining.enabled must be a boolean value")
        
        # Validate intensity field has valid values
        valid_intensities = ["low", "medium", "high"]
        intensity = rule_mining_config.get("intensity")
        if intensity not in valid_intensities:
            raise ConfigValidationError(f"rule_mining.intensity must be one of {valid_intensities}, got '{intensity}'")
        
        # Validate enabled_checks is a list and contains valid check types
        enabled_checks = rule_mining_config.get("enabled_checks")
        if not isinstance(enabled_checks, list):
            raise ConfigValidationError("rule_mining.enabled_checks must be a list")
        
        if not enabled_checks:
            raise ConfigValidationError("rule_mining.enabled_checks cannot be empty")
        
        # Define valid rule mining check types
        valid_rule_mining_checks = [
            "null_check",
            "row_count_check",
            "data_type_check",
            "pattern_check",
            "range_check",
            "uniqueness_check"
        ]
        
        for check in enabled_checks:
            if check not in valid_rule_mining_checks:
                raise ConfigValidationError(
                    f"'{check}' is not a valid rule mining check. "
                    f"Valid checks are: {valid_rule_mining_checks}"
                )

    def _validate_yaml_config(self):
        """Main validation function - enhanced to handle special validation functions"""
        
        # Validate top-level sections based on REQUIRED_STRUCTURE
        for section, requirements in self.REQUIRED_STRUCTURE.items():
            if section in self._config:
                validation_func_name = requirements.get("validation_function")
                if validation_func_name:
                    validation_func = getattr(self, f"_{validation_func_name}")
                    validation_func(self._config[section])
                
                if "required_keys" in requirements:
                    self._validate_config_section(section, requirements)
            else:
                if section != "rule_mining":  # 'rule_mining' is optional
                    raise MissingSectionError(section)

        # Validate optional sections: audit, alerts, profiling, data_source.connection 
        self._validate_audit_section()
        self._validate_alerts_section()
        self._validate_profiling_section()
        self._validate_data_source()


    def _validate_audit_section(self):
        if 'audit' not in self._config:
            return

        audit = self._config['audit']
        self._check_required_keys("audit", audit, ['enabled', 'database'])

        database = audit.get('database', {})
        self._check_required_keys("audit.database", database, ['type', 'connection'])

        connection = database.get('connection', {})
        self._check_required_keys("audit.database.connection", connection, ['host', 'port', 'database', 'user', 'password'])


    def _validate_alerts_section(self):
        if 'alerts' not in self._config:
            return

        alerts = self._config['alerts']
        self._check_required_keys("alerts", alerts, ['enabled', 'channels'])

        if not alerts.get('channels'):
            raise MissingSectionError("alerts.channels")

        for channel in alerts['channels']:
            if 'type' not in channel:
                raise MissingSectionError("alerts.channels.type")

            if channel['type'] == 'email':
                if not channel.get('recipients'):
                    raise MissingSectionError("alerts.channels.email.recipients")

            elif channel['type'] == 'slack':
                webhook = channel.get('slack_webhook', {})
                if not webhook or 'environment' not in webhook or 'url' not in webhook:
                    raise MissingSectionError("alerts.channels.slack.slack_webhook.environment or url")
                if 'channel_name' not in channel:
                    raise MissingSectionError("alerts.channels.slack.channel_name")


    def _validate_profiling_section(self):
        if 'profiling' not in self._config:
            return

        profiling = self._config['profiling']
        self._check_required_keys("profiling", profiling, ['profiling_schema', 'profiling_database'])


    def _validate_data_source(self):
        """validation for data_source.connection environment configs"""
        env_required_keys = {
            'secrets_manager': ['username', 'password', 'host', 'dbname', 'port', 'region'],
            'env_variable': ['user', 'password', 'host', 'database', 'port'],
        }

        connection_config = self._config.get('data_source', {}).get('connection', {})
        environment = connection_config.get('environment')

        if not environment:
            return

        if environment not in env_required_keys:
            raise ConfigValidationError(
                f"data_source.connection.environment value '{environment}' is not supported"
            )

        self._check_required_keys("data_source.connection", connection_config, env_required_keys[environment])


    def _check_required_keys(self, base_path: str, config_section: dict, required_keys: list):
        """Generic helper to check for required keys in a config section"""
        for key in required_keys:
            if key not in config_section:
                raise MissingSectionError(f"{base_path}.{key}")

    def is_rule_mining_enabled(self) -> bool:
        """Check if rule mining is enabled in the current configuration"""
        if self._config and 'rule_mining' in self._config:
            return self._config['rule_mining'].get('enabled', False)
        return False

    def get_rule_mining_config(self) -> Dict:
        """Get rule mining specific configuration"""
        if self._config and 'rule_mining' in self._config:
            return self._config['rule_mining']
        return {}

    def update_config_section(self, section_path: str, new_data: Dict):
        """Update a specific section of the configuration"""
        if self._config is None:
            self._config = {}
        
        # Navigate to the section and update
        current = self._config
        path_parts = section_path.split('.')
        
        # Navigate to parent of target section
        for part in path_parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        # Update the target section
        current[path_parts[-1]] = new_data
        
        # Re-validate the entire configuration
        self._validate_yaml_config()



