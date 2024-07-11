error = f"""
    body {{
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #333;
        background-color: #f9f9f9;
        margin: 0;
        padding: 20px;
    }}
    .container {{
        max-width: 600px;
        margin: auto;
        background-color: #fff;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }}
    h1 {{
        color: #d9534f;
        font-size: 24px;
        border-bottom: 2px solid #d9534f;
        padding-bottom: 10px;
    }}
    h2 {{
        font-size: 20px;
        color: #007BFF;
        margin-top: 20px;
    }}
    p {{
        line-height: 1.6;
    }}
    .error-details {{
        background-color: #f8d7da;
        color: #721c24;
        padding: 15px;
        border-left: 5px solid #f5c6cb;
        margin-bottom: 20px;
        border-radius: 4px;
    }}
    .traceback-details {{
        background-color: #e9ecef;
        color: #495057;
        padding: 15px;
        border-left: 5px solid #ced4da;
        border-radius: 4px;
        white-space: pre-wrap;
        font-family: 'Courier New', Courier, monospace;
    }}    
"""

table = f"""
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

trading_stop = f"""
   body {{
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #333;
        background-color: #f9f9f9;
        margin: 0;
        padding: 20px;
    }}
    .container {{
        max-width: 600px;
        margin: auto;
        background-color: #fff;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }}
    h1 {{
        color: #007BFF;
        font-size: 24px;
        border-bottom: 2px solid #007BFF;
        padding-bottom: 10px;
    }}
    p {{
        line-height: 1.6;
    }}
    .reason {{
        background-color: #f8d7da;
        color: #721c24;
        padding: 15px;
        border-left: 5px solid #f5c6cb;
        margin-bottom: 20px;
        border-radius: 4px;
    }}
"""
