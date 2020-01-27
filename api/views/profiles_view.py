from flask_restplus import Resource
from flask_jwt_extended import current_user
from helpers.users_helper import (
    patient_profile_validate, patient_schema,
    verify_owner, delete_temp_image, save_temp_image)
from api.models.profiles_model import PatientProfile
from api import patient_prof_ns
from utitilies.database import update_fields
from utitilies.auth import auth_user


patient_schema = patient_prof_ns.model('PatientProfile', patient_schema)


@patient_prof_ns.route('')
class PatientProfiles(Resource):
    @auth_user(['admin', 'facility_admin', 'doctor'])
    @patient_prof_ns.marshal_list_with(patient_schema, envelope='profiles')
    def get(self):
        patients = PatientProfile.query.all()
        return patients

    @auth_user(['admin', 'facility_admin', 'doctor', 'patient'])
    @patient_prof_ns.marshal_with(patient_schema, envelope='patient')
    def post(self):
        patient = patient_profile_validate()
        patient_profile = PatientProfile.query.filter_by(
            profile_user=current_user.id).first()
        if patient_profile:
            patient_prof_ns.abort(400, "profile already exists!")
        profile_pic = patient.get('profile_pic')
        if profile_pic:
            save_temp_image(profile_pic)
        else:
            delete_temp_image(f'profile_pic_{current_user.id}')
        patient['user_id'] = current_user.id
        new_profile = PatientProfile(patient)
        new_profile.save()
        return new_profile, 201


@patient_prof_ns.route('/<int:patient_id>')
class Patient(Resource):
    @auth_user(['admin', 'facility_admin', 'doctor', 'patient'])
    @patient_prof_ns.marshal_with(patient_schema, envelope='profile')
    def get(self, patient_id):
        patient_profile = PatientProfile.query.filter_by(
            profile_user=patient_id).first_or_404('Patient profile not Found')
        if current_user.user_role.role == 'patient':
            verify_owner(patient_id, current_user.id)
        return patient_profile

    @auth_user(['admin', 'facility_admin', 'doctor', 'patient'])
    @patient_prof_ns.marshal_with(patient_schema, envelope='profile')
    def put(self, patient_id):
        profile_updates = patient_prof_ns.payload
        patient_profile = PatientProfile.query.filter_by(
            profile_user=patient_id).first_or_404('Patient profile not Found')
        if current_user.user_role.role == 'patient':
            verify_owner(patient_id, current_user.id)
        patient_profile_validate()
        profile_pic = profile_updates.get('profile_pic')
        if profile_pic:
            saved_pic = save_temp_image(profile_pic)
            if not saved_pic:
                del profile_updates['profile_pic']
        else:
            delete_temp_image(f'profile_pic_{patient_id}')
        updated_profile = update_fields(patient_profile, profile_updates)
        updated_profile.save()
        return updated_profile

    @auth_user(['admin'])
    def delete(self, patient_id):
        patient_profile = PatientProfile.query.filter_by(
            profile_user=patient_id).first_or_404('Patient profile not Found')
        patient_profile.delete()
        return {"message": "patient profile deleted"}, 204
