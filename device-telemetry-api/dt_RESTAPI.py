#!/usr/bin/env python3

from flask import Flask, request, jsonify, make_response  # Flask core utilities
from flask_cors import CORS  # Enable CORS for client-side access
from flask_restx import Api, Resource, fields  # REST API framework with Swagger integration
import mysql.connector  # Connector for MySQL DB access
from config import Config  # Centralized configuration class with DB credentials
from table_definitions import columns, table_config, models  # Schema metadata
from sql_queries import get_insert_query, get_insert_or_replace_query  # SQL builders

# Initialize Flask and Flask-RESTX API
app = Flask(__name__)
api = Api(
    app,
    version='1.0',
    title='Device Telemetry API',
    description='REST API for collecting and storing anonymized telemetry data from storage appliances.'
)

# Load MySQL connection details from config
app.config.from_object(Config)

# Define namespace for endpoints
ns = api.namespace('telemetry', description='Endpoints for ingesting device telemetry')

# Register Swagger models
for table_name, model in models.items():
    ns.models[table_name] = api.model(table_name, model)

# Define base resource class for data ingestion
class SaveData(Resource):
    def __init__(self, table_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table_name = table_name
        self.columns = columns[table_name]
        self.query_func = get_insert_query if table_config[table_name] == 'insert' else get_insert_or_replace_query

    @ns.expect(ns.models[table_name], validate=True)
    @ns.response(200, 'Success')
    @ns.response(201, 'Data saved successfully')
    @ns.response(202, 'Accepted')
    @ns.response(204, 'No Content')
    @ns.response(400, 'Invalid JSON format or Missing key')
    @ns.response(401, 'Unauthorized')
    @ns.response(403, 'Forbidden')
    @ns.response(404, 'Not Found')
    @ns.response(500, 'Internal Server Error')
    def post(self):
        """
        Handle POST request for inserting or updating a row in the specified table.
        Validates input against required columns, schema model, and inserts data into the database.
        """
        try:
            data = request.get_json()

            # Reject unexpected or missing keys
            if set(data.keys()) != set(self.columns):
                extra = set(data.keys()) - set(self.columns)
                missing = set(self.columns) - set(data.keys())
                return make_response(jsonify({
                    "error": "Unexpected or missing keys in payload",
                    "extra_keys": list(extra),
                    "missing_keys": list(missing)
                }), 400)

            # Assemble tuple for query
            values = tuple(data[col] for col in self.columns)

        except KeyError as e:
            return make_response(jsonify({"error": f"Missing key: {str(e)}"}), 400)
        except TypeError:
            return make_response(jsonify({"error": "Invalid JSON format"}), 400)

        query = self.query_func(self.table_name, self.columns)

        try:
            # Connect and insert
            conn = mysql.connector.connect(
                host=app.config['MYSQL_HOST'],
                user=app.config['MYSQL_USER'],
                password=app.config['MYSQL_PASSWORD'],
                database=app.config['MYSQL_DB']
            )
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            return make_response(jsonify({"error": str(err)}), 500)

        return make_response(jsonify({"message": "Data saved successfully"}), 201)

# Factory to generate resource class per table dynamically
def create_resource(table_name):
    class TableSpecificSaveData(SaveData):
        def __init__(self, *args, **kwargs):
            super().__init__(table_name, *args, **kwargs)

        # Repeat responses for Swagger clarity
        @ns.expect(ns.models[table_name], validate=True)
        @ns.response(200, 'Success')
        @ns.response(201, 'Data saved successfully')
        @ns.response(202, 'Accepted')
        @ns.response(204, 'No Content')
        @ns.response(400, 'Invalid JSON format or Missing key')
        @ns.response(401, 'Unauthorized')
        @ns.response(403, 'Forbidden')
        @ns.response(404, 'Not Found')
        @ns.response(500, 'Internal Server Error')
        def post(self):
            return super().post()

    TableSpecificSaveData.__name__ = f"Save{table_name.capitalize()}"
    return TableSpecificSaveData

# Bind all table endpoints to /<table_name>
for table_name in columns.keys():
    api.add_resource(create_resource(table_name), f'/{table_name}', endpoint=table_name)

# Register web viewer route
from viewer_route import register_viewer_routes
register_viewer_routes(app)

# Entry point for running the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
