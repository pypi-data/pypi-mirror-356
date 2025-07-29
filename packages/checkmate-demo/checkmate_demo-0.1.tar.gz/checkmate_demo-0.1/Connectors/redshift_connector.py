from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
from Connectors.base import BaseConnector
from Connectors.credential_manager import CredentialManager
from logger.custom_logs import LoggerConfigurator
import time
from functools import wraps

# Configure logger
logger_configurator = LoggerConfigurator()
logger = logger_configurator.get_logger()

def retry_db_operation(max_retries=3, base_delay=1, backoff_factor=2):
    """
    Decorator to retry database operations with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay between retries in seconds
        backoff_factor: Multiplier for delay after each retry
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries + 1):  # +1 for initial attempt
                try:
                    return func(self, *args, **kwargs)
                except Exception as e:
                    last_exception = e
                    
                    if attempt == max_retries:
                        # Final attempt failed, raise the exception
                        logger.error(f"Final retry attempt failed for {func.__name__}: {str(e)}")
                        raise e
                    
                    # Calculate delay with exponential backoff
                    delay = base_delay * (backoff_factor ** attempt)
                    logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {str(e)}. Retrying in {delay} seconds...")
                    time.sleep(delay)
            
            # This should never be reached, but just in case
            raise last_exception
        return wrapper
    return decorator


class RedshiftConnector(BaseConnector):

    def __init__(self, config: dict, usage: str):

        self.config = config
        self.engine = None
        self.usage = usage

    def _get_credentials(self,config):
        try:
            self.credential_manager = CredentialManager(config['data_source'])
            creds = self.credential_manager.get_db_credentials()
            return creds
        except Exception as e:
            logger.error(f"Error getting Redshift credentials: {str(e)}")
            raise e

    @retry_db_operation(max_retries=3, base_delay=1, backoff_factor=2)
    def connect(self):
        try:
            creds = self._get_credentials(self.config)
            conn_str = (
                f"postgresql+psycopg2://{creds['username']}:{creds['password']}"
                f"@{creds['host']}:{creds['port']}/{creds['dbname']}"
            )
            self.engine = create_engine(conn_str, poolclass=QueuePool, pool_size=5, max_overflow=10)
            return self.engine
        except Exception as e:
            logger.error(f"Error connecting to Redshift: {str(e)}")
            raise e

    @retry_db_operation(max_retries=3, base_delay=1, backoff_factor=2)    
    def run_query(self, query: str) -> list[dict]:
        try:
            if not self.engine:
                self.connect()
            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                return [dict(row._mapping) for row in result]  # Convert to dicts
        except Exception as e:
            logger.error(f"Error running query: {str(e)}")
            raise e

    @retry_db_operation(max_retries=3, base_delay=1, backoff_factor=2)  
    def run_query_batch(self, query: str, batch_size: int = 1000):
        """
        Generator that yields batches of rows (list of dicts).
        """
        try:
            if not self.engine:
                self.connect()
            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                cursor = result.cursor  # raw DBAPI cursor

                # Get column names
                columns = [col[0] for col in cursor.description]

                while True:
                    rows = cursor.fetchmany(batch_size)
                    if not rows:
                        break
                    yield [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            logger.error(f"Error running query: {str(e)}")
            raise e
    
    @retry_db_operation(max_retries=3, base_delay=1, backoff_factor=2)
    def execute_non_query(self, query: str):
        try:
            if not self.engine:
                self.connect()
            with self.engine.connect() as conn:
                with conn.begin():
                    conn.execute(text(query))
        except Exception as e:
            logger.error(f"Error running query: {str(e)}")
            raise e
        
    @retry_db_operation(max_retries=3, base_delay=1, backoff_factor=2)    
    def execute_insert_query(self, query: str, params: dict = None):
        try:
            if not self.engine:
                self.connect()
            with self.engine.connect() as conn:
                with conn.begin():
                    conn.execute(text(query), params or {})
        except Exception as e:
            print(e)
            raise e
