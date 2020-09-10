from marshmallow import Schema, fields, INCLUDE, validate


class CommentSchema(Schema):
    id = fields.Int(dump_only=True)
    message = fields.Str(required=True, validate=[
        validate.Length(min=20, max=1000)])


class PatientSchema(Schema):
    id = fields.Int(dump_only=True)
    firstName = fields.Str(required=True, validate=[
                           validate.Length(min=2, max=50)])
    lastName = fields.Str(required=True, validate=[
                          validate.Length(min=2, max=50)])
    middleName = fields.Str(required=True, validate=[
        validate.Length(min=2, max=50)])


class AppointmentSchema(Schema):
    id = fields.Int(dump_only=True)
    startTime = fields.DateTime(required=True)
    endTime = fields.DateTime(required=True)
    comment = fields.Nested(CommentSchema, required=True)
    patient = fields.Nested(PatientSchema, required=True)


patient_schema = PatientSchema()
appointment_schema = AppointmentSchema()
