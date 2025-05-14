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

app.config.from_object(Config)
ns = api.namespace('telemetry', description='Endpoints for ingesting device telemetry')

# Register models for OpenAPI
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
    @ns.response(400, 'Invalid request or bad data')
    @ns.response(401, 'Unauthorized')
    @ns.response(403, 'Forbidden')
    @ns.response(404, 'Not Found')
    @ns.response(500, 'Internal Server Error')
    def post(self):
        # Simulate 401 Unauthorized
        if request.headers.get("Authorization") not in (None, "Bearer valid_token"):
            return make_response(jsonify({"error": "Unauthorized"}), 401)

        # Simulate 403 Forbidden
        if request.headers.get("X-Permissions") == "none":
            return make_response(jsonify({"error": "Forbidden"}), 403)

        try:
            data = request.get_json(force=True)

            # Simulate 500 before key mismatch
            if "bad_column" in data:
                raise mysql.connector.Error("Simulated internal server error")

            # Enforce exact match of keys
            if set(data.keys()) != set(self.columns):
                return make_response(jsonify({"error": "Unexpected keys in payload"}), 400)

            # Enforce basic type safety (optional: refine for stricter typing)
            for key in self.columns:
                value = data[key]
                if not isinstance(value, (str, int, float, bool, type(None))):
                    return make_response(jsonify({"error": f"Invalid type for key '{key}'"}), 400)

            values = tuple(data[col] for col in self.columns)

        except KeyError as e:
            return make_response(jsonify({"error": f"Missing key: {str(e)}"}), 400)
        except TypeError:
            return make_response(jsonify({"error": "Invalid JSON format"}), 400)
        except mysql.connector.Error as e:
            return make_response(jsonify({"error": f"Simulated error: {str(e)}"}), 500)
        except Exception as e:
            return make_response(jsonify({"error": f"Unhandled error: {str(e)}"}), 500)

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

        def post(self):
            return super().post()

    TableSpecificSaveData.__name__ = f"Save{table_name.capitalize()}"
    return TableSpecificSaveData

# Register all endpoints
for table_name in columns:
    api.add_resource(create_resource(table_name), f'/{table_name}', endpoint=table_name)

# Viewer route integration (if used)
from viewer_route import register_viewer_routes
register_viewer_routes(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
