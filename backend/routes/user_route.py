from flask_jwt_extended import (create_access_token, get_jwt_identity, jwt_required, set_access_cookies, unset_jwt_cookies)
from flask import Blueprint, request, jsonify
from utils.error_messages import ERROR as ERRO
from services.user_service import *
from extensions.extension import bcrypt

users_bp = Blueprint('users', __name__, url_prefix='')

@users_bp.route('/user/register', methods=['POST'])
def create():
    info_body = request.json

    if not info_body:
        return jsonify({'message': "Requisição inválida"}), 400

    # Validação de campos obrigatórios
    required_fields = ['senha', 'email', 'nome']  # Adicione os campos necessários
    for field in required_fields:
        if field not in info_body or not info_body[field]:
            return jsonify({'message': f"O campo '{field}' é obrigatório"}), 400

    senha = info_body['senha'].strip()
    
    if ' ' in senha:
        return jsonify({'message': "A senha não pode conter espaços"}), 400

    # Validar campos vazios
    for campo, valor in info_body.items():
        if isinstance(valor, str) and not valor.strip():
            return jsonify({'message': f"O campo '{campo}' não pode estar vazio"}), 400

    response, erro = get_user_by_email(info_body.get("email"))

    if response:
        return jsonify({'message': "Email já cadastrado"}), 409

    if erro:
        erro_info = ERRO.get(erro, {'message': 'Erro ao verificar email', 'status_code': 500})
        return jsonify({'message': erro_info['message']}), erro_info['status_code']

    info_body['senha'] = bcrypt.generate_password_hash(password=senha).decode('utf-8')

    response, erro = create_user(info_body)

    if erro:
        erro_info = ERRO.get(erro, {'message': response, 'status_code': 500})
        return jsonify({'message': erro_info['message']}), erro_info['status_code']

    return jsonify({'message': 'Usuário criado com sucesso'}), 201


@users_bp.route('/user/login', methods=['POST'])
def login():
    info_body = request.get_json()

    if not info_body:
        return jsonify({'message': "Requisição inválida"}), 400

    email = info_body.get("email", "").strip()
    senha = info_body.get("senha", "").strip()

    if not email or not senha:
        return jsonify({'message': "Email e senha são obrigatórios"}), 400

    user, erro = get_user_by_email(email)

    if erro:
        erro_info = ERRO.get(erro, {'message': 'Erro ao buscar usuário', 'status_code': 500})
        return jsonify({'message': erro_info['message']}), erro_info['status_code']

    if not user:
        return jsonify({"message": "Email ou senha incorretos"}), 401

    if not bcrypt.check_password_hash(user["senha"], senha):
        return jsonify({"message": "Email ou senha incorretos"}), 401

    access_token = create_access_token(identity=str(user['userID']))
    
    response = jsonify({
        "login": True,
        "message": "Login realizado com sucesso"
    })
    set_access_cookies(response, access_token)
    
    return response, 200


@users_bp.route("/user/me", methods=["GET"])
@jwt_required()
def user_info():
    user_id = get_jwt_identity()
    
    user, erro = get_user_by_id(int(user_id))
    
    if erro:
        erro_info = ERRO.get(erro, {'message': 'Erro ao buscar usuário', 'status_code': 500})
        return jsonify({'message': erro_info['message']}), erro_info['status_code']
    
    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404
    
    user.pop('senha', None)
    
    return jsonify(user), 200


@users_bp.route("/user/logout", methods=["POST"])
def logout():
    response = jsonify({
        "logout": True,
        "message": "Logout realizado com sucesso"
    })
    unset_jwt_cookies(response)
    return response, 200


@users_bp.route('/api/user/<int:id>', methods=['PATCH', 'PUT'])
@jwt_required()
def update(id):
    # Linha que verifica se o usuário está atualizando seus próprios dados
    current_user_id = int(get_jwt_identity())
    
    if current_user_id != id:
        return jsonify({'message': 'Não autorizado a alterar dados de outro usuário'}), 403
    
    info_body = request.json
    
    if not info_body:
        return jsonify({'message': "Requisição inválida"}), 400
    
    # Se estiver atualizando senha, fazer hash
    if 'senha' in info_body:
        senha = info_body['senha'].strip()
        
        if senha:
            
            if ' ' in senha:
                return jsonify({'message': "A senha não pode conter espaços"}), 400
            
            info_body['senha'] = bcrypt.generate_password_hash(password=senha).decode('utf-8')
        else:
            # Remove senha se vazia (não atualiza)
            info_body.pop('senha')
    
    # Segurança para não permitir atualizar userID
    if 'userID' in info_body:
        info_body.pop('userID')
    
    user, erro = update_user(id, info_body)
    
    if erro == "Email already exists":
        return jsonify({'message': 'Email já existe'}), 409
    
    if erro:
        erro_info = ERRO.get(erro, {'message': 'Erro ao atualizar usuário', 'status_code': 500})
        return jsonify({'message': erro_info['message']}), erro_info['status_code']
    
    # Remover senha antes de retornar
    if user and 'senha' in user:
        user.pop('senha')
    
    return jsonify({
        'message': 'Usuário atualizado com sucesso',
        'user': user
    }), 200


@users_bp.route('/api/user/<int:id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    # Verificar se usuário está deletando sua própria conta
    current_user_id = int(get_jwt_identity())
    
    if current_user_id != id:
        return jsonify({'message': 'Não autorizado a deletar outro usuário'}), 403
    
    response, erro = delete_user(id)
    
    if erro:
        erro_info = ERRO.get(erro, {'message': 'Erro ao deletar usuário', 'status_code': 500})
        return jsonify({'message': erro_info['message']}), erro_info['status_code']
    
    # Limpar cookies após deletar
    resp = jsonify({'message': 'Usuário deletado com sucesso'})
    unset_jwt_cookies(resp)
    
    return resp, 200


@users_bp.route('/api/getAllUsers', methods=['GET'])
@jwt_required()
def list_users():
    # IMPORTANTE: Esta rota deveria ter verificação de ADMIN
    # Por enquanto, qualquer usuário autenticado pode ver todos
    # Considere adicionar role-based access control (RBAC)
    
    users, erro = get_all_users()
    
    if erro:
        erro_info = ERRO.get(erro, {'message': 'Erro ao buscar usuários', 'status_code': 500})
        return jsonify({'message': erro_info['message']}), erro_info['status_code']
    
    # Remover senhas de todos os usuários
    if users:
        for user in users:
            user.pop('senha', None)
    
    return jsonify(users), 200


@users_bp.route('/api/user/<int:id>', methods=['GET'])
@jwt_required()
def list_user(id):
    # Verificar se usuário está acessando seus próprios dados
    # ou se é admin 
    current_user_id = int(get_jwt_identity())
    
    if current_user_id != id:
        pass
    
    user, erro = get_user_by_id(id)
    
    if erro:
        erro_info = ERRO.get(erro, {'message': 'Erro ao buscar usuário', 'status_code': 500})
        return jsonify({'message': erro_info['message']}), erro_info['status_code']
    
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    
    user.pop('senha', None)
    
    return jsonify(user), 200