ERRORS = {
    # Erros Genéricos
    "BAD_REQUEST":         (400, "Requisição inválida."),
    "MISSING_FIELDS":      (400, "Preencha todos os campos."),
    "INTERNAL_ERROR":      (500, "Erro interno do servidor."),

    # Rota Usuários
    "WRONG_DATA":          (401, "Email ou senha inválidos."),
    "USER_NOT_FOUND":     (404, "Usuário não encontrado."),
    "EMAIL_EXISTS":        (409, "Email já existe."),
    "PASSWORD_TOO_SHORT":  (400, "Senha muito curta."),
    "PASSWORD_TOO_LONG":   (400, "Senha muito longa."),

    # Rota Coleiras
    "INVALID_DISTANCE":    (400, "Distância máxima inválida."),
    "INVALID_COORDINATES": (400, "Coordenadas inválidas. Latitude: -90 a 90, longitude: -180 a 180."),
    "DEVICE_NOT_FOUND":    (404, "Coleira não encontrada."),
    "DEVICE_EXISTS":       (409, "Nome da coleira já existe."),
    "LIMIT_REACHED":       (403, "Limite de coleiras atingido."),
}

class AppError(Exception):
    def __init__(self, key):
        self.code = key
        self.status , self.message = ERRORS[key]
        
        