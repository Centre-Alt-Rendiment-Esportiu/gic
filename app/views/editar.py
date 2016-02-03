# -*- coding: utf-8 -*-
"""
@author: dani.ruiz
"""
from flask import render_template, request, redirect, url_for, session
from app import app, db
from sqlalchemy.orm import load_only
from app.models import User, Post, GIC_CFG_ROL, GIC_ROL, GIC_CFG_PERMIS, \
GIC_CFG_GRUP, GIC_PERMIS

@app.route('/edit/<id>', methods=['POST', 'GET'])
def edit(id):
    """pagina editar persones"""
    if 'email' not in session:
        return render_template('no_permis.html')
    else:
        post = Post.query.get(id)
        tip = GIC_ROL.query.filter_by(id_persona=id)
        rols = GIC_CFG_ROL.query.filter_by(actiu="1")
        grups = GIC_CFG_GRUP.query.filter_by(actiu="1").options(load_only("id_grup"))
        perm_grup = GIC_CFG_PERMIS.query.filter(GIC_CFG_PERMIS.grup.in_(grups))
        perm_asig = GIC_PERMIS.query.filter_by(id_persona=id)
        if request.method == 'POST':
            post.nom = request.form['nom']
            post.cognom1 = request.form['cognom1']
            post.cognom2 = request.form['cognom2']
            post.sexe = request.form['sexe']
            post.dni = request.form['dni']
            post.passport = request.form['passport']
            post.data_naix = request.form['data_naix']
            post.telefon1 = request.form['telefon1']
            post.telefon2 = request.form['telefon2']
            post.email1 = request.form['email1']
            post.email2 = request.form['email2']
            post.actiu = request.form['actiu']
            post.foto = request.form['foto']
            lrols = request.form.getlist('rol')  
    #        for lrol in lrols:
    #            db.session.delete(treu_rol)
    #            db.session.flush()
            grups = request.form.getlist('grup')
    #        for grups in grups:
    #            perm = GIC_CFG_PERMIS.query.filter_by(grup=grups)
    #            for perm in perm:
    #                grups = GIC_PERMIS(post.id, perm.id_permis, request.form['inici_permis'], request.form['fi_permis'])
    #                db.session.add(grups)
    #                db.session.flush()
            db.session.commit()
            return  redirect(url_for('index'))
        return render_template('edit.html', post=post, tip=tip, rols=rols, grups=grups, perm_grup=perm_grup, perm_asig=perm_asig)

@app.route('/edit_rol/<id_rol>', methods=['POST', 'GET'])
def edit_rol(id_rol):
    """pagina editar rols"""
    if 'email' not in session:
        return render_template('no_permis.html')
    else:
        rols = GIC_CFG_ROL.query.get(id_rol)
        if request.method == 'POST':
            rols.actiu = request.form['actiu']
            rols.nom_rol = request.form['nom_rol']
            rols.template = request.form['template']
            db.session.commit()
            return  redirect(url_for('index'))
        return render_template('edit_rol.html', rols=rols)

@app.route('/edit_permis/<id_permis>', methods=['POST', 'GET'])
def edit_permis(id_permis):
    """pagina editar permisos"""
    if 'email' not in session:
        return render_template('no_permis.html')
    else:
        permisos = GIC_CFG_PERMIS.query.get(id_permis)
        if request.method == 'POST':
            permisos.actiu = request.form['actiu']
            permisos.nom_permis = request.form['nom_permis']
            db.session.commit()
            return  redirect(url_for('conf'))
        return render_template('edit_permis.html', permisos=permisos)

@app.route('/edit_grup/<id_grup>', methods=['POST', 'GET'])
def edit_grup(id_grup):
    """pagina editar grups de permisos"""

    if 'email' not in session:
        return render_template('no_permis.html')
    else:
        grups = GIC_CFG_GRUP.query.get(id_grup)
        if request.method == 'POST':
            grups.actiu = request.form['actiu']
            grups.nom_grup = request.form['nom_grup']
            db.session.commit()
            return  redirect(url_for('conf'))
        return render_template('edit_grup.html', grups=grups)
