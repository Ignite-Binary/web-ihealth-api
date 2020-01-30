from flask_restplus import Resource, reqparse
from flask_jwt_extended import current_user
from api import profiles_ns
from utitilies.database import update_fields, db
from utitilies.auth import auth_user
from helpers.validators import patient_profile_validate
from helpers.users_helper import (
    verify_owner, delete_temp_image, save_temp_image)
from api.models.patient_profile_model import PatientProfile
from api.models.schemas.patient_schema import patient_schema


patient_schema = profiles_ns.model('PatientProfile', patient_schema)


@profiles_ns.route('/patients')
class PatientProfiles(Resource):
    @auth_user(['admin', 'facility_admin', 'doctor'])
    @profiles_ns.marshal_list_with(patient_schema, envelope='profiles')
    def get(self):
        patients = PatientProfile.query.all()
        return patients

    @auth_user(['admin', 'facility_admin', 'doctor', 'patient'])
    @profiles_ns.marshal_with(patient_schema, envelope='patient')
    def post(self):
        patient = patient_profile_validate(
            reqparse.RequestParser(trim=True, bundle_errors=True))
        patient_profile = PatientProfile.query.filter_by(
            profile_user=current_user.id).first()
        if patient_profile:
            profiles_ns.abort(400, "profile already exists!")
        profile_pic = patient.get('profile_pic')
        if profile_pic:
            save_temp_image(profile_pic)
        else:
            delete_temp_image(f'profile_pic_{current_user.id}')
        patient['user_id'] = current_user.id
        new_profile = PatientProfile(patient)
        new_profile.save()
        return new_profile, 201


@profiles_ns.route('/patients/<int:patient_id>')
class Patient(Resource):
    @auth_user(['admin', 'facility_admin', 'doctor', 'patient'])
    @profiles_ns.marshal_with(patient_schema, envelope='profile')
    def get(self, patient_id):
        patient_profile = PatientProfile.query.filter_by(
            profile_user=patient_id).first_or_404('Patient profile not Found')
        if current_user.user_role.role == 'patient':
            verify_owner(patient_id, current_user.id)
        return patient_profile

    @auth_user(['admin', 'facility_admin', 'doctor', 'patient'])
    @profiles_ns.marshal_with(patient_schema, envelope='profile')
    def put(self, patient_id):
        profile_updates = profiles_ns.payload
        patient_profile = PatientProfile.query.filter_by(
            profile_user=patient_id).first_or_404('Patient profile not Found')
        if current_user.user_role.role == 'patient':
            verify_owner(patient_id, current_user.id)
        patient_profile_validate(
            reqparse.RequestParser(trim=True, bundle_errors=True))
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
        try:
            patient_profile.delete()
        except Exception:
            db.session.rollback()
            profiles_ns.abort(
                403, f"profile {patient_id} cannot be deleted!")
        return {"message": "patient profile deleted"}, 204
