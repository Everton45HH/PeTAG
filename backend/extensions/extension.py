from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from utils.error_messages import AppError

bcrypt = Bcrypt()
jwt = JWTManager()

