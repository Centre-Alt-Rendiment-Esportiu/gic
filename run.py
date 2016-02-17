"""
@dani.ruiz
"""
from app import app
from werkzeug.contrib.fixers import ProxyFix
app.debug = True
app.wsgi_app = ProxyFix(app.wsgi_app)

app.run(host='0.0.0.0', processes=4)
