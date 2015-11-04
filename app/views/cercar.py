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

@app.route('/cerca_per', methods=['POST', 'GET'])
def cerca_per():
    """buscar persones"""
    if request.method == 'POST':
        nom = request.form['cerca']
        conc = "%" + nom + "%"
        post = Post.query.filter(or_(Post.nom.like(conc), Post.cognom1.like(conc)))
        rols = GIC_ROL.query.all()
    return render_template('cerca_persones.html', post=post, rols=rols)

@app.route('/cerca_grup', methods=['POST', 'GET'])
def cerca_grup():
    """buscar grups"""
    post = GIC_CFG_GRUP.query.all()
    return render_template('cerca_grup.html', post=post)

@app.route('/cerca_rol', methods=['POST', 'GET'])
def cerca_rol():
    """buscar rols"""
    if request.method == 'POST':
        nom = request.form['cerca']
        conc = "%" + nom + "%"
        post = GIC_CFG_ROL.query.filter(GIC_CFG_ROL.nom_rol.like(conc))
    return render_template('cerca_rols.html', post=post)

@app.route('/cerca_permis', methods=['POST', 'GET'])
def cerca_permis():
    """buscar permisos"""
    if request.method == 'POST':
        nom = request.form['cerca']
        conc = "%" + nom + "%"
        post = GIC_CFG_PERMIS.query.filter(GIC_CFG_PERMIS.nom_permis.like(conc))
    return render_template('cerca_permis.html', post=post)