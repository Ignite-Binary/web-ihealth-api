from flask_restplus import fields

user_schema = {
    'id': fields.Integer(description='The user unique identifier'),
    'user_name': fields.String(description='User unique name'),
    'first_name': fields.String(description='User first name'),
    'last_name': fields.String(description='User last name'),
    'gender': fields.String(
        attribute=lambda x: x.gender.value, description='User gender'),
    'dob': fields.Date(description='User date of birth'),
    'phone_no': fields.String(description='User phone number'),
    'email': fields.String(description='User email address'),
    'role': fields.String(
        attribute=lambda x: x.user_role.role, description='User role'),
    'status': fields.String(
        attribute=lambda x: x.status.value, description='User status')
}
