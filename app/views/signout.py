from app.forms import ContactForm, SignupForm, SigninForm
from app import app
from flask import render_template, request, flash, session, url_for, redirect

@app.route('/signout')
def signout():
    if 'email' not in session:
        return redirect(url_for('signin'))
    session.pop('email', None)
    return redirect(url_for('index'))