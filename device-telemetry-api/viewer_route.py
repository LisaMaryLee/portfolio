from flask import Flask, render_template_string, request
import mysql.connector
from table_definitions import models, columns
from config import Config

# HTML template for rendering the database viewer
# Uses Jinja2 templating to dynamically populate a dropdown and data table
viewer_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Database Viewer</title>
    <style>
        body { font-family: sans-serif; margin: 40px; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background-color: #f5f5f5; }
    </style>
</head>
<body>
    <h2>📋 Select a table to view:</h2>
    <form method="get">
        <select name="table" onchange="this.form.submit()">
            <option value="">-- Choose a table --</option>
            {% for t in tables %}
                <option value="{{t}}" {% if t == selected %}selected{% endif %}>{{t}}</option>
            {% endfor %}
        </select>
    </form>

    {% if headers and rows %}
        <h3>Showing last 20 rows from <code>{{selected}}</code></h3>
        <table>
            <thead>
                <tr>{% for col in headers %}<th>{{col}}</th>{% endfor %}</tr>
            </thead>
            <tbody>
                {% for row in rows %}
                <tr>{% for col in row %}<td>{{col}}</td>{% endfor %}</tr>
                {% endfor %}
            </tbody>
        </table>
    {% elif selected %}
        <p><em>No data found in this table.</em></p>
    {% endif %}
</body>
</html>
"""

# Register the viewer route to allow viewing contents of telemetry tables
def register_viewer_routes(app: Flask):
    @app.route("/viewer")
    def viewer():
        # Get the selected table from the query string
        selected = request.args.get("table")

        # Initialize rendering context
        data = {
            "tables": list(models.keys()),  # All available table names
            "headers": None,                # Column headers for the selected table
            "rows": None,                   # Table content rows
            "selected": selected            # Currently selected table name
        }

        # If a valid table was selected, connect to the DB and query it
        if selected and selected in columns:
            try:
                # Connect to MySQL using application config
                connection = mysql.connector.connect(
                    host=Config.MYSQL_HOST,
                    user=Config.MYSQL_USER,
                    password=Config.MYSQL_PASSWORD,
                    database=Config.MYSQL_DB
                )
                cursor = connection.cursor()

                # Compose SQL query to fetch the latest 20 rows ordered by the first column
                field_list = ", ".join(columns[selected])
                cursor.execute(
                    f"SELECT {field_list} FROM {selected} "
                    f"ORDER BY {columns[selected][0]} DESC LIMIT 20"
                )

                # Populate the context data with query results
                data["rows"] = cursor.fetchall()
                data["headers"] = columns[selected]

                # Clean up
                cursor.close()
                connection.close()
            except Exception as e:
                # If query fails, show the error message instead of table data
                data["headers"] = ["Error"]
                data["rows"] = [[str(e)]]

        # Render the HTML viewer with current data context
        return render_template_string(viewer_template, **data)
