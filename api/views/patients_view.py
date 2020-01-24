from flask_restplus import Resource
from flask_jwt_extended import current_user
from helpers.users_helper import user_validation, user_schema, verify_owner
from api.models.users_model import User
from api import user_ns
from utitilies.database import update_fields
from utitilies.auth import auth_user


user_schema = user_ns.model('User', user_schema)


@user_ns.route('/patients')
class Patients(Resource):
    @auth_user(['admin', 'facility_admin'])
    @user_ns.marshal_list_with(user_schema, envelope='patients')
    def get(self):
        patients = User.query.filter_by(status='active', role=4).all()
        return patients

    @user_ns.expect(user_schema)
    @user_ns.marshal_with(user_schema, envelope='patient')
    def post(self):
        patient = user_validation()
        user_name = User.query.filter_by(
            user_name=patient['user_name'], status='active').first()
        user_email = User.query.filter_by(
            email=patient['email'], status='active').first()
        if user_name or user_email:
            try:
                existing_user = user_name.user_name
            except Exception:
                existing_user = user_email.email
            user_ns.abort(400, f"{existing_user} already exists!")
        patient['status'] = "active"
        patient['role'] = 4
        new_patient = User(patient)
        new_patient.save()
        return new_patient, 201


@user_ns.route('/patients/<int:patient_id>')
class Patient(Resource):
    @auth_user(['admin', 'facility_admin', 'doctor', 'patient'])
    @user_ns.marshal_with(user_schema, envelope='patient')
    def get(self, patient_id):
        patient = User.query.filter_by(
            id=patient_id,
            status='active',
            role=4).first_or_404('Patient not Found')
        if current_user.user_role.role == 'patient':
            verify_owner(patient.id, current_user.id)
        return patient

    @auth_user(['admin', 'facility_admin', 'doctor', 'patient'])
    @user_ns.expect(user_schema)
    @user_ns.marshal_with(user_schema, envelope='patient')
    def put(self, patient_id):
        patient_updates = user_ns.payload
        patient = User.query.filter_by(
            id=patient_id,
            status='active',
            role=4).first_or_404('Patient not Found')
        if current_user.user_role.role == 'patient':
            verify_owner(patient.id, current_user.id)
        user_validation(False)
        updated_patient = update_fields(patient, patient_updates)
        updated_patient.save()
        return updated_patient

    @auth_user(['admin', 'patient'])
    def delete(self, patient_id):
        patient = User.query.filter_by(
            id=patient_id,
            status='active',
            role=4).first_or_404('Patient not Found')
        if current_user.user_role.role == 'patient':
            verify_owner(patient.id, current_user.id)
        patient.status = 'deleted'
        patient.save()
        return {"message": "patient deleted"}, 204