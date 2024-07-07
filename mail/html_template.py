def base_html(body, style):
    return f"""<html>
            <head>
            <style>
            {style}
            </style>
            </head>
            <body>
            {body}
            </body>
            </html>"""


def table_with_two_columns_body(key_value_pairs):
    return f"""
        <table>
          <tr>
              <th>Parameter</th>
              <th>Value</th>
          </tr>
          {"".join(
              [
              f"<tr><td>{key.title().replace('_', ' ')}</td><td>{value}</td></tr>"
              for key, value in key_value_pairs.items()
              ]
          )}
        </table>
        """


def style_table():
    return f"""
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }}
        th, td {{
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }}
        th {{
            background-color: #007BFF;
            color: white;
            font-weight: 600;
            text-transform: uppercase;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        tr:hover {{
            background-color: #f1f1f1;
        }}
        th:first-child, td:first-child {{
            border-left: none;
        }}
        th:last-child, td:last-child {{
            border-right: none;
        }}
        td {{
            color: #333;
        }}
    """


def table_with_two_columns(key_value_pairs):
    return base_html(
        body=table_with_two_columns_body(key_value_pairs), style=style_table()
    )


def multiple_table(details):
    return base_html(
        body=f"""
        <div>
            {"".join([f"<h4>{d['heading']}</h4> {table_with_two_columns_body(d['key_value'])}" for d in details])}
        </div>
        """,
        style=style_table(),
    )
