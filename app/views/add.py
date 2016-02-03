# -*- coding: utf-8 -*-
"""
@author: dani.ruiz
"""
from flask import render_template, request, redirect, url_for, session
from app import app, db
from app.models import User, Post, GIC_CFG_ROL, GIC_ROL, GIC_CFG_PERMIS, \
GIC_CFG_GRUP, GIC_PERMIS
from sqlalchemy.orm import load_only

@app.route('/add', methods=['POST', 'GET'])
def add():
    """afegir persones"""
    if 'email' not in session:
        return render_template('no_permis.html')
    else:
        rols = GIC_CFG_ROL.query.filter_by(actiu="1")
        grups = GIC_CFG_GRUP.query.filter_by(actiu="1")
        if request.method == 'POST':                
            post = Post(request.form['nom'], request.form['cognom1'], \
            request.form['cognom2'], request.form['sexe'], request.form['dni'], \
            request.form['passport'], request.form['data_naix'], request.form['telefon1'], \
            request.form['telefon2'], request.form['email1'], request.form['email2'], \
            request.form['actiu'], request.form['foto'], request.form['dni'])
            db.session.add(post)
            db.session.flush()
    ######### Bucle 10000 registres ########
    #        v = 10000
    #        for b in range(v):
    #            bucle = Post(b, b, b, 1, (str(b)+'A'), \
    #            b, '2015/11/15', b, b, (str(b)+'@mail.com'),(str(b)+'@mail.com'),1, b, (str(b)+'@mail.com'))
    #            db.session.add(bucle)
    #            db.session.flush
    ########################################         
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
                tip = GIC_ROL(post.id, li[0], li[1], li[2])
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
                    insert_permis = GIC_PERMIS(post.id, per.id_permis, gru[1], gru[2])
                    db.session.add(insert_permis)
                    db.session.flush()
            db.session.commit()
            return redirect(url_for('upload'))
        return render_template('add.html', rols=rols, grups=grups)

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
