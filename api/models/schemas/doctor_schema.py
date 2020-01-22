from flask_restplus import fields

doctor_schema = {
    'profile_pic': fields.String(
        attribute=lambda x: "static/images/" +
        (x.doctor_details.profile_pic or 'user_profile.png'),
        description='Doctor profile picture'),
    'user_name': fields.String(
        attribute=lambda x: x.doctor_details.user_details.user_name,
        description='Doctor unique name'),
    'first_name': fields.String(
        attribute=lambda x: x.doctor_details.user_details.first_name,
        description='Doctor first name'),
    'last_name': fields.String(
        attribute=lambda x: x.doctor_details.user_details.last_name,
        description='Doctor last name'),
    'specialty': fields.String(description='Doctor  area of specialization'),
    'bio': fields.String(description='Doctor short bio'),
    'gender': fields.String(
        attribute=lambda x: x.doctor_details.user_details.gender.value,
        description='Doctor gender'),
    'dob': fields.Date(
        attribute=lambda x: x.doctor_details.user_details.dob,
        description='Doctor date of birth'),
    'phone_no': fields.String(
        attribute=lambda x: x.doctor_details.user_details.phone_no,
        description='Doctor phone number'),
    'email': fields.String(
        attribute=lambda x: x.doctor_details.user_details.email,
        description='Doctor email address'),
    'location': fields.String(
        attribute=lambda x: x.doctor_details.state +
        ',' + x.doctor_details.location,
        description='Doctor location')
}
