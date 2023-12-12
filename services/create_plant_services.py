from logger.logger_base import log
from flask import jsonify

class CreatePlantService:
    def __init__(self, db_connector):
        self.db_connector = db_connector
        
    def get_all_plants(self):
        try:
            self.plant = list(self.db_connector.db.plant.find())
            return self.plant
        except Exception as e:
            log.critical(f'Error fetching all plant from the database: {e}')
            return jsonify({'error': f'Error fetching all plant from the database: {e}'}), 500
    
    def get_plants_by_id(self, plant_id):
        try:
            self.plant = self.db_connector.db.plant.find_one({'_id': plant_id})
            return self.plant
        except Exception as e:
            log.critical(f'Error fetching the plant id from the database: {e}')
            return jsonify({'error': f'Error fetching the plant id from the database: {e}'}), 500
        
    def add_plants(self, new_plant):
        try:
            self.max_id = self.db_connector.db.plant.find_one(sort=[('_id', -1)])['_id'] if self.db_connector.db.plant.count_documents({}) > 0 else 0
            self.new_id = self.max_id + 1
            new_plant['_id'] = self.new_id
            self.db_connector.db.plant.insert_one(new_plant)
            return new_plant
        except Exception as e:
            log.critical(f'Error creating the new plant: {e}')
            return jsonify({'error': f'Error creating the new plant: {e}'}), 500
        
    def update_plants(self, plant_id, updated_data):
        try:
            updated_plant = self.get_plant_by_id(plant_id)
            if updated_plant:
                result = self.db_connector.db.plant.update_one({'_id': plant_id}, {'$set': updated_data})
                if result.modified_count > 0:
                    return updated_plant
                else:
                    return {'message': 'The plant is already up-to-date'}
            else:
                return None

        except Exception as e:
            log.critical(f'Error updating the plant data: {e}')
            return jsonify({'error': f'Error updating the plant data: {e}'}), 500
        
    def delete_plants(self, plant_id):
        try:
            deleted_plant = self.get_plant_by_id(plant_id)
            if deleted_plant:
                self.db_connector.db.plant.delete_one({'_id': plant_id})
                return deleted_plant
            else:
                return None

        except Exception as e:
            log.critical(f'Error deleting the plant data: {e}')
            return jsonify({'error': f'Error deleting the plant data: {e}'}), 500