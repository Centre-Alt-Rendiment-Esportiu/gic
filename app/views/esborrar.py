# -*- coding: utf-8 -*-
"""
@author: dani.ruiz
"""

from flask import render_template, request, flash, redirect, url_for
from flask.ext.login import current_user, login_user, logout_user, login_required
from sqlalchemy import or_
from app import app, db, login_manager
from app.models import User, Post, GIC_CFG_ROL, GIC_ROL, GIC_CFG_PERMIS, \
GIC_CFG_GRUP, GIC_PERMIS

@app.route('/delete/<id>', methods=['POST', 'GET'])
def delete(id):
    """eliminar persones"""
    gic_rol = GIC_ROL.query.filter_by(id_persona=id)
    gic_permis = GIC_PERMIS.query.filter_by(id_persona=id)
    post = Post.query.get(id)
    for gic_rol in gic_rol:
        db.session.delete(gic_rol)
        db.session.flush()
    for gic_permis in gic_permis:
        db.session.delete(gic_permis)
        db.session.flush()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_rol/<id_rol>', methods=['POST', 'GET'])
def delete_rol(id_rol):
    """eliminar rols"""
    rols = GIC_CFG_ROL.query.get(id_rol)
    db.session.delete(rols)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_grup/<id_grup>', methods=['POST', 'GET'])
def delete_grup(id_grup):
    """eliminar grups"""
    grup = GIC_CFG_GRUP.query.get(id_grup)
    db.session.delete(grup)
    db.session.commit()
    return redirect(url_for('conf'))

@app.route('/delete_permis/<id_permis>', methods=['POST', 'GET'])
def delete_permis(id_permis):
    """eliminar permisos"""
    permisos = GIC_CFG_PERMIS.query.get(id_permis)
    db.session.delete(permisos)
    db.session.commit()
    return redirect(url_for('index'))