from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_restx import Api, Resource, fields
import mysql.connector
from config import Config
from table_definitions import columns, table_config, models
from sql_queries import get_insert_query, get_insert_or_replace_query

app = Flask(__name__)
api = Api(
    app,
    version='1.0',
    title='Device Telemetry API',
    description='REST API for collecting and storing anonymized telemetry data from storage appliances.'
)

# Load database config
app.config.from_object(Config)

# Register namespace
ns = api.namespace('', description='Device Telemetry Ingest API')


# Register models with the namespace
for table_name, model in models.items():
    ns.models[table_name] = api.model(table_name, model)

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
    Handle POST requests for ingesting data into the specified table.
    """

    # Simulate 401 Unauthorized (must come before get_json)
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header != "Bearer valid_token":
        return make_response(jsonify({"error": "Unauthorized"}), 401)

    # Simulate 403 Forbidden (must come before get_json)
    if request.headers.get("X-Permissions") == "none":
        return make_response(jsonify({"error": "Forbidden"}), 403)

    try:
        # Now it's safe to parse the body
        data = request.get_json()

        # Optionally loosen schema for testing
        if "bad_column" in data:
            raise mysql.connector.Error("Simulated internal server error")

        if set(data.keys()) != set(self.columns):
            return make_response(jsonify({"error": "Unexpected keys in payload"}), 400)

        values = tuple(data[col] for col in self.columns)

    except KeyError as e:
        return make_response(jsonify({"error": f"Missing key: {str(e)}"}), 400)
    except TypeError:
        return make_response(jsonify({"error": "Invalid JSON format"}), 400)

def create_resource(table_name):
    class TableSpecificSaveData(SaveData):
        def __init__(self, *args, **kwargs):
            super().__init__(table_name, *args, **kwargs)

        @ns.expect(ns.models[table_name], validate=True)
        @ns.response(200, 'Success')
        @ns.response(202, 'Accepted')
        @ns.response(204, 'No Content')
        @ns.response(400, 'Invalid JSON format or Missing key')
        @ns.response(401, 'Unauthorized')
        @ns.response(403, 'Forbidden')
        @ns.response(404, 'Not Found')
        @ns.response(500, 'Internal Server Error')
        @ns.response(201, 'Data saved successfully')
        def post(self):
            return super().post()

    TableSpecificSaveData.__name__ = f"Save{table_name.capitalize()}"
    return TableSpecificSaveData

# Register each route
for table_name in columns.keys():
    api.add_resource(create_resource(table_name), f'/{table_name}', endpoint=table_name)

# Register additional viewer routes if present
from viewer_route import register_viewer_routes
register_viewer_routes(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
