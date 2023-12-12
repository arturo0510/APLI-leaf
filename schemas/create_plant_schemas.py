from marshmallow import fields, validates, ValidationError

class CreatePlantSchema:
    name = fields.String(required=True)
    description = fields.String(required=False)
    date_l = fields.String(required=True)

    @validates('name')
    def validate_name(self, value):
        if len(value) > 120:
            raise ValidationError('The name must have a maximum of 120 characters.')
        
    @validates('description')
    def validate_description(self, value):
        if len(value) > 300:
            raise ValidationError('The Description must have a maximum of 300 characters.')

    @validates('date_l')
    def validate_date(self, value):
        """
        Validates the due date format.
        Args:
            value: The due date string.
        Raises:
            ValidationError: If the due date does not have the format "YYYY-MM-DD HH:mm:ss".
        """
        try:
            datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise ValidationError('Due date must have the format "YYYY-MM-DD HH:mm:ss".')