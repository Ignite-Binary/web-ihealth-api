from flask_restplus import reqparse, inputs, fields


def user_validation(create=True):
    parser = reqparse.RequestParser(trim=True, bundle_errors=True)
    parser.add_argument('user_name',
                        type=inputs.regex(r'^[0-9A-Za-z-]{3,50}$'),
                        required=create, help='User alias unique name',
                        case_sensitive=False)
    parser.add_argument('first_name',
                        type=inputs.regex(r'^[A-Za-z]{3,100}$'),
                        required=create, help='First name',
                        case_sensitive=False)
    parser.add_argument('last_name',
                        type=inputs.regex(r'^[A-Za-z]{3,100}$'),
                        required=create, help='Last name',
                        case_sensitive=False)
    parser.add_argument('gender',
                        type=str,
                        required=create,
                        choices=(
                            'male', 'Male', 'MALE' 'female', 'Female', 'FEMALE'
                        ),
                        help='Gender',
                        case_sensitive=False)
    parser.add_argument('dob',
                        type=inputs.date,
                        required=create, help='Date of Birth')
    parser.add_argument('phone_no',
                        type=inputs.regex(r'^\+[0-9]{10,15}$'),
                        required=create, help='Phone number')
    parser.add_argument('email',
                        type=inputs.email(check=True),
                        required=create, help='Email', case_sensitive=False)
    parser.add_argument('password',
                        type=inputs.regex(
                            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{6,15}$'
                        ), required=create, help='Password')
    return parser.parse_args(strict=True)


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
    'role': fields.Integer(description='User role'),
    'status': fields.String(
        attribute=lambda x: x.status.value, description='User status'),
}
