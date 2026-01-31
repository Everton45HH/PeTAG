from flask_jwt_extended import (get_jwt_identity, jwt_required , unset_jwt_cookies , create_access_token , set_access_cookies)
from flask import Blueprint, request, jsonify
from utils.error_messages import ERROR as ERRO
from services.user_service import *

users_bp = Blueprint('usuarios', __name__, url_prefix='')

@users_bp.route('/user/register', methods=['POST'])
def create():
    response , erro = create_user(request.json)

    if erro:
        return jsonify({"message": erro}), 400

    return jsonify({'message': response}), 201

@users_bp.route('/user/login', methods=['POST'])
def login():
    user_id, erro = login_user(request.json)

    if erro:
        return jsonify({"message": erro}), 400

    access_token = create_access_token(identity=user_id)

    response = jsonify({"login": True})
    set_access_cookies(response, access_token)

    return response, 200
    
@users_bp.route("/user/me", methods=["GET"])
@jwt_required(locations=["cookies"])
def user_info():
    userid = get_jwt_identity()
    return jsonify({"userID": userid}), 200

@users_bp.route("/user/logout" , methods=["POST"])
@jwt_required(locations=["cookies"])
def logout():
    response = jsonify({"logout": True})
    unset_jwt_cookies(response)
    return response, 200

@users_bp.route('/api/user', methods=['PATCH'])
@jwt_required(locations=["cookies"])
def update():
    userid = get_jwt_identity()

    response, erro = update_user(userid, request.json)

    if erro:
        return jsonify({'message': erro}), 400

    return jsonify({'message': 'Usuário atualizado.'}), 200

@users_bp.route('/api/user', methods=['DELETE'])
@jwt_required(locations=["cookies"])
def delete():
    user_id = get_jwt_identity()

    response, erro = delete_user(user_id)

    if erro:
        return jsonify({'message': erro}), 400

    return jsonify({'message': response}), 200    