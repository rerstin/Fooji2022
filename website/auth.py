from operator import ne
from unicodedata import name
from xml.sax.handler import feature_validation
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Restaurant
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import sqlite3 as sql

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
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
        first_name = request.form.get('firstName')
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


restaurants_list = {1: 'Menza',2: 'Papa Jhons'}
payment_methods = ['Bit', 'Cashe', 'PayBox', 'ApplePay']


# def fill_rest():
#     # con = sql.connect('shot_database.db')
#     # # Getting cursor
#     # c =  con.cursor() 
#     for elem in restaurants_list:
#         new_rest = Restaurant(restaurant_name = elem)
#         rest = Restaurant.query.filter_by(restaurant_name = elem).first()
#         if not rest:
#             db.session.add(new_rest)
#         #print(new_rest.restaurant_name)
#             db.session.commit()  

@auth.route('/create-order', methods=['GET', 'POST'])
def create_order():
    #payment_methods=db.execute("SELECT * FROM Payment_Methods order by pay_method")

    rest_list = db.session.execute("SELECT * FROM Restaurant order by restaurant_name")
    # if request.method == 'POST':
    #     accepted_methods = request.form.getlist('mycheckbox')
    #     #rest
    #     print(accepted_methods);
    return render_template("creation_order.html",rest_list=restaurants_list) 
