from flask_restplus import Resource
from flask_jwt_extended import current_user
from helpers.users_helper import verify_owner
from api.models.doctor_profile_model import PatientProfile
from api.models.doctor_profile_model import DoctorProfile
from api.models.schemas.doctor_schema import doctor_schema
from api import profiles_ns
from utitilies.database import update_fields
from utitilies.auth import auth_user
from helpers.validators import doctor_parser

doctor_parser = doctor_parser(profiles_ns.parser())
doctor_schema = profiles_ns.model('DoctorProfile', doctor_schema)


@profiles_ns.route('/doctors')
class DoctorProfiles(Resource):
    @auth_user(['admin', 'facility_admin'])
    @profiles_ns.marshal_list_with(doctor_schema, envelope='doctors')
    def get(self):
        doctors = DoctorProfile.query.all()
        return doctors

    @auth_user(['admin', 'facility_admin', 'doctor'])
    @profiles_ns.expect(doctor_parser)
    @profiles_ns.marshal_with(doctor_schema, envelope='doctor')
    def post(self):
        doctor = doctor_parser.parse_args(strict=True)
        doctor_profile = DoctorProfile.query.filter_by(
            patient_profile=current_user.id).first()
        if doctor_profile:
            profiles_ns.abort(400, "profile already exists!")
        patient_profile = PatientProfile.query.filter_by(
            profile_user=current_user.id).first()
        if not patient_profile:
            patient = {"user_id": current_user.id}
            new_patient_prof = PatientProfile(patient)
            new_patient_prof.save()
        doctor['patient_profile'] = current_user.id
        new_profile = DoctorProfile(doctor)
        new_profile.save()
        return new_profile, 201


@profiles_ns.route('/doctors/<int:doctor_id>')
class Doctor(Resource):
    @auth_user(['admin', 'facility_admin', 'doctor', 'patient'])
    @profiles_ns.marshal_with(doctor_schema, envelope='doctor')
    def get(self, doctor_id):
        doctor_profile = DoctorProfile.query.filter_by(
            patient_profile=doctor_id
            ).first_or_404('Doctor profile not Found!')

        return doctor_profile

    @auth_user(['admin', 'facility_admin', 'doctor'])
    @profiles_ns.marshal_with(doctor_schema, envelope='doctor')
    def put(self, doctor_id):
        profile_updates = profiles_ns.payload
        doctor_profile = DoctorProfile.query.filter_by(
            patient_profile=doctor_id
            ).first_or_404('Doctor profile not Found!')
        if current_user.user_role.role == 'doctor':
            verify_owner(doctor_id, current_user.id)
        doctor_parser.parse_args(strict=True)
        updated_profile = update_fields(doctor_profile, profile_updates)
        updated_profile.save()
        return updated_profile

    @auth_user(['admin'])
    def delete(self, doctor_id):
        doctor_profile = DoctorProfile.query.filter_by(
            patient_profile=doctor_id
            ).first_or_404('Doctor profile not Found!')
        doctor_profile.delete()
        return {"message": "doctor profile deleted"}, 204
