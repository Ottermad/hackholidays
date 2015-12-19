from flask import Flask
from app.models import DATABASE
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = 'andiefniiopaerijoargriudgkjfdorsgwehg'

basicauth = HTTPBasicAuth()

from app.auth import auth_bp
app.register_blueprint(auth_bp)
from app.ideas.views import idea_bp
app.register_blueprint(idea_bp)

from app.auth.models import User
from app.ideas.models import Idea, IdeaVotes
DATABASE.create_tables([User, Idea, IdeaVotes], safe=True)
