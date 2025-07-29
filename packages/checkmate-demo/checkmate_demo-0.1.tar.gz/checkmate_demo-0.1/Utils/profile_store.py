
import json
from datetime import datetime
from typing import Dict, Optional
from tabulate import tabulate
from decimal import Decimal

def save_profile(profile: Dict, filename: str):
    """Save profile with timestamp"""
    full_profile = {
        "metadata": {
            "generated_at": datetime.utcnow().isoformat(),
            "database": profile.get("database", "unknown")
        },
        "results": profile
    }
    with open(filename, "w") as f:
        json.dump(full_profile, f, indent=2)

def load_profile(filename: str) -> Dict:
    """Load saved profile"""
    with open(filename, "r") as f:
        return json.load(f)

def run_profiling(profiler, config):
    """Executes profiling with configuration from YAML"""
    profiling_config = config.get('profiling', {})
    database = profiling_config['profiling_database']
    schema = profiling_config['profiling_schema']

    # Get tables (support both string and list)
    tables = None
    if 'table' in profiling_config:
        tables = [profiling_config['table']]
    elif 'table_list' in profiling_config:
        tables = profiling_config['table_list']

    # Get columns (support both string and list)
    columns = None
    if 'column' in profiling_config:
        columns = [profiling_config['column']]
    elif 'column_list' in profiling_config:
        columns = profiling_config['column_list']

    # Prepare arguments with mandatory database and schema
    profile_args = {
        'database': database,
        'schema': schema
    }
    if tables:
        profile_args['tables'] = tables
    if columns:
        profile_args['columns'] = columns

    return profiler.profile(**profile_args)

def decimal_to_float(obj):
    """Convert Decimal objects to float for JSON serialization."""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def print_table_profile(table_name: str, table_data: dict):
    """Print column stats for a single table in tabular format."""
    print('Printing Profiling results...\n')
    columns = table_data["columns"]
    rows = []
    
    for col_name, stats in columns.items():
        # Handle nested metrics (e.g., avg_length)
        extra_metrics = {}
        for k, v in stats.items():
            if k not in ["data_type", "is_nullable", "non_null_count", "null_count"]:
                extra_metrics[k] = v
        
        rows.append([
            col_name,
            stats["data_type"],
            stats["is_nullable"],
            stats["non_null_count"],
            stats["null_count"],
            json.dumps(extra_metrics, default=decimal_to_float, indent=2) if extra_metrics else "N/A"
        ])
    
    print(f"\n[Table: {table_name}]")
    print(f"Schema: {table_data['schema']} | Rows: {table_data['row_count']}\n")
    print(tabulate(
        rows,
        headers=["Column", "Data Type", "Nullable?", "Non-Null", "Nulls","Additional Stats"],
        tablefmt="grid",
        maxcolwidths=[None, None, None, None, None, 20]  # Limit width of JSON
    ))

def compare_profiles(current: Dict, baseline: Dict) -> Dict:
    """Compare two profile runs"""
    comparison = {}
    for table_name, table_data in current.get("results", {}).items():
        if table_name not in baseline.get("results", {}):
            comparison[table_name] = {"status": "new_table"}
            continue
            
        table_comparison = {}
        base_table = baseline["results"][table_name]
        
        # Compare row counts
        if "row_count" in table_data and "row_count" in base_table:
            delta = table_data["row_count"] - base_table["row_count"]
            pct_change = (delta / base_table["row_count"]) * 100 if base_table["row_count"] else None
            table_comparison["row_count"] = {
                "current": table_data["row_count"],
                "baseline": base_table["row_count"],
                "delta": delta,
                "pct_change": pct_change
            }
        
        # Compare columns
        table_comparison["columns"] = {}
        for col_name, col_data in table_data.get("columns", {}).items():
            if col_name not in base_table.get("columns", {}):
                table_comparison["columns"][col_name] = {"status": "new_column"}
                continue
                
            col_comparison = {}
            base_col = base_table["columns"][col_name]
            
            for metric, value in col_data.items():
                if metric in base_col and isinstance(value, (int, float)):
                    delta = value - base_col[metric]
                    pct_change = (delta / base_col[metric]) * 100 if base_col[metric] else None
                    col_comparison[metric] = {
                        "current": value,
                        "baseline": base_col[metric],
                        "delta": delta,
                        "pct_change": pct_change
                    }
            
            table_comparison["columns"][col_name] = col_comparison
        
        comparison[table_name] = table_comparison
    
    return comparison