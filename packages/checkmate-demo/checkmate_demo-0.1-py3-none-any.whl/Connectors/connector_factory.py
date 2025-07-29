from Connectors.redshift_connector import RedshiftConnector
from Connectors.rds_connector import RDSConnector
from logger.custom_logs import LoggerConfigurator

logger_configurator = LoggerConfigurator()
logger = logger_configurator.get_logger()

class ConnectorFactory:
    CONNECTOR_MAP = {
        "redshift": RedshiftConnector,
        "rds": RDSConnector
    }

    @staticmethod
    def get_connector(config: dict, usage: str = 'none'):
        if usage == 'audit':
            if not config.get('audit', {}).get('enabled', False):
                print("Audit is disabled.")
                return None
            conn_config = config['audit']['database']
        else:
            conn_config = config['data_source']
        conn_type = conn_config['type']
        connector_class = ConnectorFactory.CONNECTOR_MAP.get(conn_type.lower())
        logger.info(f'{conn_type} has been selected for {usage} based on details in config YAML.')
        if not connector_class:
            raise ValueError(f"Unsupported connector type: {conn_type}")
        return connector_class(config, usage=usage)

