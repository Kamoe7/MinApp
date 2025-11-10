from flask import Flask, jsonify, request
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from functools import wraps
from config import Config


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'Error': 'Token format invalid'}), 401

        if not token:
            return jsonify({'Error': 'Token missing'}), 401

        try:
            data = jwt.decode(
                token, Config.SECRET_KEY, algorithms=["HS256"])
            current_user = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'Error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'Error': 'Token invalid'}), 401
        
        return f(current_user,*args,**kwargs)

    return decorated
