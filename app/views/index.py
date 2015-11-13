# -*- coding: utf-8 -*-
"""
@author: dani.ruiz
"""
from flask import render_template, request, flash, redirect, url_for, session
from sqlalchemy import or_
from app import app, db, login_manager
from app.models import User, Post, GIC_CFG_ROL, GIC_ROL, GIC_CFG_PERMIS, \
GIC_CFG_GRUP, GIC_PERMIS
from app.forms import ContactForm, SignupForm, SigninForm, Inici_Clients_Form

@app.route('/', methods=['GET', 'POST'])
def index():
    """pagina index"""
    form = Inici_Clients_Form()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('index.html', form=form)
        else:
            session['email_usu'] = form.email.data
            return redirect(url_for('profile'))               
    elif request.method == 'GET':
        return render_template('index.html', form=form)
   
@app.route('/conf', methods=['GET', 'POST'])
def conf():
    return render_template('configuracio.html')
