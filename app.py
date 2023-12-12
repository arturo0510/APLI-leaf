from flask import Flask
from models.create_plant_models import CreatePlantModel
from flask_swagger_ui import get_swaggerui_blueprint
from services.create_plant_services import CreatePlantService
from routes.create_plant_routes import CreatePlantRoutes
from schemas.create_plant_schemas import CreatePlantSchema
from flask_cors import CORS

app = Flask(__name__)
'''
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Access API'
    }
)

app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
'''
db_connector = CreatePlantModel()
db_connector.connect_to_database()

plant_service = CreatePlantService(db_connector)
plant_schema = CreatePlantSchema()

plant_blueprint = CreatePlantRoutes(plant_service, plant_schema)
app.register_blueprint(plant_blueprint)

CORS(app, resources={r'/api/plants': {'origins': 'http://localhost:3000'}})

if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        db_connector.close_connection()