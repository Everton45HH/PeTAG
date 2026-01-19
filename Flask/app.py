from datetime import timedelta
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask import Flask


bcrypt = Bcrypt()
jwt = JWTManager()

# Gambiarra para não da problema de import  
def create_app():
    app = Flask(__name__)

    app.config["JWT_SECRET_KEY"] = "paodebatata"    
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_COOKIE_SECURE"] = False 
    app.config["JWT_COOKIE_SAMESITE"] = "Lax" 
    app.config["JWT_ACCESS_COOKIE_PATH"] = "/"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    app.config["JWT_COOKIE_DOMAIN"] = None
    app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token_cookie" 

    bcrypt.init_app(app)
    jwt.init_app(app)

    from routes.user_route import users_bp
    app.register_blueprint(users_bp)

    from routes.coleira_route import coleira_bp
    app.register_blueprint(coleira_bp)

    CORS(app, supports_credentials=True, origins=[
    "http://localhost:5173",
    "http://localhost",
    "http://127.0.0.1:5173",
    "http://127.0.0.1",
    "http://192.168.18.10:5173",
    "http://192.168.18.10:5000",    
])


    return app
if __name__ == '__main__':
    app = create_app()
    app.run(port=5000,debug=True , host='0.0.0.0')