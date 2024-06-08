'''Creates an api server interface'''
from .views import api
from flask import Flask
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(api)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


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
    port = getenv('FAL_API_PORT', '5001')
    app.run(host=host, port=port, threaded=True, debug=True)
