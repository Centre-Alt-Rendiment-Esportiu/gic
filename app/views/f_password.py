# -*- coding: utf-8 -*-
"""
@author: dani.ruiz
"""
from flask import render_template, request, redirect, url_for, session
from app import app, db
from app.models import User, Post, A_GE_CAR_PERSONA
from flask.ext.mail import Message
from app import mail
from app.token import generate_confirmation_token, confirm_token
from werkzeug import generate_password_hash
from app.forms import emailForm, email_adminForm
import hashlib

@app.route('/enviat', methods=['GET', 'POST'])
def enviat():
    """confirma i envia el email per canviar password"""
    form = emailForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('f_password.html', form=form)
        else:
            correu = request.form['email']
            user = A_GE_CAR_PERSONA.query.filter_by(e_mail=correu).first()
            token = generate_confirmation_token(correu)
            confirm_url = url_for('confirm_email', token=token, _external=True)
            html = render_template('canvi_pass.html', confirm_url=confirm_url)
            sender = ['no-reply@sau.car.edu', user.e_mail]
            msg = Message('Restablir Password', sender=sender[0], recipients=sender)
            msg.html = html
            mail.send(msg)
            return redirect(url_for('enviat'))
    elif request.method == 'GET':
        return render_template('enviat.html', form=form)

@app.route('/enviat_admin', methods=['GET', 'POST'])
def enviat_admin():
    """confirma i envia el email per canviar password per administradors"""
    form = email_adminForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('f_password_admin.html', form=form)
        else:
            correu = request.form['email']
            user = User.query.filter_by(email=correu).first()
            token = generate_confirmation_token(correu)
            confirm_url = url_for('confirm_email_admin', token=token, _external=True)
            html = render_template('canvi_pass.html', confirm_url=confirm_url)
            sender = ['no-reply@sau.car.edu', user.email]
            msg = Message('Restablir Password', sender=sender[0], recipients=sender)
            msg.html = html
            mail.send(msg)
            return redirect(url_for('enviat_admin'))
    elif request.method == 'GET':
        return render_template('enviat.html', form=form)

@app.route('/f_password', methods=['GET', 'POST'])
def f_password():
    """formulari on s'ha d'enviar el correu de canvi de password"""
    form = emailForm()
    return render_template('f_password.html', form=form)

@app.route('/f_password_admin', methods=['GET', 'POST'])
def f_password_admin():
    """formulari on s'ha d'enviar el correu de canvi de password per admins"""
    form = email_adminForm()
    return render_template('f_password_admin.html', form=form)

@app.route('/confirm/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    """confirma el token del correu i canvia el password"""
    if request.method == 'POST':
        email = request.form['email']
        user = A_GE_CAR_PERSONA.query.filter_by(e_mail=email).first()
        user.password = hashlib.sha256('[B@3f13a310' + request.form['password']).hexdigest()
        db.session.commit()
        return redirect(url_for('index'))
    else:
        try:
            email = confirm_token(token)
        except:
            return redirect(url_for('error'))
        if email:
            user = A_GE_CAR_PERSONA.query.filter_by(e_mail=email).first()
            return render_template('reset.html', user=user, email=email)
        else:
            return redirect(url_for('error'))

@app.route('/confirm_admin/<token>', methods=['GET', 'POST'])
def confirm_email_admin(token):
    """confirma el token del correu i canvia el password per admins"""
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        user.pwdhash = hashlib.sha256('[B@3f13a310' + request.form['password']).hexdigest()
        db.session.commit()
        return redirect(url_for('index'))
    else:
        try:
            email = confirm_token(token)
        except:
            return redirect(url_for('error'))
        if email:
            user = User.query.filter_by(email=email).first()
            return render_template('reset.html', user=user, email=email)
        else:
            return redirect(url_for('error'))

@app.route('/error', methods=['GET', 'POST'])
def error():
    """pagina d'error en cas de no poder confirmar el token"""
    return render_template('error.html')
