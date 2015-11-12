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

@app.route('/enviat', methods=['GET', 'POST'])
def enviat():
    if request.method == 'POST':
        correu = request.form['email']
        user = Post.query.filter_by(email1=correu).first()
        token = generate_confirmation_token(correu)

        confirm_url = url_for('confirm_email', token=token, _external=True)
        html = render_template('canvi_pass.html', confirm_url=confirm_url)

        sender=['no-reply@sau.car.edu', correu]
        msg = Message('Restablir Password', sender=sender[0], recipients=sender)
        msg.html = html
        mail.send(msg)
        return redirect(url_for('enviat'))
    return render_template('enviat.html')

@app.route('/f_password', methods=['GET', 'POST'])
def f_password():
    return render_template('f_password.html')
    
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
        user = Post.query.filter_by(email1=email).first()
        return render_template('reset.html', user=user, email=email)
        