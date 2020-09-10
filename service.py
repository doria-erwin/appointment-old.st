
from schema import appointment_schema, patient_schema
from marshmallow import ValidationError
from util import isValidTime, response
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

        return response(appointment_schema.dump(self.repo.create(self.Appointment(data))))

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

    def show(self, request):
        try:
            start = datetime.strptime('{}'.format(
                request.args.get('startDate')), '%Y-%m-%d')
        except:
            return response("invalid startDate format should be YYYY-mm-dd", False, 422)

        try:
            end = datetime.strptime('{}'.format(
                request.args.get('endDate')), '%Y-%m-%d')
        except:
            return response("invalid endDate format should be YYYY-mm-dd", False, 422)

        if start > end:
            return response("invalid endDate", False, 422)
        elif start == end:
            return response("startDate and endDate should not be equal", False, 422)
        elif start is None or end is None:
            return response("required query parameters startDate and endDate", False, 422)

        appointments = list(
            map(lambda appointment: appointment.serialize(), self.repo.findBetweenDate(start, end)))

        return response(appointments, key="appointments")

    def delete(self, id):
        appointment = self.Appointment.query.get(id)
        if appointment is None:
            return response("Appointment not found", False, 422)
        if self.repo.delete(self.Patient, appointment.patient.id) and self.repo.delete(self.Comment, appointment.comment.id) and self.repo.delete(self.Appointment, id):
            return response("Successfully deleted", key="message")
        else:
            return response("Unable to delete appointment please try again later", False, 422)
