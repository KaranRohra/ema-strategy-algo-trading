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
          }}
          th, td {{
              border: 1px solid black;
              padding: 8px;
              text-align: left;
          }}
          th {{
              background-color: #f2f2f2;
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
