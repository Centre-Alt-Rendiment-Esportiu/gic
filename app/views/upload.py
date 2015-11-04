# -*- coding: utf-8 -*-
"""
@author: dani.ruiz
"""
import ldap
from flask import render_template, request, flash, redirect, url_for, Blueprint, g
from flask.ext.login import current_user, login_user, logout_user, login_required
from sqlalchemy import or_
from app import app, db, login_manager
from sqlalchemy.orm import load_only
from app.models import User, Post, GIC_CFG_ROL, GIC_ROL, GIC_CFG_PERMIS, \
GIC_CFG_GRUP, GIC_PERMIS
from werkzeug import secure_filename
import os

def allowed_file(filename):
    """comprova les extensions dels arxius"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    """pujar arxius"""
    if request.method == 'POST':
        file = request.files['foto']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
    return render_template('up.html')