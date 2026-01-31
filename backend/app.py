from datetime import timedelta
from flask_cors import CORS
from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv() 

SECRET_KEY = os.environ.get("SECRET_KEY")
IS_PROD = os.environ.get("FLASK_ENV") == "production"

def create_app():
    app = Flask(__name__)

    app.config["JWT_SECRET_KEY"] = SECRET_KEY 
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]    
    app.config["JWT_COOKIE_SECURE"] = IS_PROD
    app.config["JWT_COOKIE_SAMESITE"] = "None" if IS_PROD else "Lax"
    app.config["JWT_COOKIE_DOMAIN"] = None
    app.config["JWT_COOKIE_HTTPONLY"] = True
    app.config["JWT_ACCESS_COOKIE_PATH"] = "/"
    app.config["JWT_REFRESH_COOKIE_PATH"] = "/"
    app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token_cookie"
    app.config["JWT_REFRESH_COOKIE_NAME"] = "refresh_token_cookie"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False  # Desabilitar por enquanto para testar
    from extensions.extension import bcrypt, jwt
    
    bcrypt.init_app(app)
    jwt.init_app(app)

    from routes.user_route import users_bp
    app.register_blueprint(users_bp)

    from routes.coleira_route import coleira_bp
    app.register_blueprint(coleira_bp)

    # Configuração do CORS
    allowed_origins = []
    
    if IS_PROD:
        allowed_origins = ["https://petag-project.vercel.app" , "https://petag-project-mz0sq9pee-evertons-projects-28bbad75.vercel.app/"]
            
    else:
        allowed_origins = [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://192.168.18.10:5173",
            "http://192.168.56.1:5173"
        ]

    CORS(
        app, 
        supports_credentials=True, 
        origins=allowed_origins,
        allow_headers=["Content-Type", "Authorization"],
        expose_headers=["Set-Cookie"],
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
    )

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=not IS_PROD)