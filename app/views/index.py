# -*- coding: utf-8 -*-
"""
@author: dani.ruiz
"""
from flask import render_template, request, redirect, url_for, session
from app import app
from app.forms import Inici_Clients_Form

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
    """pagina de configuracio"""
    if 'email' not in session:
        return render_template('no_permis.html')
    else:
        return render_template('configuracio.html')
