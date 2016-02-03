from app import app, db
from flask import render_template, request, session, url_for, redirect
from app.models import User, Post, GIC_CFG_ROL, GIC_ROL, GIC_CFG_PERMIS, \
GIC_CFG_GRUP, GIC_PERMIS
from sqlalchemy.orm import load_only
from werkzeug import generate_password_hash
from sqlalchemy import create_engine
import hashlib
from sqlalchemy import text
import re

@app.route('/profile')
def profile():
    """redirecciona a la pagina perfil depenent si un usuari es admin o no o si no hi ha sessio"""
    if 'email' not in session and 'email_usu' not in session:
        return redirect(url_for('signin'))
    elif 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('profile.html', user=user)
    elif 'email_usu' in session:
        post_user = Post.query.filter_by(email1=session['email_usu']).first()
        return render_template('profile.html', post_user=post_user)

@app.route('/canvi_password/<id>', methods=['GET', 'POST'])
def canvi_password(id):
    """canvia de password """
    correu = session['email_usu']
    sql = text("select id from A_GIC_PERSONA where email1 like '%s' ;"%correu)
    result = db.engine.execute(sql)
    names = []
    for row in result:
        names.append(row[0])
    if 'email_usu' not in session or str(id) != str(names[0]):
        return render_template('no_permis.html')
    else:
        post = Post.query.get(id)
        if request.method == 'POST':
            post = Post.query.get(id)
            post.pwdhash = hashlib.sha256('[B@3f13a310' + request.form['password']).hexdigest()
            db.session.commit()
            return redirect(url_for('correcte'))
        return render_template('reset.html', post=post)

@app.route('/canvi_password_admin/<id>', methods=['GET', 'POST'])
def canvi_password_admin(id):
    """canvi de password per admins"""
    correu = session['email']
    sql = text("select id from A_GIC_ADMIN where email like '%s' ;"%correu)
    result = db.engine.execute(sql)
    names = []
    for row in result:
        names.append(row[0])
    if 'email' not in session or str(id) != str(names[0]):
        return render_template('no_permis.html')
    else:
        user = User.query.get(id)
        if request.method == 'POST':
            user = User.query.get(id)
            user.pwdhash = hashlib.sha256('[B@3f13a310' + request.form['password']).hexdigest()
            db.session.commit()
            return redirect(url_for('correcte'))
        return render_template('reset.html', user=user)

@app.route('/correcte', methods=['GET', 'POST'])
def correcte():
    """pagina del canvi correcte"""
    if 'email' not in session and 'email_usu' not in session:
        return render_template('no_permis.html')
    else:
        return render_template('correcte.html')

@app.route('/perfil/<id>', methods=['POST', 'GET'])
def perfil(id):
    """Veure de persones"""
    if 'email' not in session:
        return render_template('no_permis.html')
    else:
        post = Post.query.get(id)
        tip = GIC_ROL.query.filter_by(id_persona=id)
        rols = GIC_CFG_ROL.query.filter_by(actiu="1")
        grups = GIC_CFG_GRUP.query.filter_by(actiu="1").options(load_only("id_grup"))
        perm_grup = GIC_CFG_PERMIS.query.filter(GIC_CFG_PERMIS.grup.in_(grups))
        perm_asig = GIC_PERMIS.query.filter_by(id_persona=id)
        return render_template('perfil.html', post=post, tip=tip, rols=rols, grups=grups, perm_grup=perm_grup, perm_asig=perm_asig)    
