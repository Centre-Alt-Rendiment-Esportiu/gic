# -*- coding: utf-8 -*-
"""
@author: dani.ruiz
"""
from flask import render_template, request, redirect, url_for, session
from app import app, db
from sqlalchemy.orm import load_only
from app.models import User, GIC_CFG_ROL, GIC_ROL, GIC_CFG_PERMIS, \
GIC_CFG_GRUP, GIC_PERMIS, A_GE_CAR_PERSONA
import datetime

def data_gecar(data):
    if data == '':
        return ''
    elif data:
        return datetime.datetime.strptime(data,'%Y-%m-%d').date()

@app.route('/edit_gecar/<id>', methods=['POST', 'GET'])
def edit_gecar(id):
    """pagina editar persones"""
    if 'email' not in session:
        return render_template('no_permis.html')
    else:
        post = A_GE_CAR_PERSONA.query.get(id)
        tip = GIC_ROL.query.filter_by(id_persona=id)
        rols = GIC_CFG_ROL.query.filter_by(actiu="1")
        grups = GIC_CFG_GRUP.query.filter_by(actiu="1").options(load_only("id_grup"))
        perm_grup = GIC_CFG_PERMIS.query.filter(GIC_CFG_PERMIS.grup.in_(grups))
        perm_asig = GIC_PERMIS.query.filter_by(id_persona=id)
        if request.method == 'POST':
            post.foto = request.form['foto']
            post.dni = request.form['dni']
            post.passaport = request.form['passaport']
            post.nom = request.form['nom']
            post.cognom1 = request.form['cognom1']
            post.cognom2 = request.form['cognom2']
            post.sexe = request.form['sexe']
            post.ss = request.form['ss']
            post.tipus = request.form['tipus']
            post.data_neix = data_gecar(request.form['data_neix'])
            post.lloc_neix = request.form['lloc_neix']
            post.provincia_neix = request.form['provincia_neix']
            post.comarca_neix = request.form['comarca_neix']
            post.auto_neix = request.form['auto_neix']
            post.pais_neix = request.form['pais_neix']
            post.direccio = request.form['direccio']
            post.poblacio = request.form['poblacio']
            post.provincia = request.form['provincia']
            post.cp = request.form['cp']
            post.comarca = request.form['comarca']
            post.autonomia = request.form['autonomia']
            post.pais = request.form['pais']
            post.telefon1 = request.form['telefon1']
            post.telefon2 = request.form['telefon2']
            post.e_mail = request.form['e_mail']
            post.estudis_act = request.form['estudis_act']
            post.nivel_academic = request.form['nivel_academic']
            post.tipus_centre = request.form['tipus_centre']
            post.nom_centre = request.form['nom_centre']
            post.aceptacio = request.form['aceptacio']
            post.revisiom = request.form['revisiom']
            post.revisiops = request.form['revisiops']
            post.fitxacomplerta = request.form['fitxacomplerta']
            post.vehicle = request.form['vehicle']
            post.matricula = request.form['matricula']
            post.tutor1 = request.form['tutor1']
            post.contacto1 = request.form['contacto1']
            post.tutor2 = request.form['tutor2']
            post.contacto2 = request.form['contacto2']
            post.actiu = request.form['actiu']
            post.identificador_ant = request.form['identificador_ant']
            post.id_med = request.form['id_med']
            post.id_fis = request.form['id_fis']
            post.id_psi = request.form['id_psi']
            post.cip = request.form['cip']
            post.consentiment = request.form['consentiment']
            post.data_consentiment = data_gecar(request.form['data_consentiment'])
            post.data_revisiom = data_gecar(request.form['data_revisiom'])
            post.consentiment_dad = request.form['consentiment_dad']
            post.consentiment_proinf = request.form['consentiment_proinf']
            post.pro_sal_es = request.form['pro_sal_es']
            post.e_mail2 = request.form['e_mail2']
            db.session.commit()
            return  redirect(url_for('index'))
        return render_template('edit_gecar.html', post=post, tip=tip, rols=rols, grups=grups, perm_grup=perm_grup, perm_asig=perm_asig)
