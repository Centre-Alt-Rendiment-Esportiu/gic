# -*- coding: utf-8 -*-
"""
@author: dani.ruiz
"""
from flask import render_template, request, flash, redirect, url_for
from app import app, db, login_manager
from app.models import User, Post, GIC_CFG_ROL, GIC_ROL, GIC_CFG_PERMIS, \
GIC_CFG_GRUP, GIC_PERMIS
from flask.ext.mail import Message
from app import mail
from app.token import generate_confirmation_token, confirm_token
from werkzeug import generate_password_hash
from app.forms import emailForm, email_adminForm

@app.route('/enviat', methods=['GET', 'POST'])
def enviat():
    form = emailForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('f_password.html', form=form)
        else:
            correu = request.form['email']
            user = Post.query.filter_by(email1=correu).first()
            token = generate_confirmation_token(correu)

            confirm_url = url_for('confirm_email', token=token, _external=True)
            html = render_template('canvi_pass.html', confirm_url=confirm_url)

            sender=['no-reply@sau.car.edu', user.email1]
            msg = Message('Restablir Password', sender=sender[0], recipients=sender)
            msg.html = html
            mail.send(msg)
            return redirect(url_for('enviat'))            
    elif request.method == 'GET':
        return render_template('enviat.html', form=form)    

@app.route('/enviat_admin', methods=['GET', 'POST'])
def enviat_admin():
    form = email_adminForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('f_password_admin.html', form=form)
        else:
            correu = request.form['email']
            user = User.query.filter_by(email=correu).first()
            token = generate_confirmation_token(correu)

            confirm_url = url_for('confirm_email', token=token, _external=True)
            html = render_template('canvi_pass.html', confirm_url=confirm_url)

            sender=['no-reply@sau.car.edu', user.email]
            msg = Message('Restablir Password', sender=sender[0], recipients=sender)
            msg.html = html
            mail.send(msg)
            return redirect(url_for('enviat_admin'))            
    elif request.method == 'GET':
        return render_template('enviat.html', form=form) 
    

@app.route('/f_password', methods=['GET', 'POST'])
def f_password():
    form = emailForm()
    return render_template('f_password.html', form=form)

@app.route('/f_password_admin', methods=['GET', 'POST'])
def f_password_admin():
    form = email_adminForm()
    return render_template('f_password_admin.html', form=form)
    
@app.route('/confirm/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    if request.method == 'POST':
        email = request.form['email']
        user = Post.query.filter_by(email1=email).first()
        user.pwdhash = generate_password_hash(request.form['password'])
        db.session.commit()
        return redirect(url_for('index'))
    else:
        try:
            email = confirm_token(token)
        except:
            flash('The confirmation link is invalid or has expired.', 'danger')
            return redirect(url_for('error'))
        if email:
            user = Post.query.filter_by(email1=email).first()
            return render_template('reset.html', user=user, email=email)
        else:
            return redirect(url_for('error'))
            
@app.route('/confirm_admin/<token>', methods=['GET', 'POST'])
def confirm_email_admin(token):
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        user.pwdhash = generate_password_hash(request.form['password'])
        db.session.commit()
        return redirect(url_for('index'))
    else:
        try:
            email = confirm_token(token)
        except:
            flash('The confirmation link is invalid or has expired.', 'danger')
            return redirect(url_for('error'))
        if email:
            user = User.query.filter_by(email=email).first()
            return render_template('reset.html', user=user, email=email)
        else:
            return redirect(url_for('error'))
        
@app.route('/error', methods=['GET', 'POST'])
def error():
    return render_template('error.html')
        