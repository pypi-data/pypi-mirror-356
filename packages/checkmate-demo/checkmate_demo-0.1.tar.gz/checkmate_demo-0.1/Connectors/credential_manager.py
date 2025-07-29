import os
import boto3
import json
from dotenv import load_dotenv
from logger.custom_logs import LoggerConfigurator
import time
from functools import wraps
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError, EndpointConnectionError


logger_configurator = LoggerConfigurator()
logger = logger_configurator.get_logger()

def retry_aws_operation(max_retries=3, base_delay=1, backoff_factor=2, jitter=True):
    """
    Decorator to retry AWS operations with exponential backoff and jitter.
    
    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay between retries in seconds
        backoff_factor: Multiplier for delay after each retry
        jitter: Add randomization to delay to prevent thundering herd
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            import random
            last_exception = None
            
            # AWS error codes that should NOT be retried
            non_retryable_errors = {
                'AccessDenied',
                'InvalidParameterException', 
                'InvalidParameterValue',
                'ResourceNotFoundException',
                'ValidationException',
                'DecryptionFailure',
                'InternalServiceError',
                'InvalidRequestException',
                'MalformedQueryString',
                'OptInRequired',
                'RequestExpired',
                'ServiceUnavailable',
                'UnauthorizedOperation'
            }
            
            for attempt in range(max_retries + 1):  # +1 for initial attempt
                try:
                    return func(self, *args, **kwargs)
                except ClientError as e:
                    error_code = e.response.get('Error', {}).get('Code', '')
                    last_exception = e
                    
                    # Don't retry certain error types
                    if error_code in non_retryable_errors:
                        logger.error(f"Non-retryable AWS error in {func.__name__}: {error_code} - {str(e)}")
                        raise e
                    
                    if attempt == max_retries:
                        logger.error(f"Final retry attempt failed for {func.__name__}: {error_code} - {str(e)}")
                        raise e
                    
                    # Calculate delay with exponential backoff and optional jitter
                    delay = base_delay * (backoff_factor ** attempt)
                    if jitter:
                        delay = delay * (0.5 + random.random() * 0.5)  # Add 0-50% jitter
                    
                    logger.warning(f"AWS operation attempt {attempt + 1} failed for {func.__name__}: {error_code} - {str(e)}. Retrying in {delay:.2f} seconds...")
                    time.sleep(delay)
                    
                except (NoCredentialsError, PartialCredentialsError) as e:
                    # Credential errors shouldn't be retried
                    logger.error(f"AWS credential error in {func.__name__}: {str(e)}")
                    raise e
                    
                except EndpointConnectionError as e:
                    last_exception = e
                    
                    if attempt == max_retries:
                        logger.error(f"Final retry attempt failed for {func.__name__} (connection error): {str(e)}")
                        raise e
                    
                    delay = base_delay * (backoff_factor ** attempt)
                    if jitter:
                        delay = delay * (0.5 + random.random() * 0.5)
                    
                    logger.warning(f"AWS connection attempt {attempt + 1} failed for {func.__name__}: {str(e)}. Retrying in {delay:.2f} seconds...")
                    time.sleep(delay)
                    
                except Exception as e:
                    last_exception = e
                    
                    if attempt == max_retries:
                        logger.error(f"Final retry attempt failed for {func.__name__}: {str(e)}")
                        raise e
                    
                    delay = base_delay * (backoff_factor ** attempt)
                    if jitter:
                        delay = delay * (0.5 + random.random() * 0.5)
                    
                    logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {str(e)}. Retrying in {delay:.2f} seconds...")
                    time.sleep(delay)
            
            # This should never be reached, but just in case
            raise last_exception
        return wrapper
    return decorator

class CredentialManager:

    def __init__(self, credential_config):
        self.config = credential_config

    def get_db_credentials(self):
        try:
            method = self.config['connection']['environment']
            db_type = self.config['type']
            logger.info(f"Getting {db_type} credentials from {method}..")
            if method == "env_variable":
                load_dotenv()
                return {
                    "host": os.getenv(self.config['connection']['host']),
                    "port": int(os.getenv(self.config['connection']['port'])),
                    "dbname": os.getenv(self.config['connection']['database']),
                    "username": os.getenv(self.config['connection']['user']),
                    "password": os.getenv(self.config['connection']['password']),
                }

            elif method == "secrets_manager":
                db_conn = self.config['connection']
                secret = self._get_secret_manager_creds(db_conn)
                return {
                    "username": secret[db_conn['username']],
                    "password": secret[db_conn['password']],
                    "host":secret[db_conn['host']],
                    "port":secret[db_conn['port']],
                    "dbname":secret[db_conn['dbname']]
                }
            else:
                raise ValueError(f"Unknown credential type: {method}")
        except Exception as e:
            print(e)
            raise e

    def get_smtp_credentials(self, channel_type='email'):
        """Get SMTP credentials from configured source"""
        try:
            smtp_config = None
            for channel in self.config['alerts']['channels']:
                if channel.get('type') == 'email' and 'sender_creds' in channel:
                    smtp_config = channel['sender_creds']
                    break
                
            if not smtp_config:
                raise ValueError("SMTP configuration not found in alerts channels")
                
            method = smtp_config['environment']
            logger.info(f"Getting SMTP credentials from {method}")
            
            if method == "env_variable":
                load_dotenv()
                return {
                    "server": os.getenv(smtp_config['server']),
                    "port": int(os.getenv(smtp_config['port'])),
                    "username": os.getenv(smtp_config['username']),
                    "password": os.getenv(smtp_config['password'])
                }
            elif method == "secrets_manager":
                secret = self._get_secret_manager_creds(smtp_config)
                return {
                    "server": secret[smtp_config['server']],
                    "port": int(secret[smtp_config['port']]),
                    "username": secret[smtp_config['username']],
                    "password": secret[smtp_config['password']]
                }
            else:
                raise ValueError(f"Unknown SMTP credential type: {method}")
        except Exception as e:
            print(f"Error getting SMTP credentials: {e}")
            raise e

    def get_slack_webhook_url(self, channel_type='slack'):
        """Get Slack webhook URL from configured source (env vars or Secrets Manager)"""
        try:
            # Look for Slack config in alerts channels
            slack_config = None
            if 'alerts' in self.config and 'channels' in self.config['alerts']:
                for channel in self.config['alerts']['channels']:
                    if channel.get('type') == 'slack' and 'slack_webhook' in channel:
                        slack_config = channel['slack_webhook']
                        break
                
            if not slack_config:
                raise ValueError("Slack configuration not found in credentials config")
                
            method = slack_config['environment']
            logger.info(f"Getting Slack webhook URL from {method}")
            
            if method == "env_variable":
                load_dotenv()
                return os.getenv(slack_config.get('url', 'SLACK_WEBHOOK_URL'))
            elif method == "secrets_manager":
                secret = self._get_secret_manager_creds(slack_config)
                return secret[slack_config.get('url', 'slack_webhook_url')]
            else:
                raise ValueError(f"Unknown Slack credential type: {method}")
        except Exception as e:
            print(f"Error getting Slack webhook URL: {e}")
            raise e

    @retry_aws_operation(max_retries=3, base_delay=1, backoff_factor=2, jitter=True)
    def _get_secret_manager_creds(self, config):
        """Helper method to get credentials from Secrets Manager"""
        try:
            secret_arn = config["secret_arn"]
            region = config["region"]
            client = boto3.client("secretsmanager", region_name=region)
            secret_value = client.get_secret_value(SecretId=secret_arn)
            return json.loads(secret_value["SecretString"])
        except Exception as e:
            print(f"Error retrieving from Secrets Manager: {e}")
            raise e