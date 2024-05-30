'''Creates an api server interface'''
from api.v1.views import app_views
from flask import Flask
from os import getenv


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.route('/')
def _home():
    '''return server status'''
    return "Welcome to Find a locum api interface\n"


@app.errorhandler(404)
def _404(e):
    '''handle 404 error'''
    return {'error': 'Not found'}


if __name__ == '__main__':
    host = getenv('FAL_API_HOST', '0.0.0.0')
    port = getenv('FAL_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True, debug=True)
