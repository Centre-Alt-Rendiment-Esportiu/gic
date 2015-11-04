from app import app
from flask import render_template, request, flash, session, url_for, redirect
from app.models import User

@app.route('/profile')
def profile():
    if 'email' not in session:
        return redirect(url_for('signin'))
    user = User.query.filter_by(email = session['email']).first()
    if user is None:
        return redirect(url_for('signin'))
    else:
        return render_template('profile.html')