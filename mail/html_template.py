from mail import style


def base_html(body, style):
    return f"""
    <html>
        <head>
            <style>
                {style}
            </style>
        </head>
        <body>
            <div class="container">
                {body}
                <p>Best regards,<br>Your Algo Trading</p>
            </div>
        </body>
    </html>
    """


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


def error_template(error_details, traceback_details):
    body = f"""
        <h1>Error Report</h1>
        <p>An error has occurred in the system. Below are the details:</p>
        <h2>Error Details</h2>
        <div class="error-details">
            <strong>{error_details['type']}</strong>: {error_details['message']}
        </div>
        <h2>Traceback</h2>
        <div class="traceback-details">
            {traceback_details}
        </div>
        <p>Please address this issue as soon as possible.</p>
    """
    return base_html(body, style.error)


def table_with_two_columns(key_value_pairs, notification_heading):
    body = f"""
        <h1>{notification_heading}</h1>
        {table_with_two_columns_body(key_value_pairs)}
    """
    return base_html(body=body, style=style.table + " " + style.trading_stop)


def multiple_table(details, notification_heading):
    return base_html(
        body=f"""
        <h1>{notification_heading}</h1>
        <div>
            {"".join([f"<h4>{d['heading']}</h4> {table_with_two_columns_body(d['key_value'])}" for d in details])}
        </div>
        """,
        style=style.table + " " + style.trading_stop
    )


def trading_stop():
    return base_html(
        body=f"""
        <h1>Trading Stopped</h1>
        <p>The trading script has stopped running due to the following reason:</p>
        <div class="reason">
            <ul>
                <li>Current time is outside market hours.</li>
                <li>Multiple failed login attempts detected on Kite web platform.</li>
                <li>An error occurred during script execution.</li>
            </ul>
        </div>
        <p>Please take appropriate action to resolve this issue.</p>
        """,
        style=style.trading_stop,
    )
