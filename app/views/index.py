# -*- coding: utf-8 -*-
"""
@author: dani.ruiz
"""
from flask import render_template, request, flash, redirect, url_for
from sqlalchemy import or_
from app import app, db, login_manager
from app.models import User, Post, GIC_CFG_ROL, GIC_ROL, GIC_CFG_PERMIS, \
GIC_CFG_GRUP, GIC_PERMIS
from app.forms import ContactForm, SignupForm, SigninForm

@app.route('/')
def index():
    """pagina index"""
    form = SigninForm()
    post = Post.query.all()
    rols = GIC_CFG_ROL.query.all()
    return render_template('index.html', post=post, rols=rols, form=form)
    
@app.route('/conf', methods=['GET', 'POST'])
def conf():
    rols = GIC_CFG_ROL.query.all()
    return render_template('configuracio.html', rols=rols)
