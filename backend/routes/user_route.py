from flask_jwt_extended import (create_access_token, get_jwt_identity, jwt_required , set_access_cookies , unset_jwt_cookies)
from flask import Blueprint, request, jsonify
from utils.error_messages import ERROR as ERRO
from services.user_service import *
from extensions.extension import bcrypt

users_bp = Blueprint('users', __name__, url_prefix='')

@users_bp.route('/user/register', methods=['POST'])
def create():

    info_body = request.json

    senha = info_body['senha']

    if ' ' in senha:
        return jsonify({'message': "A senha não pode conter espaços"}), 400

    senha = senha.split()
    senha = ''.join(senha)

    if senha == "" or senha is None:
        return jsonify({'message': "A senha não pode estar vazia"}), 400
    
    for campo , valor in info_body.items():
        if valor == "" or valor is None:
            return jsonify({'message': "Não pode haver campos vazios"}), 400

    response, erro = get_user_by_email(info_body.get("email"))

    info_body['senha'] = bcrypt.generate_password_hash(password = senha).decode('utf-8')

    if response:
        return jsonify({'message': "Email já cadastrado"}), 409

    response, erro = create_user(info_body)

    if erro:
        erro_info = ERRO.get(erro, {'message': response, 'status_code': 500})
        return jsonify({'message': erro_info['message']}), erro_info['status_code']

    return jsonify({'message': response}), 201

@users_bp.route('/user/login', methods=['POST'])
def login():
    info_body = request.get_json()

    if not info_body:
        return jsonify({'message': "Requisição inválida"}), 400

    for campo, valor in info_body.items():
        if valor == "" or valor is None:
            return jsonify({'message': "Não pode haver campos vazios"}), 400

    email = info_body.get("email")
    senha = info_body.get("senha")

    user, erro = get_user_by_email(email)

    if erro:
        erro_info = ERRO.get(erro, {'message': erro, 'status_code': 500})
        return jsonify({'message': erro_info['message']}), erro_info['status_code']

    if not user:
        return jsonify({"message": "Email não encontrado"}), 404
    if bcrypt.check_password_hash(user["senha"], senha):

        aux = str(user['userID'])
        access_token_cookie = create_access_token(aux)
        response = jsonify({"login" : True })
        set_access_cookies(response, access_token_cookie)
        return response, 200
    else:
        return jsonify({"message": "Senha incorreta"}), 401

@users_bp.route("/user/me", methods=["GET"])
@jwt_required(locations=["cookies"])
def user_info():
    user_id = get_jwt_identity()
    return jsonify({"user_ID": user_id}), 200

@users_bp.route("/user/logout" , methods=["POST"])
def logout():
    response = jsonify({"logout": True})
    unset_jwt_cookies(response)
    return response, 200

@users_bp.route('/api/user/<int:id>', methods=['PATCH','PUT'])
def update(id):
    user, erro = update_user(id, request.json)
    if erro == "Email already exists":
        return jsonify({'message': 'Email já existe'}), 409 
    return jsonify(user), 200

@users_bp.route('/api/user/<int:id>', methods=['DELETE'])
def delete(id):
    response, erro = delete_user(id)
    if erro:
        erro_info = ERRO.get(erro, {'message': 'Unknown error', 'status_code': 500})
        return jsonify({'message': erro_info['message']}), erro_info['status_code']
    return jsonify({'message':response}) , 200

@users_bp.route('/api/getAllUsers', methods=['GET'])
def list_users():
    users, erro = get_all_users()
    if erro:
        erro_info = ERRO.get(erro, {'message': 'Unknown error', 'status_code': 500})
        return jsonify({'message': erro_info['message']}), erro_info['status_code']
    return jsonify(users), 200

@users_bp.route('/api/user/<int:id>', methods=['GET'])
def list_user(id):
    users, erro = get_user_by_id(id)
    if erro:
        erro_info = ERRO.get(erro, {'message': 'Unknown error', 'status_code': 500})
        return jsonify({'message': erro_info['message']}), erro_info['status_code']
    return jsonify(users), 200
    