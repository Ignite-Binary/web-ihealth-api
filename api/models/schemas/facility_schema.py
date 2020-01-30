from flask_restplus import fields

facility_schema = {
    'id': fields.Integer(description='The facility unique identifier'),
    'name': fields.String(description='Facility name'),
    'location': fields.String(description='Facility location'),
    'certifications': fields.String(description='Facility certifications'),
    'phone_no': fields.String(description='Facility phone number'),
    'email': fields.String(description='Facility email address'),
    'status': fields.String(attribute=lambda x: x.status.value,
                            description='Facility status'),
}
