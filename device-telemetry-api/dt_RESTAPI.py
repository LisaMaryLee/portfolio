from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_restx import Api, Resource, fields
import mysql.connector
from config import Config
from table_definitions import columns, table_config, models
from sql_queries import get_insert_query, get_insert_or_replace_query
import json

app = Flask(__name__)
api = Api(
    app,
    version='1.0',
    title='Device Telemetry API',
    description='REST API for collecting and storing anonymized telemetry data from storage appliances.'
)

app.config.from_object(Config)
ns = api.namespace('telemetry', description='Endpoints for ingesting device telemetry')

# Register models
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
        # 🛡️ Simulate 401 Unauthorized
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header != "Bearer valid_token":
            return make_response(jsonify({"error": "Unauthorized"}), 401)

        # 🚫 Simulate 403 Forbidden
        if request.headers.get("X-Permissions") == "none":
            return make_response(jsonify({"error": "Forbidden"}), 403)

        try:
            # 🧪 Parse raw data first for JSON validation
            raw_data = request.get_data(as_text=True)
            data = json.loads(raw_data)

            # 🔥 Simulate 500 Internal error
            if "bad_column" in data:
                raise mysql.connector.Error("Simulated internal server error")

            # 🚫 Reject if payload keys do not match model
            if set(data.keys()) != set(self.columns):
                return make_response(jsonify({"error": "Unexpected keys in payload"}), 400)

            # 🔎 Simple type check
            for col in self.columns:
                if not isinstance(data[col], str):
                    return make_response(jsonify({"error": f"Invalid type for key '{col}'"}), 400)

            values = tuple(data[col] for col in self.columns)

        except json.JSONDecodeError:
            return make_response(jsonify({"error": "Malformed JSON"}), 400)
        except KeyError as e:
            return make_response(jsonify({"error": f"Missing key: {str(e)}"}), 400)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

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

# Register all table endpoints
for table_name in columns.keys():
    api.add_resource(create_resource(table_name), f'/{table_name}', endpoint=table_name)

# Add viewer route
from viewer_route import register_viewer_routes
register_viewer_routes(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
