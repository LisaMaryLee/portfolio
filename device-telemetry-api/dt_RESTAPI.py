#!/usr/bin/env python3

"""
Device Telemetry REST API

This API collects and stores anonymized telemetry data from storage appliances. 
It supports multiple dynamic endpoints based on table definitions and allows 
data ingestion with custom runtime validation and error simulation for testing.
"""

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_restx import Api, Resource, fields
import mysql.connector
from werkzeug.exceptions import BadRequest
from config import Config
from table_definitions import columns, table_config, models
from sql_queries import get_insert_query, get_insert_or_replace_query

# Initialize Flask application
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Configure Swagger API documentation
api = Api(
    app,
    version='1.0',
    title='Device Telemetry API',
    description='REST API for collecting and storing anonymized telemetry data from storage appliances.'
)

# Define a namespace for telemetry-related routes
ns = api.namespace('telemetry', description='Endpoints for ingesting device telemetry')

# Register Swagger models for each telemetry table
for table_name, model in models.items():
    ns.models[table_name] = api.model(table_name, model)

# Base class for handling telemetry data ingestion
class SaveData(Resource):
    def __init__(self, table_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table_name = table_name
        self.columns = columns[table_name]
        self.query_func = get_insert_query if table_config[table_name] == 'insert' else get_insert_or_replace_query

    @ns.response(200, 'Success')
    @ns.response(201, 'Data saved successfully')
    @ns.response(202, 'Accepted')
    @ns.response(204, 'No Content')
    @ns.response(400, 'Invalid JSON format or Missing key')
    @ns.response(401, 'Unauthorized')
    @ns.response(403, 'Forbidden')
    @ns.response(404, 'Not Found')
    @ns.response(409, 'Conflict: Duplicate entry')
    @ns.response(500, 'Internal Server Error')
    def post(self):
        """
        Handle POST requests for ingesting data into the specified table.
        Validates the request payload, simulates common errors, and inserts data into MySQL.
        """

        # Mock 401 Unauthorized
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header != "Bearer valid_token":
            return make_response(jsonify({"error": "Unauthorized"}), 401)

        # Mock 403 Forbidden
        if request.headers.get("X-Permissions") == "none":
            return make_response(jsonify({"error": "Forbidden"}), 403)

        # Parse and validate JSON input
        try:
            data = request.get_json(force=True)

            if not isinstance(data, dict):
                raise TypeError("Payload is not a valid JSON object")

        except BadRequest as e:
            return make_response(jsonify({"error": f"Malformed JSON: {str(e)}"}), 400)
        except TypeError as e:
            return make_response(jsonify({"error": f"Invalid JSON format: {str(e)}"}), 400)
        except Exception as e:
            return make_response(jsonify({"error": f"Unexpected error: {str(e)}"}), 500)

        # Simulate server error for testing
        if "bad_column" in data:
            raise mysql.connector.Error("Simulated internal server error")

        # Ensure payload contains exact expected keys
        if set(data.keys()) != set(self.columns):
            return make_response(jsonify({"error": "Payload keys mismatch"}), 400)

        # Manual runtime type checking based on model field types
        for field, value in data.items():
            expected_field = ns.models[self.table_name][field]
            if isinstance(expected_field, fields.String):
                if not isinstance(value, str):
                    return make_response(jsonify({"error": f"Wrong type for field '{field}', expected string"}), 400)
            elif isinstance(expected_field, fields.Integer):
                if not isinstance(value, int):
                    return make_response(jsonify({"error": f"Wrong type for field '{field}', expected integer"}), 400)

        # Prepare and execute SQL insert or replace
        values = tuple(data[col] for col in self.columns)
        query = self.query_func(self.table_name, self.columns)

        try:
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
            if "Duplicate entry" in str(err):
                return make_response(jsonify({"error": f"Conflict: {str(err)}"}), 409)
            return make_response(jsonify({"error": str(err)}), 500)

        return make_response(jsonify({"message": "Data saved successfully"}), 201)

# Factory function to create per-table resource classes dynamically
def create_resource(table_name):
    class TableSpecificSaveData(SaveData):
        def __init__(self, *args, **kwargs):
            super().__init__(table_name, *args, **kwargs)

        @ns.expect(ns.models[table_name], validate=False)
        @ns.response(200, 'Success')
        @ns.response(201, 'Data saved successfully')
        @ns.response(202, 'Accepted')
        @ns.response(204, 'No Content')
        @ns.response(400, 'Invalid JSON format or Missing key')
        @ns.response(401, 'Unauthorized')
        @ns.response(403, 'Forbidden')
        @ns.response(404, 'Not Found')
        @ns.response(409, 'Conflict: Duplicate entry')
        @ns.response(500, 'Internal Server Error')
        def post(self):
            return super().post()

    TableSpecificSaveData.__name__ = f"Save{table_name.capitalize()}"
    return TableSpecificSaveData

# Dynamically register routes for each telemetry table
for table_name in columns.keys():
    api.add_resource(create_resource(table_name), f'/{table_name}', endpoint=table_name)

# Register read-only viewer routes if defined
from viewer_route import register_viewer_routes
register_viewer_routes(app)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
