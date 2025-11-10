from flask import Flask,jsonify, request
from flask_cors import CORS
from config import Config
from models import init_db


from auth.routes import auth_bp
from pricelist.routes import pricelist_bp
from translations.routes import translations_bp


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    
    CORS(app,origins=Config.CORS_ORIGINS)
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(pricelist_bp)
    app.register_blueprint(translations_bp)
    
    return app


app = create_app()
if __name__ =='__main__':
    init_db()
    app.run(debug=True,port=5000)
        
