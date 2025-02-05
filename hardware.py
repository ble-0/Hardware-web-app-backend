

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from flask import request
from datetime import datetime
from models import Hardware  
from extensions import db

# Define the namespace
hardware_ns = Namespace('hardware', description="Operations related to hardware items")

# Define the hardware model for API documentation
Hardware_model = hardware_ns.model(
    'Hardware',
    {
        'id': fields.Integer(description='The ID', example=1),
        'title': fields.String(required=True, description='The title of the hardware', example='Drill Machine'),
        'user_id': fields.Integer(required=True, description='The ID of the user who created the hardware', example=123),
        'destination': fields.String(required=True, description='The destination of the hardware', example='Warehouse A'),
        'details': fields.String(required=True, description='The details of the hardware', example='Heavy-duty drill machine with 10mm chuck'),
        'date': fields.String(required=True, description='The date of the hardware (YYYY-MM-DD)', example='2023-10-15')
    }
)

# Route for retrieving and creating hardware
@hardware_ns.route('/hardware')
class HardwareResource(Resource):
    @hardware_ns.marshal_list_with(Hardware_model)
    def get(self):
        """Fetch all hardware items"""
        hardwares = Hardware.query.all()
        return hardwares, 200

    @jwt_required()
    @hardware_ns.expect(Hardware_model)
    @hardware_ns.marshal_with(Hardware_model)
    def post(self):
        """Create a new hardware item"""
        data = request.get_json()

        # Validate input
        if not data:
            return {"error": "Invalid JSON data"}, 400

        # Convert date to correct format
        try:
            formatted_date = datetime.strptime(data.get('date'), '%Y-%m-%d').date()
        except ValueError:
            return {"error": "Invalid date format. Use YYYY-MM-DD"}, 400

        # Create new hardware item
        new_hardware = Hardware(
            title=data.get('title'),
            user_id=data.get('user_id'),
            destination=data.get('destination'),
            details=data.get('details'),
            date=formatted_date
        )

        db.session.add(new_hardware)
        db.session.commit()

        return new_hardware, 201


# Route for retrieving, updating, and deleting a specific hardware item
@hardware_ns.route('/hardware/<int:id>')
class HardwareItemResource(Resource):
    @jwt_required()
    @hardware_ns.marshal_with(Hardware_model)
    def get(self, id):
        """Get a hardware item by ID"""
        hardware = Hardware.query.get_or_404(id)
        return hardware, 200

    @jwt_required()
    @hardware_ns.expect(Hardware_model)
    @hardware_ns.marshal_with(Hardware_model)
    def put(self, id):
        """Update an existing hardware item"""
        hardware = Hardware.query.get_or_404(id)
        data = request.get_json()

        if not data:
            return {"error": "Invalid JSON data"}, 400

        # Convert date format if present
        if 'date' in data:
            try:
                data['date'] = datetime.strptime(data['date'], '%Y-%m-%d').date()
            except ValueError:
                return {"error": "Invalid date format. Use YYYY-MM-DD"}, 400

        # Update fields
        hardware.title = data.get('title', hardware.title)
        hardware.user_id = data.get('user_id', hardware.user_id)
        hardware.destination = data.get('destination', hardware.destination)
        hardware.details = data.get('details', hardware.details)
        hardware.date = data.get('date', hardware.date)

        db.session.commit()
        return hardware, 200

    @jwt_required()
    def delete(self, id):
        """Delete a hardware item"""
        hardware = Hardware.query.get(id)
        if not hardware:
            return {"error": "Hardware not found"}, 404

        db.session.delete(hardware)
        db.session.commit()
        return {"message": "Hardware deleted successfully"}, 200