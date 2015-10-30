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
from app.models import User, LoginForm, Post, GIC_CFG_ROL, GIC_ROL, GIC_CFG_PERMIS, \
GIC_CFG_GRUP, GIC_PERMIS
from werkzeug import secure_filename
import os

auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(id):
    """get user id for login"""
    return User.query.get(id)

@auth.before_request
def get_current_user():
    """current user"""
    g.user = current_user

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """login"""
    if current_user.is_authenticated():
        flash('you are already logged in.')
        return redirect(url_for('auth.index'))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            User.try_login(username, password)
        except ldap.INVALID_CREDENTIALS:
            flash('Invalid username or password. Try again.', 'danger')
            return render_template('login_fail.html', form=form)
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username, password)
            db.session.add(user)
            db.session.commit()
        login_user(user)
        flash('Succefilly logged in', 'success')
        return redirect(url_for('auth.index'))
    if form.errors:
        flash(form.errors, 'danger')
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    """logout"""
    logout_user()
    return redirect(url_for('auth.index'))