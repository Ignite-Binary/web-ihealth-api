from flask_restplus import reqparse, inputs, fields


def facility_validation(create=True):
    parser = reqparse.RequestParser(trim=True, bundle_errors=True)
    parser.add_argument('name',
                        type=inputs.regex(r'^[0-9A-Za-z-]{3,50}$'),
                        required=create, help='Facility name',
                        case_sensitive=False)
    parser.add_argument('location',
                        type=inputs.regex(r'^[A-Za-z]{3,100}$'),
                        required=create, help='Facility location',
                        case_sensitive=False)
    parser.add_argument('certifications',
                        type=str,
                        required=create,
                        help='certifications')
    parser.add_argument('phone_no',
                        type=inputs.regex(r'^\+[0-9]{10,15}$'),
                        required=create, help='Phone number')
    parser.add_argument('email',
                        type=inputs.email(check=True),
                        required=create, help='Email')
    return parser.parse_args(strict=True)


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
