
from schema import appointment_schema, patient_schema
from marshmallow import ValidationError
from util import isValidTime
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
            return {"errors": err.messages}, 422
        if self.repo.findAppointmentBetweenDateTime(data) != None:
            return {"errors": "This time already have a booking"}, 400
        return {"appointment": appointment_schema.dump(self.repo.create(self.Appointment(data)))}

    def update(self, request, id):
        appointment = self.Appointment.query.get(id)
        if appointment is None:
            return {"errors": "Appointment not found"}, 422
        try:
            data = appointment_schema.load(request.get_json())
            data['patient']['id'] = appointment.patient.id
            data['comment']['id'] = appointment.comment.id
            validTime = isValidTime(data['startTime'], data['endTime'])
            if validTime:
                return validTime
        except ValidationError as err:
            return {"errors": err.messages}, 422

        appointmentBetweenDateTime = self.repo.findAppointmentBetweenDateTime(
            data)

        if appointmentBetweenDateTime != None and appointmentBetweenDateTime.id != id:
            return {"errors": "This time already have a booking"}, 400

        appointment.update(data)
        return "Successfully updated"

    def show(self, request):
        try:
            start = datetime.strptime('{}'.format(
                request.args.get('startDate')), '%Y-%m-%d')
        except:
            return {"errors": 'invalid startDate format should be YYYY-mm-dd'}, 422

        try:
            end = datetime.strptime('{}'.format(
                request.args.get('endDate')), '%Y-%m-%d')
        except:
            return {"errors": 'invalid endDate format should be YYYY-mm-dd'}, 422

        if start > end:
            return {"errors": 'invalid endDate'}, 422
        elif start == end:
            return {"errors": 'startDate and endDate should not be equal'}, 422
        elif start is None or end is None:
            return {"errors": 'required query parameters startDate and endDate'}, 422

        appointments = list(
            map(lambda appointment: appointment.serialize(), self.repo.findBetweenDate(start, end)))

        return {"appointments": appointments}

    def delete(self, id):
        appointment = self.Appointment.query.get(id)
        if appointment is None:
            return {"errors": "Appointment not found"}, 422
        if self.repo.delete(self.Comment, appointment.comment.id) and self.repo.delete(self.Appointment, id):
            return "Successfully deleted"
        else:
            return {"errors": "Unable to delete appointment please try again later"}, 422
