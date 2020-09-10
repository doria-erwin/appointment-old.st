from sqlalchemy import Date, func
import datetime


class Repository:
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

    def delete(self, obj, id):
        try:
            self.session.query(obj).filter_by(id=id).delete()
            self.session.commit()
            return True
        except:
            return False

    # determine if there's a overbooked
    # added 1 second to the new starttime to exclude if existing starttime is equal to new booking starttime
    def findAppointmentBetweenDateTime(self, data):
        return self.Appointment.query.filter(self.Appointment.endTime.between(data['startTime'] + datetime.timedelta(0, 1), data['endTime'])).first()

    def findBetweenDate(self, start, end):
        return self.Appointment.query.filter(func.DATE(self.Appointment.startTime).between(start, end))
