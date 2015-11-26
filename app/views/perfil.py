from app import app, db
from flask import render_template, request, session, url_for, redirect
from app.models import User, Post
from werkzeug import generate_password_hash

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
    post = Post.query.get(id)
    if request.method == 'POST':
        post = Post.query.get(id)
        post.pwdhash = generate_password_hash(request.form['password'])
        db.session.commit()
        return redirect(url_for('correcte'))
    return render_template('reset.html', post=post)

@app.route('/canvi_password_admin/<uid>', methods=['GET', 'POST'])
def canvi_password_admin(uid):
    """canvi de password per admins"""
    user = User.query.get(uid)
    if request.method == 'POST':
        user = User.query.get(uid)
        user.pwdhash = generate_password_hash(request.form['password'])
        db.session.commit()
        return redirect(url_for('correcte'))
    return render_template('reset.html', user=user)

@app.route('/correcte', methods=['GET', 'POST'])
def correcte():
    """pagina del canvi correcte"""
    return render_template('correcte.html')
