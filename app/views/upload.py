# -*- coding: utf-8 -*-
"""
@author: dani.ruiz
"""

from flask import render_template, request, redirect, url_for, jsonify, session, make_response
from app import app
from werkzeug import secure_filename
import os
import csv
import requests
import json
import urllib2
from cStringIO import StringIO

def allowed_file(filename):
    """comprova les extensions dels arxius"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    """pujar arxius"""
    if 'email' not in session:
        return render_template('no_permis.html')
    else:
        if request.method == 'POST':
            file = request.files['foto']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('index'))
        return render_template('up.html')

@app.route('/upload_csv', methods=['POST', 'GET'])
def upload_csv():
    """pujar arxius csv"""
    if 'email' not in session:
        return render_template('no_permis.html')
    else:
        if request.method == 'POST':
            f = request.files['data_file']
            if not f:
                return "No file"
            file_contents = StringIO(f.stream.read())
            reader = csv.DictReader(file_contents)
            out = []
            for row in reader:
                out = row
#            print out
#        out = json.dumps([ row for row in reader ])
            dataj = json.dumps({"data": {"type":"users","attributes": out}}, sort_keys=True)
            url = "http://127.0.0.1:5000/persones.json"
            headers = {'content-type': "application/json", 'cache-control': "no-cache", 'postman-token': "72921f98-7d3e-c7be-72e6-50fad56c1eb3"}
            response = requests.request("POST", url, data=dataj, headers=headers)
#            print response.raise_for_status()
            return redirect(url_for('index'))
        return render_template('up_csv.html')
