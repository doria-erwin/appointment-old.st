from sqlalchemy import Date, func, desc, or_
import datetime
from urllib.parse import unquote


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

    def findAllAppointments(self, search=''):
        if search != None and len(search.strip()) > 0:
            search = '%{}%'.format(unquote(search))
            appointments = self.Appointment.query.join(self.Patient).filter(or_(func.lower(self.Patient.firstName).like(func.lower(search)), func.lower(self.Patient.lastName).like(
                func.lower(search)), func.lower(self.Patient.middleName).like(func.lower(search)))).order_by(desc(self.Appointment.id))
        else:
            appointments = self.Appointment.query.order_by(
                desc(self.Appointment.id)).all()

        return appointments

    # determine if there's a overbooked
    # added 1 second to the new starttime to exclude if existing starttime is equal to new booking starttime
    def findAppointmentBetweenDateTime(self, data):
        return self.Appointment.query.filter(self.Appointment.endTime.between(data['startTime'] + datetime.timedelta(0, 1), data['endTime'])).first()

    def findBetweenDate(self, start, end, search):
        if search != None and len(search.strip()) > 0:
            search = '%{}%'.format(unquote(search))
            appointments = self.Appointment.query.filter(func.DATE(self.Appointment.startTime).between(start, end), or_(func.lower(self.Patient.firstName).like(func.lower(search)), func.lower(self.Patient.lastName).like(
                func.lower(search)), func.lower(self.Patient.middleName).like(func.lower(search)))).order_by(desc(self.Appointment.id))
        else:
            appointments = self.Appointment.query.filter(func.DATE(
                self.Appointment.startTime).between(start, end)).order_by(desc(self.Appointment.id))

        return appointments
