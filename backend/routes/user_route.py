from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
    unset_jwt_cookies,
    create_access_token,
    set_access_cookies,
)

from services.user_service import create_user, login_user, delete_user

users_bp = Blueprint("usuarios", __name__, url_prefix="/api/usuarios")

@users_bp.route("/cadastro", methods=["POST"])
def create():
    create_user(request.json)
    return jsonify({"message": "Usuário criado com sucesso."}), 201

@users_bp.route("/entrar", methods=["POST"])
def login():
    user_id = login_user(request.json)

    response = jsonify({"message": "Login realizado com sucesso."})
    access_token = create_access_token(identity=str(user_id))
    set_access_cookies(response, access_token)
    return response, 200

#Apenas remove os cookies
@users_bp.route("/me", methods=["POST"])
@jwt_required(locations=["cookies"])
def logout():
    response = jsonify({"message": "Logout realizado com sucesso."})
    unset_jwt_cookies(response)
    return response, 200

#Resgate o ID para o front end usar
@users_bp.route("/me", methods=["GET"])
@jwt_required(locations=["cookies"])
def user_info():
    return jsonify({"userID": int(get_jwt_identity())}), 200

#Deleta usuario e depois a apaga os cookies
@users_bp.route("/me", methods=["DELETE"])
@jwt_required(locations=["cookies"])
def delete():
    delete_user(int(get_jwt_identity()))

    response = jsonify({"message": "Usuário removido com sucesso."})
    unset_jwt_cookies(response)
    return response, 200

# @users_bp.route("/update", methods=["PATCH"])
# @jwt_required(locations=["cookies"])
# def update():
    
#     update_user(get_jwt_identity(), request.json)

#     return jsonify({"message": "Usuário atualizado."}), 200