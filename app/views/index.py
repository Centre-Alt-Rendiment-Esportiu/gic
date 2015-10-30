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
from app.views.login import auth

@auth.route('/')
def index():
    """pagina index"""
    post = Post.query.all()
    rols = GIC_CFG_ROL.query.all()
    return render_template('index.html', post=post, rols=rols)
    
@auth.route('/conf', methods=['GET', 'POST'])
def conf():
    rols = GIC_CFG_ROL.query.all()
    return render_template('configuracio.html', rols=rols)
