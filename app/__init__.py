from flask import Flask
from app.models import DATABASE

app = Flask(__name__)

from app.auth.models import User
DATABASE.create_tables([User], safe=True)
