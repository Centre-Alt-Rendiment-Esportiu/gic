from app import app
from flask import session, url_for, redirect

@app.route('/signout')
def signout():
    """tancar la sessio"""
    if 'email' not in session and 'email_usu' not in session:
        return redirect(url_for('signin'))
    session.pop('email', None)
    session.pop('email_usu', None)
    return redirect(url_for('index'))
