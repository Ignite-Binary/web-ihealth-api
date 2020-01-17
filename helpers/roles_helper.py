from flask_restplus import reqparse, inputs, fields


def role_validation(create=True):
    parser = reqparse.RequestParser(trim=True, bundle_errors=True)
    parser.add_argument('role',
                        type=inputs.regex(r'^[0-9A-Za-z_]{3,50}$'),
                        required=create, help='role name',
                        case_sensitive=False)
    parser.add_argument('code',
                        type=inputs.positive,
                        required=create, help='role code')
    return parser.parse_args(strict=True)


role_schema = {
    'id': fields.Integer(description='Role unique identifier'),
    'role': fields.String(description='role name'),
    'code': fields.Integer(description='role code')
}
