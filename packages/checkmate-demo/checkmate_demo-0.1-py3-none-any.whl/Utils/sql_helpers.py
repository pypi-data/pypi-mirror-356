# utils/sql_helpers.py
import re
from typing import Union

# Common SQL reserved keywords (add more as needed)
RESERVED_WORDS = {
    'constraint', 'select', 'insert', 'update', 'delete', 'where', 'group', 
    'by', 'order', 'having', 'limit', 'offset', 'join', 'as', 'on', 'in'
}

def quote_if_reserved(identifier: str) -> str:
    """Quote identifier if it's a reserved word or contains special characters"""
    # Check if it's a simple identifier (letters, numbers, underscore)
    is_simple = re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', identifier)
    
    if not is_simple or identifier.lower() in RESERVED_WORDS:
        return f'"{identifier}"'
    return identifier