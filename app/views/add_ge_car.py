# -*- coding: utf-8 -*-
"""
@author: dani.ruiz
"""
from flask import render_template, request, redirect, url_for, session
from app import app, db
from app.models import User, Post, GIC_CFG_ROL, GIC_ROL, GIC_CFG_PERMIS, \
GIC_CFG_GRUP, GIC_PERMIS, A_GE_CAR_PERSONA
import datetime
from sqlalchemy.orm import load_only

def data_gecar(data):
    if data == '':
        return ''
    elif data:
        return datetime.datetime.strptime(data,'%Y-%m-%d').date()

@app.route('/add-ge-car', methods=['POST', 'GET'])
def add_ge_car():
    """afegir persones a GECAR"""
    if 'email' not in session:
        return render_template('no_permis.html')
    else:
        rols = GIC_CFG_ROL.query.filter_by(actiu="1")
        grups = GIC_CFG_GRUP.query.filter_by(actiu="1")
        if request.method == 'POST':                
            post = A_GE_CAR_PERSONA(request.form['foto'], request.form['dni'], \
            request.form['passaport'], request.form['nom'], request.form['cognom1'], \
            request.form['cognom2'], request.form['sexe'], request.form['ss'], \
            request.form['tipus'], data_gecar(request.form['data_neix']), request.form['lloc_neix'], \
            request.form['provincia_neix'], request.form['comarca_neix'], request.form['auto_neix'], \
            request.form['pais_neix'], request.form['direccio'], request.form['poblacio'], \
            request.form['provincia'], request.form['cp'], request.form['comarca'], \
            request.form['autonomia'], request.form['pais'], request.form['telefon1'], \
            request.form['telefon2'], request.form['e_mail'], request.form['estudis_act'], \
            request.form['nivel_academic'], request.form['tipus_centre'],request.form['nom_centre'], \
            request.form['aceptacio'], request.form['revisiom'], request.form['revisiops'], \
            request.form['fitxacomplerta'], request.form['vehicle'], request.form['matricula'], \
            request.form['tutor1'], request.form['contacto1'], request.form['tutor2'], \
            request.form['contacto2'], request.form['actiu'], request.form['identificador_ant'], \
            request.form['id_med'], request.form['id_fis'], request.form['id_psi'], \
            request.form['cip'], request.form['consentiment'], \
            data_gecar(request.form['data_consentiment']), data_gecar(request.form['data_revisiom']), \
            request.form['consentiment_dad'], request.form['consentiment_proinf'], \
            request.form['pro_sal_es'], request.form['e_mail2'], 'randompassword', 'randomsalt')
            db.session.add(post)
            db.session.flush()      
            lrol = request.form.getlist('rol')
            lini = request.form.getlist('inici')
            lfi = request.form.getlist('fi')
            i = len(lrol)
            j = len(lini)
            k = len(lfi)
            lista = []
            listaini = []
            listafi = []
            a = 0
            li = 0
            lf = 0
            for le in range(j):
                if lini[le]:
                    listaini.insert(le, lini[le])
            for lf in range(k):
                if lfi[lf]:
                    listafi.insert(lf, lfi[lf])
            for a in range(i):
                lista.insert(a, [lrol[a], listaini[a], listafi[a]])
            for li in lista:
                tip = GIC_ROL(post.identificador, li[0], li[1], li[2])
                db.session.add(tip)
                db.session.flush()
            lgrups = request.form.getlist('grup')
            lini_g = request.form.getlist('inici_permis')
            lfi_g = request.form.getlist('fi_permis')
            h = len(lgrups)
            l = len(lini_g)
            u = len(lfi_g)
            lista_grups = []
            listaini_grups = []
            listafi_grups = []
            for le_g in range(l):
                if lini_g[le_g]:
                    listaini_grups.insert(le_g, lini_g[le_g])
            for lf_g in range(u):
                if lfi_g[lf_g]:
                    listafi_grups.insert(lf_g, lfi_g[lf_g])
            for a in range(h):
                lista_grups.insert(a, [lgrups[a], listaini_grups[a], listafi_grups[a]])
            for gru in lista_grups:
                perm = GIC_CFG_PERMIS.query.filter_by(grup=gru[0])
                for per in perm:
                    insert_permis = GIC_PERMIS(post.identificador, per.id_permis, gru[1], gru[2])
                    db.session.add(insert_permis)
                    db.session.flush()
            db.session.commit()
            return redirect(url_for('upload'))
        return render_template('add_gecar.html', rols=rols, grups=grups)


@app.route('/add_permis', methods=['POST', 'GET'])
def add_permis():
    """afegir permisos"""
    if 'email' not in session:
        return render_template('no_permis.html')
    else:
        grups = GIC_CFG_GRUP.query.filter_by(actiu="1")
        if request.method == 'POST':
            post = GIC_CFG_PERMIS(request.form['nom_permis'], request.form['actiu'], \
            request.form['grup'])
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('conf'))
        return render_template('add_permis.html', grups=grups)

@app.route('/add_rol', methods=['POST', 'GET'])
def add_rol():
    """afegir rols"""
    if 'email' not in session:
        return render_template('no_permis.html')
    else:
        if request.method == 'POST':
            post = GIC_CFG_ROL(request.form['nom_rol'], request.form['template'], request.form['actiu'])
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('add_rol.html')

@app.route('/add_grup', methods=['POST', 'GET'])
def add_grup():
    """afegir grups"""
    if 'email' not in session:
        return render_template('no_permis.html')
    else:
        if request.method == 'POST':
            post = GIC_CFG_GRUP(request.form['nom_grup'], request.form['actiu'])
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('conf'))
        return render_template('add_grup.html')

