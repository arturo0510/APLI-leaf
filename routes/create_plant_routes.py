from flask import Blueprint, jsonify, request
from logger.logger_base import log
from marshmallow import ValidationError

class CreatePlantRoutes(Blueprint):
    def __init__(self, plant_service, plant_schema):
        super().__init__('plant', __name__)
        self.plant_service = plant_service
        self.plant_schema = plant_schema
        self.register_routes()

    def register_routes(self):
        self.route('/api/plants', methods=['GET'])(self.get_plants)
        self.route('/api/plants/<int:plant_id>', methods=['GET'])(self.get_plants_by_id)
        self.route('/api/plants', methods=['POST'])(self.add_plant)
        self.route('/api/plants/<int:plant_id>', methods=['PUT'])(self.update_plant)
        self.route('/api/plants/<int:plant_id>', methods=['DELETE'])(self.delete_plant)

    def get_plants(self):
        try:
            self.plants = self.plant_service.get_all_plants()
            return jsonify(self.plants), 200
        except Exception as e:
            log.exception(f'Error fetching data from the database: {e}')
            return jsonify({'error': 'Failed to fetch data from the database'}), 500
    
    def get_plants_by_id(self, plant_id):
        self.plant = self.plant_service.get_plant_by_id(plant_id)
        if self.plant:
            return jsonify(self.plant), 200
        else: 
            return jsonify({'error': 'plant not found'}), 404
        
    def add_plant(self):
        try:
            self.data = request.json
            if not self.data:
                return jsonify({'error': 'Invalid data'}), 400
            
            self.name = self.data.get('name')
            self.description = self.data.get('description')
            self.date_l = self.data.get('date_l')

            try:
                self.plant_schema.validate_name(self.name)
                self.plant_schema.validate_description(self.description)
                self.plant_schema.validate_date(self.date_l)
            except ValidationError as e:
                 return(jsonify({'error': 'Invalid data', 'details': e.messages}), 400)
            
            self.new_plant = {
                'name': self.name,
                'description': self.description,
                'date_l': self.date_l
            }

            self.created_plant = self.plant_service.add_plant(self.new_plant)
            return jsonify(self.created_plant), 201
        except Exception as e:
            log.critical(f'Error adding a new plant to the database: {e}')

    def update_plant(self, plant_id):
        try:
            self.data = request.json
            if not self.data:
                return jsonify({'error': 'Invalid data'}), 400
            
            self.name = self.data.get('name')
            self.description = self.data.get('description')
            self.date_l= self.data.get('date_l')

            try:
                self.plant_schema.validate_name(self.name)
                self.plant_schema.validate_description(self.description)
                self.plant_schema.validate_date(self.date_l)
            except ValidationError as e:
                 return(jsonify({'error': 'Invalid data', 'details': e.messages}), 400)
            
            self.plant_updated = self.plant_service.update_plant(plant_id, self.data)

            if self.plant_updated:
                return jsonify(self.plant_updated), 200
            else:
                return jsonify({'error': 'plant not found'}), 404

        except Exception as e:
            log.critical(f'Error updating the plant in the database: {e}')

    def delete_plant(self, plant_id):
        try:
            self.plant_deleted = self.plant_service.delete_plant(plant_id)
            if self.plant_deleted:
                return jsonify(self.plant_deleted), 200
            else:
                return jsonify({'error': 'plant not found'}), 404
        except Exception as e:
            log.critical(f'Error deleting the plant in the database: {e}')