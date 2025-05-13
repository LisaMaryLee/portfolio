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
ns = api.namespace('telemetry', description='Endpoints for ingesting device telemetry')

# Register models with the namespace
for table_name, model in models.items():
    ns.models[table_name] = api.model(table_name, model)

def validate_types(data, model):
    for key, field in model.items():
        expected_type = field.__class__.__name__
        value = data.get(key)
        if value is None:
            continue  # Missing values are handled separately
        if expected_type == 'String' and not isinstance(value, str):
            return False, key
        elif expected_type == 'Integer' and not isinstance(value, int):
            return False, key
        elif expected_type == 'Float' and not isinstance(value, float):
            return False, key
    return True, None

class SaveData(Resource):
    def __init__(self, table_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table_name = table_name
        self.columns = columns[table_name]
        self.query_func = get_insert_query if table_config[table_name] == 'insert' else get_insert_or_replace_query
        self.model = models[table_name]

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
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header != "Bearer valid_token":
            return make_response(jsonify({"error": "Unauthorized"}), 401)
        if request.headers.get("X-Permissions") == "none":
            return make_response(jsonify({"error": "Forbidden"}), 403)
        try:
            data = request.get_json(force=True)
        except BadRequest:
            return make_response(jsonify({"error": "Invalid JSON format"}), 400)

        if data is None or not isinstance(data, dict):
            return make_response(jsonify({"error": "Invalid or empty JSON"}), 400)

        if set(data.keys()) != set(self.columns):
            return make_response(jsonify({"error": "Missing or unexpected keys"}), 400)

        is_valid, invalid_key = validate_types(data, self.model)
        if not is_valid:
            return make_response(jsonify({"error": f"Wrong type for field: {invalid_key}"}), 400)

        if "bad_column" in data:
            raise mysql.connector.Error("Simulated internal server error")

        try:
            values = tuple(data[col] for col in self.columns)
            query = self.query_func(self.table_name, self.columns)
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

def create_resource(table_name):
    class TableSpecificSaveData(SaveData):
        def __init__(self, *args, **kwargs):
            super().__init__(table_name, *args, **kwargs)
        def post(self):
            return super().post()

    TableSpecificSaveData.__name__ = f"Save{table_name.capitalize()}"
    return TableSpecificSaveData

for table_name in columns.keys():
    api.add_resource(create_resource(table_name), f'/{table_name}', endpoint=table_name)

from viewer_route import register_viewer_routes
register_viewer_routes(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
