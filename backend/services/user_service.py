from dao.userDAO import UserDAO
from extensions.extension import bcrypt
from utils.error_messages import AppError

daoService = UserDAO()

def create_user(info):

    for campo in ("nome", "email", "senha"):
        if not info.get(campo):
            raise AppError("MISSING_FIELDS")
        
    senha = info["senha"]

    if len(senha) < 8:
        raise AppError("PASSWORD_TOO_SHORT")

    if len(senha.encode("utf-8")) > 72:
        raise AppError("PASSWORD_TOO_LONG")

    info["senha"] = bcrypt.generate_password_hash(senha).decode("utf-8")
    daoService.create(info)

def login_user(info):
    for campo in ("email", "senha"):
        if not info.get(campo):
            raise AppError("MISSING_FIELDS")    
    user = get_user_by_email(info.get("email"))

    if not user:
        raise AppError("USER_NOT_FOUND")
    
    if not bcrypt.check_password_hash(user["senha"], info.get("senha")):
        raise AppError("WRONG_DATA")
    
    return user["id"]

def get_user_by_email(email):
    return daoService.get_by_email(email)


# def update_user(user_id, new_info):
#     if not user_id:
#         return None, "Usuário não autenticado"

#     if not new_info:
#         return None, "Requisição inválida"

#     allowed_fields = {"nome", "email", "senha"}
#     data = {k: v for k, v in new_info.items() if k in allowed_fields and v}

#     if not data:
#         return None, "Nenhum campo válido para atualizar"

#     if "email" in data:
#         user, _ = get_user_by_email(data["email"])
#         if user and user["userid"] != user_id:
#             return None, "Email já existe"

#     if "senha" in data:
#         senha = data["senha"].strip()
#         if not senha:
#             return None, "Senha não pode estar vazia"
#         if " " in senha:
#             return None, "Senha não pode conter espaços"

#         data["senha"] = bcrypt.generate_password_hash(senha).decode("utf-8")

#     response, error = daoService.update(user_id, data)

#     if error:
#         return None, error

#     if not response:
#         return None, "Usuário não encontrado"

#     return "Usuário atualizado com sucesso", None


def delete_user(user_id):
    daoService.delete(user_id)
