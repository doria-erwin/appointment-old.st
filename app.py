from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Text, ForeignKey, String, DateTime, Boolean, update
from sqlalchemy.orm.exc import NoResultFound
from gevent.pywsgi import WSGIServer
from config import HOST, PORT
from service import Service
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

    def __init__(self, data):
        self.message = data['message']

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
    appointment_id = Column(Integer, ForeignKey('appointment.id'))
    appointment = db.relationship("Appointment", back_populates="patient")

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
    patient = db.relationship(
        "Patient", uselist=False, back_populates="appointment", lazy='joined')

    def __init__(self, data):
        self.startTime = data['startTime']
        self.endTime = data['endTime']
        self.patient = Patient(data['patient'])
        self.comment = Comment(data['comment'])

    def update(self, data):
        self.startTime = data['startTime']
        self.endTime = data['endTime']
        Patient.query.filter(
            Patient.id == data['patient']['id']).update(data['patient'])
        Comment.query.filter(
            Comment.id == data['comment']['id']).update(data['comment'])
        db.session.commit()

    def serialize(self):
        return{
            "id": self.id,
            "startTime": self.startTime,
            "endTime": self.endTime,
            "comment": self.comment.serialize(),
            "patient": self.patient.serialize()
        }


db.create_all()

service = Service(db.session, Appointment, Patient, Comment)


@app.route('/appointment', methods=['POST'])
def create():
    return service.create(request)


@app.route('/appointment/<int:id>', methods=['PUT'])
def updateAppointment(id):
    return service.update(request, id)


@app.route('/appointments', methods=['GET'])
def showAll():
    return service.show(request)


@app.route('/appointment/<int:id>', methods=['DELETE'])
def delete(id):
    return service.delete(id)


if __name__ == "__main__":
    app.debug = True
    http_server = WSGIServer((HOST, PORT), app)
    print("server running: {}:{}".format(HOST, PORT))
    http_server.serve_forever()
