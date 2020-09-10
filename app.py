from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Text, ForeignKey, String, DateTime, Boolean, update
from sqlalchemy.orm.exc import NoResultFound
from gevent.pywsgi import WSGIServer
from schema import appointment_schema, patient_schema
from marshmallow import ValidationError
import datetime
from config import HOST, PORT
from repository import repository
from util import isValidTime

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)


class Comment(db.Model):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    message = Column(Text(), nullable=False)
    appointment_id = Column(Integer, ForeignKey('appointment.id'))
    appointment = db.relationship("Appointment", back_populates="comment")

    def __init__(self, message, appointment):
        self.message = message
        self.appointment = appointment

    def serialize(self):
        return{
            "id": self.id,
            "message": self.message,
        }


class Patient(db.Model):
    __tablename__ = 'patient'
    id = Column(Integer, primary_key=True)
    firstName = Column(String(50), nullable=False)
    lastName = Column(String(50), nullable=False)
    middleName = Column(String(50), nullable=False)
    appointment = db.relationship("Appointment",  back_populates="patient")

    def __init__(self, data):
        self.firstName = data['firstName']
        self.lastName = data['lastName']
        self.middleName = data['middleName']

    def serialize(self):
        return {
            "id": self.id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "middleName": self.middleName
        }


class Appointment(db.Model):
    __tablename__ = 'appointment'
    id = Column(Integer, primary_key=True)
    startTime = Column(DateTime, nullable=False)
    endTime = Column(DateTime, nullable=False)
    comment = db.relationship("Comment", uselist=False,
                              back_populates="appointment", lazy='joined')
    patient_id = Column(Integer, ForeignKey('patient.id'))
    patient = db.relationship(
        "Patient", back_populates="appointment", lazy='joined')

    def __init__(self, data):
        self.startTime = data['startTime']
        self.endTime = data['endTime']

    def serialize(self):
        return{
            "id": self.id,
            "startTime": self.startTime,
            "endTime": self.startTime,
            "comment": self.comment.serialize(),
            "patient": self.patient.serialize()
        }


db.create_all()

repo = repository(db.session, Appointment, Patient, Comment)


@app.route('/appointment', methods=['POST'])
def create():
    try:
        data = appointment_schema.load(request.get_json())
        patient = repo.findPatientByName(data['patient'])
        isValidTime(data['startTime'], data['endTime'])
    except ValidationError as err:
        return {"errors": err.messages}, 422
    if patient != None and repo.findAppointmentByDateAndPatient(data, patient) != None:
        return {"errors": "This patient already have a booking in {}".format(data['startTime'].date())}
    elif repo.findAppointmentBetweenDateTime(data) != None:
        return {"errors": "This time already have a booking"}, 400
    else:
        if patient == None:
            patient = repo.create(Patient(data['patient']))

        appointment = Appointment(data)
        appointment.patient = patient
        appointment = repo.create(appointment)

        comment = repo.create(Comment(data['comment']['message'], appointment))
        appointment.comment = comment

        return {"appointment": appointment_schema.dump(appointment)}


@app.route('/appointment/<int:id>', methods=['PUT'])
def update(id):
    appointment = Appointment.query.get(id)
    return {"appointment": appointment.serialize()}


@app.route('/appointments', methods=['GET'])
def showAll():
    appointments = list(
        map(lambda appointment: appointment.serialize(), Appointment.query.all()))
    return {"appointments": appointments}


if __name__ == "__main__":
    app.debug = True
    http_server = WSGIServer((HOST, PORT), app)
    print("server running: {}:{}".format(HOST, PORT))
    http_server.serve_forever()
