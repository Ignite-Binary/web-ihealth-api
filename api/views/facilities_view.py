from flask_restplus import Resource
from helpers.facilities_helper import facility_validation, facility_schema
from api.models.facilities_model import Facility as FacilityModel
from api import facility_ns
from utitilies.database import update_fields

facility_schema = facility_ns.model('Facility', facility_schema)


@facility_ns.route('')
class Facilities(Resource):
    @facility_ns.marshal_list_with(facility_schema, envelope='facilities')
    def get(self):
        facilities = FacilityModel.query.filter_by(status='active').all()
        return facilities

    @facility_ns.expect(facility_schema)
    @facility_ns.marshal_with(facility_schema, envelope='facility')
    def post(self):
        facility = facility_validation()
        name = FacilityModel.query.filter_by(
            name=facility['name'], status='active').first()
        email = FacilityModel.query.filter_by(
            email=facility['email'], status='active').first()
        if name or email:
            try:
                facility = name.name
            except Exception:
                facility = email.email
            facility_ns.abort(400, facility + " already exists!")
        facility['status'] = "active"
        new_facility = FacilityModel(facility)
        new_facility.save()
        return new_facility, 201


@facility_ns.route('/<int:facility_id>')
class Facility(Resource):
    @facility_ns.marshal_list_with(facility_schema, envelope='facility')
    def get(self, facility_id):
        facility = FacilityModel.query.filter_by(
            id=facility_id,
            status='active',
            ).first_or_404(description='Facility not Found')
        return facility

    @facility_ns.expect(facility_schema)
    @facility_ns.marshal_with(facility_schema, envelope='facility')
    def put(self, facility_id):
        facility_updates = facility_ns.payload
        facility = FacilityModel.query.filter_by(
            id=facility_id,
            status='active',
            ).first_or_404(description='Facility not Found')
        facility_validation(False)
        updated_facility = update_fields(facility, facility_updates)
        updated_facility.save()
        return updated_facility

    def delete(self, facility_id):
        facility = FacilityModel.query.filter_by(
            id=facility_id,
            status='active',
            ).first_or_404(description='Facility not Found')
        facility.status = 'deleted'
        facility.save()
        return {"message": "Facility deleted"}, 204
