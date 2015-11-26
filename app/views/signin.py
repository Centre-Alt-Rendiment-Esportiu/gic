from app.forms import SigninForm
from app import app
from flask import render_template, request, session, url_for, redirect

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signin.html', form=form)
        else:
            session['email'] = form.email.data
            return redirect(url_for('profile'))               
    elif request.method == 'GET':
        return render_template('signin.html', form=form)

