from dao.coleiraDAO import ColeiraDAO
import math

daoService = ColeiraDAO()

MAX_COLEIRAS = 7

def create_coleira(info, user_id):
    if not info:
        return None, "Requisição Inválida"

    nome = str(info.get('nomeColeira', '')).strip()
    if not nome:
        return None, "Nome Inválido"

    coleiras, erro = daoService.get_all_coleiras_by_user(user_id)
    if erro:
        return None, "Erro ao verificar coleiras do usuário"

    if coleiras and len(coleiras) >= MAX_COLEIRAS:
        return None, "Limite de coleiras atingido"

    try:
        distancia = float(info.get('distanciaMaxima', 0))
        distancia = math.ceil(distancia)

        if distancia < 1:
            return None, "Distancia Invalida"

        info['distanciaMaxima'] = distancia
    except (ValueError, TypeError):
        return None, "Distancia Invalida"

    info['userid'] = user_id

    coordenadas_if = {
        'latitude': -22.948797944778388,
        'longitude': -46.55866095924524
    }

    info.setdefault('latitude', coordenadas_if['latitude'])
    info.setdefault('longitude', coordenadas_if['longitude'])

    response, erro = daoService.create(info)
    if erro:
        return None, "Erro ao criar coleira"

    return response, None


def get_all_coleiras(user_id):
    response, error = daoService.get_all_coleiras_by_user(user_id)

    if error:
        return None, error

    return response, None


def delete_coleira(id_coleira):
    response, error = daoService.delete(id_coleira)

    if error:
        return None, error

    if not response:
        return None, "Coleira não encontrada"

    return "Coleira removida com sucesso", None


def get_coleira(id):
    response, error = daoService.get_by_id(id)
    
    if error:
        return None, error
    
    return response, None


def update_coleira_settings(data, user_id):

    id_coleira = data.get('idColeira')

    print(data , user_id)

    if not data:
        return None, "Requisição inválida"

    if 'nomeColeira' in data:
        nome = str(data.get('nomeColeira', '')).strip()
        if not nome:
            return None, "O nome da coleira não pode estar vazio"
        data['nomeColeira'] = nome

    if 'distanciaMaxima' in data:
        try:
            distancia = float(data.get('distanciaMaxima'))
            if distancia < 1:
                return None, "A distância máxima deve ser pelo menos 1 metro"
            data['distanciaMaxima'] = math.ceil(distancia)
        except (ValueError, TypeError):
            return None, "Distância máxima inválida"

    response, error = daoService.update_settings(id_coleira, data, user_id)

    if error:
        return None, "Erro ao atualizar coleira"

    if not response:
        return None, "Coleira não encontrada"

    return "Coleira atualizada com sucesso", None


def update_coleira_coords(data):
    if not data:
        return None, "Requisição inválida"
        
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    idColeira = data.get('idColeira')    
    if latitude is None or longitude is None:
        return None, "Latitude e longitude são obrigatórias"
    
    try:
        latitude = float(latitude)
        longitude = float(longitude)
        
        if not (-90 <= latitude <= 90):
            return None, "Latitude deve estar entre -90 e 90"
        if not (-180 <= longitude <= 180):
            return None, "Longitude deve estar entre -180 e 180"
            
    except (ValueError, TypeError):
        return None, "Coordenadas inválidas"

    response, error = daoService.update_coords(data ,idColeira )
    
    if error:
        return None, "Erro ao atualizar coordenadas"
    
    if not response:
        return None, "Coleira não encontrada"
    
    return "Coordenadas atualizadas com sucesso", None