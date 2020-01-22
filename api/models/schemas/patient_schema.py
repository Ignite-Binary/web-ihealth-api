from flask_restplus import fields

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
