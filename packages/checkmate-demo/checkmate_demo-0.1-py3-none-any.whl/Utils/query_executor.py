# Placeholder for query_executor.py
from jinja2 import Environment, FileSystemLoader
import os
from typing import Dict, List
from .sql_helpers import quote_if_reserved

class QueryExecutor:
    def __init__(self, connector, db_type: str, config: Dict):
        self.connector = connector
        self.db_type = db_type
        self.config = config
        
        # Setup template environment with fallback
        template_paths = [
            os.path.join("templates", db_type),
            os.path.join("templates", "common")
        ]
        self.env = Environment(
            loader=FileSystemLoader(template_paths),
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    ''' def render_query(self, template_name: str, context: Dict) -> str:
        """  Process column names before rendering """
        if 'column_name' in context:
            context['column_name'] = quote_if_reserved(context['column_name'])
       
        """Render SQL template with context"""
        template = self.env.get_template(template_name)
        return template.render(context)
     '''
    def render_query(self, template_name: str, context: Dict) -> str:
        """Process column names before rendering"""
        if 'column_name' in context:
            context['column_name'] = quote_if_reserved(context['column_name'])
        
        # Add database name to context if available
        if 'database_name' not in context and 'database' in self.config:
            context['database_name'] = self.config['database']
        
        """Render SQL template with context"""
        template = self.env.get_template(template_name)
        return template.render(context)
    
    def execute(self, query: str) -> List[Dict]:
        """Execute query and return results"""
        return self.connector.run_query(query)
