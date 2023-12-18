from flask import Blueprint, render_template, session,request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
#from website.database import add_user
from werkzeug.security import generate_password_hash ,check_password_hash
import re
import mysql.connector

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email= request.form['email']
        password = request.form['password']
        mydb = mysql.connector.connect(
        host="aws.connect.psdb.cloud",
        user="v7ksxyhwiyvck3ehk73z",
        password="pscale_pw_UihWfqn6aKIfFKGfV0fPgFjxrlf1GF5InL02NlBjRU1")

        mycursor = mydb.cursor()
        sql='SELECT * FROM user WHERE email = %s'
        mycursor.execute(sql, (email,))
        user = mycursor.fetchone()
        print(user)
        if user:
            hashed_password = user[3]  # Assuming the hashed password is in the fourth column.
            if check_password_hash(hashed_password, password):
               session['loggedin'] = True
               session['userid'] = user[0]
               session['name'] = user[1]
               session['email'] = user[2]
               print(type(session))
               mesage = 'Logged in successfully !'
               return render_template('home.html', mesage = mesage)
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage = mesage)


@auth.route('/logout')
def logout():
    session['loggedin']=False
    session.pop('userid', None)
    session.pop('email', None)
    print(session)
    return render_template('login.html')
  

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    mesage = ''
    print(request.form)

    if request.method == 'POST' and 'firstName' in request.form and 'password1' in request.form and 'email' in request.form :
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        password = request.form['password1']
        print(request.form)
        hash_password=generate_password_hash(password, "sha256")
        email = request.form['email']
        mydb = mysql.connector.connect(
        host="aws.connect.psdb.cloud",
        user="v7ksxyhwiyvck3ehk73z",
        password="pscale_pw_UihWfqn6aKIfFKGfV0fPgFjxrlf1GF5InL02NlBjRU1"
        )
        print(firstName,lastName ,password ,email )
        mycursor = mydb.cursor()
        sql='SELECT * FROM user WHERE first_name = %s'
        mycursor.execute(sql, (firstName,))
        account = mycursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not firstName or not lastName or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            sql = "INSERT INTO user (first_name, email,password,lastname) VALUES (%s, %s, %s,%s)"
            val =  (firstName, email, hash_password ,lastName) 
            mycursor.execute(sql, val)
            mesage = 'You have successfully registered !'
            mydb.commit()

    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('sign_up.html', mesage = mesage)
    
    
