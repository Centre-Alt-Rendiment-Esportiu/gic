# -*- coding: utf-8 -*-
"""
@author: dani.ruiz
"""
from flask import render_template, request, redirect, url_for
from app import app
from werkzeug import secure_filename
import os

def allowed_file(filename):
    """comprova les extensions dels arxius"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    """pujar arxius"""
    if request.method == 'POST':
        file = request.files['foto']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
    return render_template('up.html')
