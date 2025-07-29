from tabulate import tabulate
import datetime

def render_profiling_html(results: dict) -> str:
    run_id = results.get("run_id", "N/A")
    timestamp = results.get("timestamp", str(datetime.datetime.utcnow()))

    html_sections = []
    for table_key, table_info in results.get("results", {}).items():
        schema = table_info.get("schema", "N/A")
        table_name = table_info.get("table", "N/A")
        row_count = table_info.get("row_count", "N/A")
        columns = table_info.get("columns", {})

        # Prepare tabular data
        table_data = []
        for col_name, stats in columns.items():
            table_data.append([
                col_name,
                stats.get("data_type", ""),
                stats.get("is_nullable", ""),
                stats.get("non_null_count", ""),
                stats.get("distinct_count", ""),
                stats.get("null_count", "")
            ])

        headers = ["Column Name", "Data Type", "Nullable", "Non-null Count", "Distinct Count", "Null Count"]
        html_table = tabulate(table_data, headers=headers, tablefmt="html")

        # Append section
        html_sections.append(f"""
            <h3>Schema: {schema} | Table: {table_name}</h3>
            <p><b>Row Count:</b> {row_count}</p>
            {html_table}
            <br/>
        """)

    # Full HTML Page
    full_html = f"""
    <html>
    <head>
        <title>Database Profiling Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; }}
            table {{ border-collapse: collapse; width: 100%; margin-top: 10px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; }}
            th {{ background-color: #f2f2f2; }}
            h2, h3 {{ color: #333; }}
        </style>
    </head>
    <body>
        <h2>Data Profiling Report</h2>
        <p><b>Run ID:</b> {run_id}</p>
        <p><b>Timestamp:</b> {timestamp}</p>
        {''.join(html_sections)}
    </body>
    </html>
    """
    return full_html
