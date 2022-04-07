from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     data = db.Column(db.String(10000))
#     date = db.Column(db.DateTime(timezone=True), default=func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey('User.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    # notes = db.relationship('Note')
    # host_orders = db.relationship('HostOrder')
    #participant_orders = db.relationship('ParticipantOrder')

#class Restaurant(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    # restaurant_name = db.Column(db.String(150))

#class Payment_Methods(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    
    # pay_method = db.Column(db.String(50))

#class User(db.Model, UserMixin):
    # id_user = db.Column(db.Integer, primary_key=True)
    # email = db.Column(db.String(150), unique=True)
    # password = db.Column(db.String(150))
    # first_name = db.Column(db.String(150))
    # host_orders = db.relationship('HostOrder')
    # participant_orders = db.relationship('ParticipantOrder')


class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_name = db.Column(db.String(150))


#class ParticipantOrder(db.Model):
    # id_participant_order = db.Column(db.Integer, primary_key=True)
    # id_participant_user = db.Column(db.Integer, db.ForeignKey('user.id_user'))
    # id_host_order = db.Column(db.Integer, db.ForeignKey('hostorder.id_host_order'))
    # payment_in = db.Column(db.String)
    # price = db.Column(db.Float)
    # Description = db.Column(db.String)
    # IsAccepted = db.Column(db.Boolean)


class HostOrder(db.Model):
    id_host_order = db.Column(db.Integer, primary_key=True)
    id_host_user = db.Column(db.Integer)
    rest_name = db.Column(db.String(50))
    time = db.Column(db.String(10))
    max_ppl_num = db.Column(db.Integer)
    #payment_methods = db.relationship('PaymentMethod')
    #participant_orders = db.relationship('ParticipantOrder')


class PaymentMethod(db.Model):
    id_pay_method = db.Column(db.Integer, primary_key=True)
    pay_method = db.Column(db.String(50))
    id_order = db.Column(db.Integer)
