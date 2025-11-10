from flask import Blueprint,request,jsonify
from werkzeug.security import check_password_hash
import jwt
from datetime import datetime, timedelta
from config import Config
from utils.database import get_connection
from middleware.auth import token_required

auth_bp = Blueprint('auth',__name__,url_prefix='/api/auth')

@auth_bp.route('/login',methods=['POST'])
def login():
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'Error':'No data provided'}),400
        email = data.get('email')
        password = data.get('password')
        
        print(f"Login attempt : {email}", )
        
        if not email or not password :
            return jsonify({'Error':'Email and password required'}),400
        
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT id,email,password_hash FROM users WHERE email = %s',
                    (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        if not user:
            return jsonify({'Error':'Invalid Credentials'}),401
        
        if not check_password_hash(user['password_hash'],password): 
            return jsonify({'Error': 'Invalid Credentials'}), 401
        
        token = jwt.encode({
            'user_id':user['id'],
            'email':user['email'],
            'exp':datetime.utcnow() + timedelta(hours=24)
            
        },Config.SECRET_KEY,algorithm='HS256')
        
        return jsonify({
            'message':'Login Successful',
            'token':token,
            'user':{
                'id':user['id'],
                'email':user['email']
            }
        }),200
        
    
    except Exception as e:
        return jsonify({'Error':'Login Failed'}),500
    
    
@auth_bp.route('/verify',methods=['GET'])
@token_required
def verify_token(current_user):
    return jsonify({'Valid':True,'user_id':current_user}),200