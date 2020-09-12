
from schema import appointment_schema, patient_schema
from marshmallow import ValidationError
from util import isValidTime, isValidDates, response
from datetime import datetime
from repository import Repository


class Service:
    def __init__(self, session, Appointment, Patient, Comment):
        self.repo = Repository(session, Appointment, Patient, Comment)
        self.Patient = Patient
        self.Appointment = Appointment
        self.Comment = Comment

    def create(self, request):
        try:
            data = appointment_schema.load(request.get_json())
            validTime = isValidTime(data['startTime'], data['endTime'])
            if validTime:
                return validTime
        except ValidationError as err:
            return response(err.messages, False, 422)
        if self.repo.findAppointmentBetweenDateTime(data) != None:
            return response("This time already have a booking", False, 400)

        return appointment_schema.dump(self.repo.create(self.Appointment(data)))

    def update(self, request, id):
        appointment = self.Appointment.query.get(id)
        if appointment is None:
            return response("Appointment not found", False, 422)
        try:
            data = appointment_schema.load(request.get_json())
            data['patient']['id'] = appointment.patient.id
            data['comment']['id'] = appointment.comment.id
            validTime = isValidTime(data['startTime'], data['endTime'])
            if validTime:
                return validTime
        except ValidationError as err:
            return response(err.messages, False, 422)

        appointmentBetweenDateTime = self.repo.findAppointmentBetweenDateTime(
            data)

        if appointmentBetweenDateTime != None and appointmentBetweenDateTime.id != id:
            return response("This time already have a booking", False, 400)

        appointment.update(data)
        return response("Successfully updated", key="message")

    def findAll(self, request):
        if request.args.get('startDate'):
            validDates = isValidDates(request)
            if validDates:
                return validDates

            appointments = list(
                map(lambda appointment: appointment.serialize(), self.repo.findBetweenDate(request.args.get('startDate'), request.args.get('endDate'))))
        else:
            appointments = list(
                map(lambda appointment: appointment.serialize(), self.repo.findAll(self.Appointment)))

        return response(appointments, key="appointments")

    def delete(self, id):
        appointment = self.Appointment.query.get(id)
        if appointment is None:
            return response("Appointment not found", False, 422)
        if self.repo.delete(self.Patient, appointment.patient.id) and self.repo.delete(self.Comment, appointment.comment.id) and self.repo.delete(self.Appointment, id):
            return response("Successfully deleted", key="message")
        else:
            return response("Unable to delete appointment please try again later", False, 422)

    def findById(self, id):
        return response(appointment_schema.dump(self.Appointment.query.get(id)))
