from DAO.userDAO import UserDAO

daoService = UserDAO()

def create_user(info):
    response , error = daoService.addUserDAO(info)
    return response, error

def get_user_by_email(info):
    response , error = daoService.getUserByEmailDAO(info)
    return response , error

def get_all_users():
    users, erro = daoService.listAllUsersDAO()
    return users, erro

def get_user_by_id(id):
    user , erro = daoService.getUserByIdDAO(id)
    return user , erro

def update_user(id, new_info):
    users, erro = daoService.updateUserDAO(id, new_info)
    return users, erro

def delete_user(id):
    response, erro = daoService.deleteUserDAO(id)
    return response, erro
