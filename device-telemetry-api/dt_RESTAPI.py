from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_restx import Api, Resource, fields
import mysql.connector
from config import Config
from table_definitions import columns, table_config, models
from sql_queries import get_insert_query, get_insert_or_replace_query
from werkzeug.exceptions import BadRequest

app = Flask(__name__)
api = Api(
    app,
    version='1.0',
    title='Device Telemetry API',
    description='REST API for collecting and storing anonymized telemetry data from storage appliances.'
)

app.config.from_object(Config)
CORS(app)

# Define namespace
ns = api.namespace('telemetry', description='Endpoints for ingesting device telemetry')

# Register all models with the namespace
for table_name, model in models.items():
    ns.models[table_name] = api.model(table_name, model)

class SaveData(Resource):
    def __init__(self, table_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table_name = table_name
        self.columns = columns[table_name]
        self.query_func = get_insert_query if table_config[table_name] == 'insert' else get_insert_or_replace_query

    @ns.expect(ns.models[table_name])
    @ns.response(200, 'Success')
    @ns.response(201, 'Data saved successfully')
    @ns.response(400, 'Invalid JSON format or Missing key or Wrong type')
    @ns.response(401, 'Unauthorized')
    @ns.response(403, 'Forbidden')
    @ns.response(404, 'Not Found')
    @ns.response(500, 'Internal Server Error')
    def post(self):
        # Simulate 401 Unauthorized
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header != "Bearer valid_token":
            return make_response(jsonify({"error": "Unauthorized"}), 401)

        # Simulate 403 Forbidden
        if request.headers.get("X-Permissions") == "none":
            return make_response(jsonify({"error": "Forbidden"}), 403)

        # Try parsing the JSON safely
        try:
            data = request.get_json(force=True)
        except BadRequest:
            return make_response(jsonify({"error": "Malformed JSON"}), 400)

        # Check for missing keys
        if not all(k in data for k in self.columns):
            return make_response(jsonify({"error": "Missing key(s) in JSON payload"}), 400)

        # Check for type mismatch manually
        model_schema = ns.models[self.table_name]
        for field_name, field_type in model_schema.items():
            if field_name not in data:
                continue
            expected_type = field_type.__class__.__name__
            value = data[field_name]
            if expected_type == "Integer" and not isinstance(value, int):
                return make_response(jsonify({"error": f"Invalid type for '{field_name}', expected integer"}), 400)
            if expected_type == "String" and not isinstance(value, str):
                return make_response(jsonify({"error": f"Invalid type for '{field_name}', expected string"}), 400)

        # Simulate 500 error
        if "bad_column" in data:
            return make_response(jsonify({"error": "Simulated internal server error"}), 500)

        # Prepare values
        values = tuple(data[col] for col in self.columns)

        # Execute insert
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
            return make_response(jsonify({"error": str(err)}), 500)

        return make_response(jsonify({"message": "Data saved successfully"}), 201)

# Create table-specific subclasses
def create_resource(table_name):
    class TableSpecificSaveData(SaveData):
        def __init__(self, *args, **kwargs):
            super().__init__(table_name, *args, **kwargs)

        @ns.expect(ns.models[table_name])
        def post(self):
            return super().post()

    TableSpecificSaveData.__name__ = f"Save{table_name.capitalize()}"
    return TableSpecificSaveData

# Register endpoints dynamically
for table_name in columns.keys():
    api.add_resource(create_resource(table_name), f'/{table_name}', endpoint=table_name)

# Register viewer routes if needed
from viewer_route import register_viewer_routes
register_viewer_routes(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
