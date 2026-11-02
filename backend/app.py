import os
from datetime import timedelta

from flask_cors import CORS
from dotenv import load_dotenv
from flask import Flask, jsonify

from utils.error_messages import AppError, ERRORS
from routes.coleira_route import coleira_bp
from routes.user_route import users_bp
from extensions.extension import bcrypt, jwt

load_dotenv()

SECRET_KEY = os.environ["SECRET_KEY"]
IS_PROD = os.environ.get("FLASK_ENV") == "production"


def create_app():
    app = Flask(__name__)

    app.config["JWT_SECRET_KEY"] = SECRET_KEY
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_COOKIE_SECURE"] = IS_PROD
    app.config["JWT_COOKIE_SAMESITE"] = "None" if IS_PROD else "Lax"
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(users_bp)
    app.register_blueprint(coleira_bp)

    if IS_PROD:
        origins = ["https://petag-project.vercel.app"]
    else:
        origins = [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://192.168.18.10:5173",
        ]

    CORS(
        app,
        supports_credentials=True,
        origins=origins,
        allow_headers=["Content-Type", "X-CSRF-TOKEN"],
        methods=["GET", "POST","DELETE", "OPTIONS" ,"PUT" ],
    )

    @app.errorhandler(AppError)
    def handle_app_error(e):
        return jsonify({"error": {"code": e.code, "message": e.message}}), e.status

    
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=not IS_PROD)