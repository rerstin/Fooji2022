from curses import def_prog_mode
import email
from hashlib import new
from operator import ne
from time import time
from unicodedata import name
from xml.sax.handler import feature_validation
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Restaurant, HostOrder, PaymentMethod, ParticipantOrder
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import sqlite3 as sql
import random 
from os import path
auth = Blueprint('auth', __name__)



@auth.route('/login', methods=['GET', 'POST'])
def login():
    user = User.query.filter_by().first()
    if not user:
        print('update')
        populate_database()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('fullName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)


times = ['12:00', '14:15', '13:56', '04:12', '10:15']


restaurants_list = {'1': 'Menza',
                    '2': 'Papa Jhons', 
                    '3': 'Moti Sushi',
                    '4': 'Sufersal',
                    '5': 'Rami Levi',
                    '6': 'Macdonalds',
                    '7': 'Jahnun Afula'}

payment_methods = {'1': 'Bit',
                   '2': 'Cashe', 
                   '3': 'PayBox', 
                   '4': 'ApplePay', 
                   '5': 'Bitcoin', 
                   '6': 'Dogecoin'}

def_all = {'0': 'All'}

def populate_users():
    names = ['Kostya', 'Yonatan', 'Shaked', 'Daniel', 'Michael']
    email_str = '@mail.huji.ac.il'
    passwords = names
    for name in names:
        new_user = User(first_name = name, 
                            password = name, 
                            email = name + email_str)
        db.session.add(new_user)
    db.session.commit()


def create_def_order(user):
    rand_rest = random.randint(1, len(restaurants_list))
    rand_time = random.randint(1, len(times))
    rand_num = random.randint(1, 100)
    rand_com = random.randint(1, 10)
    new_order = HostOrder(id_host_user = user.id, 
                          rest_name = restaurants_list[str(rand_rest)], 
                          time = times[rand_time],
                          commission = rand_com,
                          max_ppl_num = rand_num)
    db.session.add(new_order)
    populate_partOrders(new_order, user)


def populate_partOrders(hostOrder, user):
    participant = User.query.filter(id != user.id).first()
    rand_method = random.randint(1, len(payment_methods))
    rand_price = random.randint(1, 100)
    new_order = ParticipantOrder(id_host_order = hostOrder.id_host_order, 
                                 participant_id = participant.id,
                                 payment_in = payment_methods[str(rand_method)], 
                                 price = rand_price,
                                 Description = "Some description...", 
                                 IsAccepted = bool(random.randint(0,1)))
    db.session.add(new_order)


def populate_HostOrders():
    users = User.query.filter_by()
    for user in users:
        #print(user.first_name)
        create_def_order(user)


def populate_database():
    populate_users()
    populate_HostOrders()
    db.session.commit()
    print('database udated succesfully')


@auth.route('/create-order', methods=['GET', 'POST'])
def create_order():
    if request.method == 'POST':
        accepted_methods = request.form.getlist('mycheckbox')    
        restaurant = request.form.get('rest_choice')
        order_time = request.form.get('order_time')
        part_num = request.form.get('participants_max_num')
        commission = request.form.get('commission') 
        if len(accepted_methods) == 0:
            flash('Choose payment methods.', category='error')
        elif len(restaurant) == 0:
            flash('Choose restaurant.', category='error')
        elif len(order_time) == 0:
            flash('Choose order time.', category='error')
        elif len(part_num) == 0:
            flash('Choose maximum number of participants.', category='error')
        elif len(commission) == 0:
            flash('Choose wonder commission.', category='error')
        elif int(commission) < 0:
            flash('Choose wonder commission.', category='error')
        else:
            new_order = HostOrder(id_host_user = 100, 
                                  rest_name = restaurants_list[restaurant],
                                  time = order_time,
                                  commission = commission,
                                  max_ppl_num = part_num)
            db.session.add(new_order)                      
            for elem in accepted_methods:
                order_pay = PaymentMethod(pay_method = payment_methods[elem], 
                id_order = new_order.id_host_order)
                db.session.add(order_pay)
            db.session.commit()  
            print(type(order_time))
    return render_template("creation_order.html",rest_list=restaurants_list, methods_list=payment_methods) 


# @auth.route('/join_order', methods=['GET', 'POST'])
# def join_order():
    
 