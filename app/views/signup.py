# -*- coding: utf-8 -*-
"""
@author: dani.ruiz
"""
from flask import render_template, request, flash, redirect, url_for, session
from app import app, db
from app.models import User
from flask.ext.mail import Message, Mail
from app.forms import SignupForm, ContactForm

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if 'email' in session:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signup.html', form=form)
        else:
            newuser = User(form.nom.data, form.cognom.data, form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()
            session['email'] = newuser.email
            return redirect(url_for('profile'))
    elif request.method == 'GET':
        return render_template('signup.html', form=form)