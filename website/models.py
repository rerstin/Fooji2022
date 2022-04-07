from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150))
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))


class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_name = db.Column(db.String(150))


class ParticipantOrder(db.Model):
    id_participant_order = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer)
    id_host_order = db.Column(db.Integer)
    payment_in = db.Column(db.String(50))
    price = db.Column(db.Float)
    Description = db.Column(db.String(50))
    IsAccepted = db.Column(db.Boolean)

class HostOrder(db.Model):
    id_host_order = db.Column(db.Integer, primary_key=True)
    id_host_user = db.Column(db.Integer)
    rest_name = db.Column(db.String(50))
    time = db.Column(db.String(10))
    commission = db.Column(db.Integer)
    max_ppl_num = db.Column(db.Integer)



class PaymentMethod(db.Model):
    id_pay_method = db.Column(db.Integer, primary_key=True)
    pay_method = db.Column(db.String(50))
    id_order = db.Column(db.Integer)
