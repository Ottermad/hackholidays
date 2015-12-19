from flask import Blueprint, g, jsonify, request
from flask.ext.bcrypt import check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from app import app, basicauth
from .models import User

auth_bp = Blueprint('auth_bp', __name__)


def generate_auth_token(user, expiration=600):
    s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({'id': user.user_id})


def verify_auth_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None    # valid token, but expired
    except BadSignature:
        return None    # invalid token
    try:
        user = User.get(User.user_id == data['id'])
        return user
    except:
        return None


@basicauth.verify_password
def verify_password(email_or_token, password):
    # first try to authenticate by token
    user = verify_auth_token(email_or_token)
    if not user:
        # try to authenticate with email/password
        try:
            user = User.get(User.email == email_or_token)
        except:
            return False
        if not user or not check_password_hash(user.password, password):
            return False
    g.user = user
    return True


@auth_bp.route('/token')
@basicauth.login_required
def get_auth_token():
    token = generate_auth_token(g.user, 600)
    print(token)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@auth_bp.route('/signup', methods=('POST', 'GET'))
def signup():
    try:
        User.add_user(
            email=request.form['email'],
            password=request.form['password']
        )
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
