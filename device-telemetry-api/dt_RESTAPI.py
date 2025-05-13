from flask import Flask, request, jsonify, make_response # Import Flask and request
from flask_cors import CORS  # Import CORS for cross-origin resource sharing        
from flask_restx import Api, Resource, fields   # Import Flask-RESTx for building REST APIs
import mysql.connector # Import MySQL connector for database operations
from config import Config  # Import the Config class
from table_definitions import columns, table_config, models  # Import columns, table config, and models
from sql_queries import get_insert_query, get_insert_or_replace_query  # Import the SQL query functions

# Initialize Flask app and API
app = Flask(__name__)
api = Api(
    app,
    version='1.0',
    title='Device Telemetry API',
    description='REST API for collecting and storing anonymized telemetry data from storage appliances.'
)

# Load MySQL configurations from the Config class
app.config.from_object(Config)

# Define the API namespace without prefix
ns = api.namespace('telemetry', description='Endpoints for ingesting device telemetry')

# Register models with the API namespace
for table_name, model in models.items():
    ns.models[table_name] = api.model(table_name, model)

# Enable CORS for the app
class SaveData(Resource):
    def __init__(self, table_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table_name = table_name
        self.columns = columns[table_name]
        self.query_func = get_insert_query if table_config[table_name] == 'insert' else get_insert_or_replace_query
    
    @ns.expect(ns.models[table_name], validate=True)   # Expect the model for the table
    @ns.response(200, 'Success') # 200 OK
    @ns.response(201, 'Data saved successfully') # 201 Created
    @ns.response(202, 'Accepted') # 202 Accepted
    @ns.response(204, 'No Content') # 204 No Content        
    @ns.response(400, 'Invalid JSON format or Missing key') # 400 Bad Request
    @ns.response(401, 'Unauthorized')   # 401 Unauthorized  
    @ns.response(403, 'Forbidden')  # 403 Forbidden
    @ns.response(404, 'Not Found')      # 404 Not Found
    @ns.response(500, 'Internal Server Error')  # 500 Internal Server Error
    def post(self):
        """
        Handle POST requests to insert or update data in the table.
        """
        try:
            data = request.get_json()
            values = tuple(data[col] for col in self.columns)
        except KeyError as e:
            return make_response(jsonify({"error": f"Missing key: {str(e)}"}), 400) # Missing key
        except TypeError:
            return make_response(jsonify({"error": "Invalid JSON format"}), 400) # Invalid JSON format

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
            return make_response(jsonify({"error": str(err)}), 500) # Internal Server Error

        return make_response(jsonify({"message": "Data saved successfully"}), 201) # 201 Created

# Factory function to create resources for each table
def create_resource(table_name):
    class TableSpecificSaveData(SaveData):
        def __init__(self, *args, **kwargs):
            super().__init__(table_name, *args, **kwargs)

        @ns.expect(ns.models[table_name], validate=True)
        @ns.response(200, 'Success') # 200 OK
        @ns.response(202, 'Accepted') # 202 Accepted
        @ns.response(204, 'No Content') # 204 No Content
        @ns.response(400, 'Invalid JSON format or Missing key') # 400 Bad Request
        @ns.response(401, 'Unauthorized')   # 401 Unauthorized
        @ns.response(403, 'Forbidden')  # 403 Forbidden
        @ns.response(404, 'Not Found')      # 404 Not Found
        @ns.response(500, 'Internal Server Error')  # 500 Internal Server Error
        @ns.response(201, 'Data saved successfully')    # 201 Created
        @ns.response(400, 'Invalid JSON format or Missing key') # 400 Bad Request
        @ns.response(401, 'Unauthorized')   # 401 Unauthorized
        @ns.response(403, 'Forbidden')  # 403 Forbidden
        @ns.response(404, 'Not Found')    # 404 Not Found
        @ns.response(500, 'Internal Server Error') # 500 Internal Server Error
        def post(self): 
            return super().post()

    TableSpecificSaveData.__name__ = f"Save{table_name.capitalize()}"
    return TableSpecificSaveData

# Register the endpoints for each table dynamically without the /api prefix
for table_name in columns.keys():
    api.add_resource(create_resource(table_name), f'/{table_name}', endpoint=table_name)

# Add the namespace to the API
api.add_namespace(ns)


# --- Viewer Route Integration ---
from viewer_route import register_viewer_routes
register_viewer_routes(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

