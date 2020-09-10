from sqlalchemy import Date, func
import datetime


class repository:
    def __init__(self, session, Appointment, Patient, Comment):
        self.session = session
        self.Appointment = Appointment
        self.Patient = Patient
        self.Comment = Comment

    def create(self, obj):
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def updateById(self, obj, id, data):
        self.session.query(obj).filter_by(id=id).update(data)
        self.session.commit()
        return obj

    def findAppointmentBetweenDateTime(self, data):
        return self.Appointment.query.filter(self.Appointment.endTime.between(data['startTime'] + datetime.timedelta(0, 1), data['endTime'])).first()

    def findAppointmentByDateAndPatient(self, data, patient):
        return self.Appointment.query.filter(func.DATE(self.Appointment.startTime) == data['startTime'].date(), self.Appointment.patient_id == patient.id).first()

    def findPatientByName(self, data):
        return self.Patient.query.filter(func.lower(self.Patient.firstName) == func.lower(data['firstName']), func.lower(self.Patient.lastName) == func.lower(data['lastName']), func.lower(self.Patient.middleName) == func.lower(data['middleName'])).first()

    def findBetweenDate(self, start, end):
        return self.Appointment.query.filter(func.DATE(self.Appointment.startTime).between(start, end))
