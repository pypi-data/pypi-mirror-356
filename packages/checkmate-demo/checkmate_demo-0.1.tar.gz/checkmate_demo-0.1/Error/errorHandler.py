# config_errors.py

class ConfigError(Exception):
    """Base class for all config-related exceptions."""
    pass

class ConfigLoadError(ConfigError):
    def __init__(self, message="Failed to load the configuration file"):
        super().__init__(f"ConfigLoadError: {message}")

class ConfigValidationError(ConfigError):
    def __init__(self, message="Configuration validation failed"):
        super().__init__(f"ConfigValidationError: {message}")

class MissingSectionError(ConfigValidationError):
    def __init__(self, section):
        super().__init__(f"Missing required section: '{section}'")

class InvalidDataSourceError(ConfigValidationError):
    def __init__(self):
        super().__init__("Invalid or missing fields in 'data_source' section")

class InvalidChecksError(ConfigValidationError):
    def __init__(self,error_string):
        super().__init__(error_string)

class NotifyValidationError(ConfigValidationError):
    def __init__(self):
        super().__init__("The 'alerts.notify_on' field must be a list.")

class ChannelValidationError(ConfigValidationError):
    def __init__(self):
        super().__init__("The 'alerts.channels' field must be a list.")

class EnabledValidationError(ConfigValidationError):
    def __init__(self):
        super().__init__("The 'alerts.enabled' field must be a boolean.")

class ThresholdConfigValidationError(ConfigValidationError):
    def __init__(self):
        super().__init__("No threshold config found for check '{check_name}' and column '{column}'")

class DatabaseOperationError(ConfigError):
    def __init__(self, message="Database operation failed"):
        super().__init__(f"DatabaseOperationError: {message}")

class NotificationError(Exception):
    """Raised when there's an error sending notifications"""
    def __init__(self, message: str):
        super().__init__(message)

   
