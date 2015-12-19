from flask import Flask
from app.models import DATABASE
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = 'andiefniwehg'

basicauth = HTTPBasicAuth()

from app.auth import auth_bp
app.register_blueprint(auth_bp)
from app.ideas.views import idea_bp
app.register_blueprint(idea_bp)

from app.auth.models import User
DATABASE.create_tables([User], safe=True)
