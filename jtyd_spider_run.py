from apps.flask_init import app
from werkzeug.contrib.fixers import ProxyFix


app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ ==  '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=False)