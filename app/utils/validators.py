from marshmallow import Schema, fields, validate, ValidationError

class UserRegistrationSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8, max=50))

class UserLoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class TrainSchema(Schema):
    train_number = fields.Str(required=True, validate=validate.Length(min=3, max=10))
    name = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    source = fields.Str(required=True, validate=validate.Length(min=2, max=50))
    destination = fields.Str(required=True, validate=validate.Length(min=2, max=50))
    total_seats = fields.Int(required=True, validate=validate.Range(min=1))
    departure_time = fields.Time(required=True)
    arrival_time = fields.Time(required=True)

class BookingSchema(Schema):
    train_id = fields.Int(required=True)
    source = fields.Str(required=True, validate=validate.Length(min=2, max=50))
    destination = fields.Str(required=True, validate=validate.Length(min=2, max=50))
    booking_date = fields.Date(required=True)
    number_of_seats = fields.Int(required=True, validate=validate.Range(min=1))