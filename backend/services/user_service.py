from dao.userDAO import UserDAO
from extensions.extension import bcrypt

daoService = UserDAO()

def create_user(info):
    if not info:
        return None, "Requisição inválida"

    for campo in ['nome', 'email', 'senha']:
        if not info.get(campo):
            return None, "Não pode haver campos vazios"

    senha = info.get('senha')

    if ' ' in senha:
        return None, "A senha não pode conter espaços"

    senha = senha.strip()
    if not senha:
        return None, "A senha não pode estar vazia"
    user, error = get_user_by_email(info['email'])
    if user:
        return None, "Email já existe"
    
    elif error:
        return None, error

    info['senha'] = bcrypt.generate_password_hash(senha).decode('utf-8')

    response, erro = daoService.create(info)

    print(erro)

    if erro:
        return None,erro
    
    return response, None

def login_user(info):
    if not info:
        return None, "Requisição inválida"

    for campo in ['email', 'senha']:
        if not info.get(campo):
            return None, "Não pode haver campos vazios"

    email = info['email']
    senha = info['senha']

    user, error = get_user_by_email(email)

    if error:
        return None, error

    if not user:
        return None, "Email não encontrado"

    if not bcrypt.check_password_hash(user["senha"], senha):
        return None, "Senha inválida"

    return str(user["userID"]), None

def get_user_by_email(email):
    response , error = daoService.get_by_email(email)
    return response , error

def update_user(user_id, new_info):
    if not user_id:
        return None, "Usuário não autenticado"

    if not new_info:
        return None, "Requisição inválida"

    allowed_fields = {'nome', 'email', 'senha'}
    data = {k: v for k, v in new_info.items() if k in allowed_fields and v}

    if not data:
        return None, "Nenhum campo válido para atualizar"

    if 'email' in data:
        user, _ = get_user_by_email(data['email'])
        if user and user['userid'] != user_id:
            return None, "Email já existe"

    if 'senha' in data:
        senha = data['senha'].strip()
        if not senha:
            return None, "Senha não pode estar vazia"
        if ' ' in senha:
            return None, "Senha não pode conter espaços"

        data['senha'] = bcrypt.generate_password_hash(senha).decode('utf-8')

    response, error = daoService.update(user_id, data)

    if error:
        return None, error

    if not response:
        return None, "Usuário não encontrado"

    return "Usuário atualizado com sucesso", None

def delete_user(user_id):
    response, error = daoService.delete(user_id)

    if error:
        return None, error

    if not response:
        return None, "Usuário não encontrado"

    return "Usuário removido com sucesso", None
