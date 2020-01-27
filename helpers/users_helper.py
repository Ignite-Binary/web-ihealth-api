import os
from flask_restplus import reqparse, inputs, fields, abort

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

patient_schema = {
    'profile_pic': fields.String(
        attribute=lambda x: "static/images/" +
        (x.profile_pic or 'user_profile.png'),
        description='Patient profile picture'),
    'user_name': fields.String(
        attribute=lambda x: x.user_details.user_name,
        description='Patient unique name'),
    'first_name': fields.String(
        attribute=lambda x: x.user_details.first_name,
        description='Patient first name'),
    'last_name': fields.String(
        attribute=lambda x: x.user_details.last_name,
        description='Patient last name'),
    'gender': fields.String(
        attribute=lambda x: x.user_details.gender.value,
        description='Patient gender'),
    'dob': fields.Date(
        attribute=lambda x: x.user_details.dob,
        description='Patient date of birth'),
    'phone_no': fields.String(
        attribute=lambda x: x.user_details.phone_no,
        description='Patient phone number'),
    'email': fields.String(
        attribute=lambda x: x.user_details.email,
        description='Patient email address'),
    'location': fields.String(
        attribute=lambda x: x.state + ',' + x.location,
        description='Patient location')
}


def allowed_images(filename):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    if '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        return filename.rsplit('.', 1)[1].lower()


def delete_temp_image(filename):
    file_path = f'static/temporary/{filename}'
    if os.path.isfile(f'{file_path}.jpg'):
        os.remove(f'{file_path}.jpg')
    if os.path.isfile(f'{file_path}.jpeg'):
        os.remove(f'{file_path}.jpeg')
    if os.path.isfile(f'{file_path}.png'):
        os.remove(f'{file_path}.png')


def save_temp_image(filename):
    temp_path = f'static/temporary/{filename}'
    permanent_path = f'static/images/{filename}'
    if os.path.isfile(temp_path):
        os.rename(temp_path, permanent_path)
        return filename


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
    parser.add_argument('role', type=inputs.positive, help='User role')
    parser.add_argument('password',
                        type=inputs.regex(
                            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{6,15}$'
                        ), required=create, help='Password')
    return parser.parse_args(strict=True)


def patient_profile_validate():
    parser = reqparse.RequestParser(trim=True, bundle_errors=True)
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


def verify_owner(owner, identity):
    if owner != identity:
        abort(403, 'You are not authorized!')
