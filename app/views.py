"""
@dani.ruiz
"""
import ldap
from flask import render_template, request, flash, redirect, url_for, Blueprint, g
from flask.ext.login import current_user, login_user, logout_user, login_required
from sqlalchemy import or_
from app import app, db, login_manager
from app.models import User, LoginForm, Post, GIC_CFG_ROL, GIC_ROL, GIC_CFG_PERMIS, GIC_PERMIS
from werkzeug import secure_filename
import os

auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(id):
    """get user id for login"""
    return User.query.get(int(id))

@auth.before_request
def get_current_user():
    """current user"""
    g.user = current_user

@auth.route('/conf', methods=['GET','POST'])
def conf():
    rols = GIC_CFG_ROL.query.all()
    return render_template('configuracio.html',rols=rols)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """login"""
    if current_user.is_authenticated():
        flash('you are already logged in.')
        return redirect(url_for('auth.index'))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            User.try_login(username, password)
        except ldap.INVALID_CREDENTIALS:
            flash('Invalid username or password. Try again.', 'danger')
            return render_template('login_fail.html', form=form)
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username, password)
            db.session.add(user)
            db.session.commit()
        login_user(user)
        flash('Succefilly logged in', 'success')
        return redirect(url_for('auth.index'))
    if form.errors:
        flash(form.errors, 'danger')
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    """logout"""
    logout_user()
    return redirect(url_for('auth.index'))

def allowed_file(filename):
    """comprova les extensions dels arxius"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/add', methods=['POST', 'GET'])
def add():
    """afegi persones"""
    rols = GIC_CFG_ROL.query.filter_by(actiu="1")
    if request.method == 'POST':
        post = Post(request.form['nom'], request.form['cognom1'], request.form['cognom2'], request.form['sexe'], request.form['dni'], request.form['passport'], request.form['data_naix'], request.form['telefon1'], request.form['telefon2'], request.form['email1'], request.form['email2'], request.form['actiu'], request.form['foto'])#,request.form['password'])
        db.session.add(post)
        #tip=GIC_ROL(request.form['rol'])
        #db.session.add(tip)
        db.session.commit()
        return redirect(url_for('upload'))
    return render_template('add.html', rols=rols)

@auth.route('/add_permis', methods=['POST', 'GET'])
def add_permis():
    """afegir permisos"""
    if request.method == 'POST':
        post = GIC_CFG_PERMIS(request.form['nom_permis'], request.form['actiu'])
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('auth.conf'))
    return render_template('add_permis.html')

@app.route('/add_rol', methods=['POST', 'GET'])
def add_rol():
    """afegir rols"""
    if request.method == 'POST':
        post = GIC_CFG_ROL(request.form['nom_rol'], request.form['template'], request.form['actiu'])
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('auth.index'))
    return render_template('add_rol.html')

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    """pujar arxius"""
    if request.method == 'POST':
        file = request.files['foto']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('auth.index'))
    return render_template('up.html')

@app.route('/cerca_per', methods=['POST', 'GET'])
def cerca_per():
    """buscar persones"""
    if request.method == 'POST':
        nom = request.form['cerca']
        conc = "%" + nom + "%"
        post = Post.query.filter(or_(Post.nom.like(conc), Post.cognom1.like(conc)))
        rols = GIC_ROL.query.all()
        #rols = GIC_ROL.query.filter(GIC_ROL.id_persona.like(Post.id))
    return render_template('cerca_persones.html', post=post, rols=rols)

@app.route('/cerca_rol', methods=['POST', 'GET'])
def cerca_rol():
    """buscar rols"""
    if request.method == 'POST':
        nom = request.form['cerca']
        conc = "%" + nom + "%"
        post = GIC_CFG_ROL.query.filter(GIC_CFG_ROL.nom_rol.like(conc))
    return render_template('cerca_rols.html', post=post)

@auth.route('/cerca_permis', methods=['POST', 'GET'])
def cerca_permis():
    """buscar permisos"""
    if request.method == 'POST':
        nom = request.form['cerca']
        conc = "%" + nom + "%"
        post = GIC_CFG_PERMIS.query.filter(GIC_CFG_PERMIS.nom_permis.like(conc))
    return render_template('cerca_permis.html', post=post)

@auth.route('/')
def index():
    """pagina index"""
    post = Post.query.all()
    rols = GIC_CFG_ROL.query.all()
    return render_template('index.html', post=post, rols=rols)

@app.route('/edit/<id>', methods=['POST', 'GET'])
def edit(id):
    """pagina editar persones"""
    post = Post.query.get(id)
    tip = GIC_ROL.query.filter_by(id_persona=id)
    rols = GIC_CFG_ROL.query.filter_by(actiu="1")
    if request.method == 'POST':
        tip.id_rol = request.form['rol']
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
#        post.password = request.form['password']
        db.session.commit()
        return  redirect(url_for('auth.index'))
    return render_template('edit.html', post=post, tip=tip, rols=rols)

@app.route('/edit_rol/<id_rol>', methods=['POST', 'GET'])
def edit_rol(id_rol):
    """pagina editar rols"""
    rols = GIC_CFG_ROL.query.get(id_rol)
    if request.method == 'POST':
        rols.actiu = request.form['actiu']
        rols.nom_rol = request.form['nom_rol']
        rols.template = request.form['template']
        db.session.commit()
        return  redirect(url_for('auth.index'))
    return render_template('edit_rol.html', rols=rols)

@app.route('/edit_permis/<id_permis>', methods=['POST', 'GET'])
def edit_permis(id_permis):
    """pagina editar permisos"""
    permisos = GIC_CFG_PERMIS.query.get(id_permis)
    if request.method == 'POST':
        permisos.actiu = request.form['actiu']
        permisos.nom_permis = request.form['nom_permis']
        db.session.commit()
        return  redirect(url_for('auth.conf'))
    return render_template('edit_permis.html', permisos=permisos)

@app.route('/delete/<id>', methods=['POST', 'GET'])
def delete(id):
    """eliminar persones"""
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('auth.index'))

@app.route('/delete_rol/<id_rol>', methods=['POST', 'GET'])
def delete_rol(id_rol):
    """eliminar rols"""
    rols = GIC_CFG_ROL.query.get(id_rol)
    db.session.delete(rols)
    db.session.commit()
    return redirect(url_for('auth.index'))

@app.route('/delete_permis/<id_permis>', methods=['POST', 'GET'])
def delete_permis(id_permis):
    """eliminar permisos"""
    permisos = GIC_CFG_PERMIS.query.get(id_permis)
    db.session.delete(permisos)
    db.session.commit()
    return redirect(url_for('auth.index'))

