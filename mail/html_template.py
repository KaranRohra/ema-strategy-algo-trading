def table_with_two_columns(key_value_pairs):
    return f"""<html>
            <head>
            <style>
            table {{
                border-collapse: collapse;
                width: 100%;
            }}
            th, td {{
                border: 1px solid black;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            </style>
            </head>
            <body>
            <table>
            <tr>
                <th>Parameter</th>
                <th>Value</th>
            </tr>
            {"".join(
                [
                f"<tr><td>{key.title().replace('_', ' ')}</td><td>{str(value).title().replace('_', ' ')}</td></tr>"
                for key, value in key_value_pairs.items()
                ]
            )}
            </table>
            </body>
            </html>"""
