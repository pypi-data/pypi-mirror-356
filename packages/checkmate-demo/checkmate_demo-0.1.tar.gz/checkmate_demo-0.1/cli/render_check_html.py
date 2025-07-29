from tabulate import tabulate

def render_check_result_html(results: list) -> str:
    if not results:
        return "<p>No results found.</p>"

    # Build table rows
    table_data = []
    for result in results:
        table_data.append([
            result.get("check_name", "N/A"),
            result.get("database", "N/A"),
            result.get("schema", "N/A"),
            result.get("table", "N/A"),
            result.get("column", "N/A"),
            f"{result.get('null_percentage', 'N/A')}%",
            result.get("timestamp", "N/A"),
            result.get("run_id", "N/A"),
        ])

    headers = ["Check", "Database", "Schema", "Table", "Column", "Null %", "Timestamp", "Run ID"]
    html_table = tabulate(table_data, headers=headers, tablefmt="html")

    html_content = f"""
    <html>
    <head>
        <title>Data Quality Check Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; }}
            table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: center; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h2>Data Quality Check Results</h2>
        {html_table}
    </body>
    </html>
    """
    return html_content
