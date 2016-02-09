# -*- coding: utf-8 -*-
"""
@author: dani.ruiz
"""
from flask import render_template, request, redirect, url_for, session
from sqlalchemy import or_
from app import app, db
from app.models import User, Post, GIC_CFG_ROL, GIC_ROL, GIC_CFG_PERMIS, \
GIC_CFG_GRUP, GIC_PERMIS, A_GE_CAR_PERSONA

@app.route('/llista_per', methods=['POST', 'GET'])
@app.route('/llista_per/<int:page>', methods=['POST', 'GET'])
def llista_per(page=1):
    if 'email' not in session:
        return render_template('no_permis.html')
    else:
        """buscar persones"""
        nom = session['cerca']
        conc = "%" + nom + "%"
        post = Post.query.filter(or_(Post.nom.ilike(conc), Post.cognom1.ilike(conc))).paginate(page, 5, False)
        return render_template('llista_persones.html', post=post)

@app.route('/llista_per_gecar', methods=['POST', 'GET'])
@app.route('/llista_per_gecar/<int:page>', methods=['POST', 'GET'])
def llista_per_gecar(page=1):
    if 'email' not in session:
        return render_template('no_permis.html')
    else:
        """buscar persones gecar"""
        nom = session['cerca_gecar']
        conc = "%" + nom + "%"
        post = A_GE_CAR_PERSONA.query.filter(or_(A_GE_CAR_PERSONA.nom.ilike(conc), A_GE_CAR_PERSONA.cognom1.ilike(conc))).paginate(page, 10, False)
        return render_template('llista_persones_gecar.html', post=post)

@app.route('/cerca_per', methods=['POST', 'GET'])
def cerca_per():
    """buscar persones"""
    if 'email' not in session:
        return render_template('no_permis.html')
    else:
        if request.method == 'POST':
            session['cerca'] = request.form['cerca']
            return redirect(url_for('llista_per'))

@app.route('/cerca_per_gecar', methods=['POST', 'GET'])
def cerca_per_gecar():
    """buscar persones gecar"""
    if 'email' not in session:
        return render_template('no_permis.html')
    else:
        if request.method == 'POST':
            session['cerca_gecar'] = request.form['cerca']
            return redirect(url_for('llista_per_gecar'))

@app.route('/cerca_grup', methods=['POST', 'GET'])
def cerca_grup():
    """buscar grups"""
    if 'email' not in session:
        return render_template('no_permis.html')
    else:
        post = GIC_CFG_GRUP.query.all()
        return render_template('cerca_grup.html', post=post)

@app.route('/cerca_rol', methods=['POST', 'GET'])
def cerca_rol():
    """buscar rols"""
    if 'email' not in session:
        return render_template('no_permis.html')
    else:
        if request.method == 'POST':
            nom = request.form['cerca']
            conc = "%" + nom + "%"
            post = GIC_CFG_ROL.query.filter(GIC_CFG_ROL.nom_rol.like(conc))
        return render_template('cerca_rols.html', post=post)

@app.route('/cerca_permis', methods=['POST', 'GET'])
def cerca_permis():
    """buscar permisos"""
    if 'email' not in session:
        return render_template('no_permis.html')
    else:
        if request.method == 'POST':
            nom = request.form['cerca']
            conc = "%" + nom + "%"
            post = GIC_CFG_PERMIS.query.filter(GIC_CFG_PERMIS.nom_permis.like(conc))
        return render_template('cerca_permis.html', post=post)
