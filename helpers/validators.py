from flask_restplus import inputs


def user_validation(parser, create=True):
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
    parser.add_argument('role', type=inputs.positive, help='User role')
    parser.add_argument('password',
                        type=inputs.regex(
                            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{6,15}$'
                        ), required=create, help='Password')
    return parser.parse_args(strict=True)


def patient_profile_validate(parser):
    parser.add_argument('profile_pic',
                        type=str, help='User picture')
    parser.add_argument('country',
                        type=inputs.regex(r'^[A-Za-z]{1,100}$'),
                        help='country name')
    parser.add_argument('state',
                        type=inputs.regex(r'^[A-Za-z]{1,100}$'),
                        help='state/region/county name')
    parser.add_argument('location',
                        type=str, help='location name')
    return parser.parse_args(strict=True)


def doctor_parser(parser):
    parser.add_argument('specialty', type=str, trim=True,
                        help='Username', location='json')
    parser.add_argument('bio', type=str, trim=True,
                        help='Password', location='json')
    return parser
