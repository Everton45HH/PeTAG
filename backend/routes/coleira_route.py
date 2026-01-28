from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.coleira_service import *
from utils.error_messages import ERROR as ERRO
from flask import Blueprint, request, Response
import folium

coleira_bp = Blueprint('coleiras', __name__, url_prefix='')

@coleira_bp.route('/api/coleira', methods=['POST'])
@jwt_required(locations=["cookies"])
def create():
    info = request.json

    if not info:
        return jsonify({'message': "Requisição inválida"}), 400

    user_id = get_jwt_identity()
    
    if not user_id:
        return jsonify({'message': "Usuário não autenticado"}), 401

    nome = str(info.get('nomeColeira')).strip()

    coleiras_existentes, erro = get_all_coleiras(int(user_id))

    if erro:
        erro_info = ERRO.get(erro, {'message': 'Erro ao verificar coleiras', 'status_code': 500})
        return jsonify({'message': erro_info['message']}), erro_info['status_code']
    
    nome = str(info.get('nomeColeira', '')).strip()
    
    if coleiras_existentes and len(coleiras_existentes) >= 7:
        return jsonify({'message': "Limite de 7 coleiras atingido"}), 400
    
    try:
        distancia = float(info.get('distanciaMaxima', 0))
        if distancia <= 0:
            return jsonify({'message': "A distância máxima deve ser maior que zero"}), 400
    except (ValueError, TypeError):
        return jsonify({'message': "Distância máxima inválida"}), 400

    if not nome:
        return jsonify({'message': "O nome da coleira não pode estar vazio"}), 400

    info['userID'] = int(user_id)

    coordenadasDoIF = {
        'latitude': -22.948797944778388,
        'longitude': -46.55866095924524
    }

    info.setdefault('latitude', coordenadasDoIF['latitude'])
    info.setdefault('longitude', coordenadasDoIF['longitude'])

    response, erro = create_coleira(info)

    if erro:
        erro_info = ERRO.get(erro, {'message': 'Erro ao criar coleira', 'status_code': 500})
        return jsonify({'message': erro_info['message']}), erro_info['status_code']

    return jsonify({'message': 'Coleira criada com sucesso'}), 201

@coleira_bp.route('/api/coleira/<int:id>', methods=['GET'])
@jwt_required(locations=["cookies"])
def listColeira(id):

    user_id = get_jwt_identity()

    if not user_id:
        return jsonify({'message': "Usuário não autenticado"}), 401
    
    if int(user_id) != id:
        return jsonify({'message': "Não autorizado a acessar coleiras de outro usuário"}), 403
    
    lista, erro = get_coleira(id)

    if erro:
        erro_info = ERRO.get(erro, {'message': 'Erro ao buscar coleiras', 'status_code': 500})
        return jsonify({'message': erro_info['message']}), erro_info['status_code']
    
    if not lista:
        return jsonify([]), 200
    
    return jsonify(lista), 200

@coleira_bp.route('/api/coleiras/<int:id>', methods=['GET'])
@jwt_required(locations=["cookies"])
def listColeiras(id):

    user_id = get_jwt_identity()

    if not user_id:
        return jsonify({'message': "Usuário não autenticado"}), 401
    
    if int(user_id) != id:
        return jsonify({'message': "Não autorizado a acessar coleiras de outro usuário"}), 403
    
    lista, erro = get_all_coleiras(id)

    if erro:
        erro_info = ERRO.get(erro, {'message': 'Erro ao buscar coleiras', 'status_code': 500})
        return jsonify({'message': erro_info['message']}), erro_info['status_code']
    
    if not lista:
        return jsonify([]), 200
    
    return jsonify(lista), 200


@coleira_bp.route('/api/coleira/<int:id_coleira>', methods=['DELETE'])
@jwt_required(locations=["cookies"])
def deleteColeira(id_coleira):

    user_id = get_jwt_identity()

    if not user_id:
        return jsonify({'message': "Usuário não autenticado"}), 401

    response, erro = delete_coleira(id_coleira, int(user_id))

    if erro:
        erro_info = ERRO.get(
            erro,
            {"message": "Erro ao deletar coleira", "status_code": 500}
        )
        return jsonify({"message": erro_info["message"]}), erro_info["status_code"]

    return jsonify({"message": "Coleira deletada com sucesso"}), 200


@coleira_bp.route('/api/coleira/<int:id_coleira>/coords', methods=['PATCH', 'PUT'])
def updateCoords(id_coleira):
    data = request.json

    if not data:
        return jsonify({'message': "Requisição inválida"}), 400

    user_id = 3
    
    if not user_id:
        return jsonify({'message': "Usuário não autenticado"}), 401

    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if latitude is None or longitude is None:
        return jsonify({'message': "Latitude e longitude são obrigatórias"}), 400

    try:
        latitude = float(latitude)
        longitude = float(longitude)

        if not (-90 <= latitude <= 90):
            return jsonify({'message': "Latitude deve estar entre -90 e 90"}), 400
        if not (-180 <= longitude <= 180):
            return jsonify({'message': "Longitude deve estar entre -180 e 180"}), 400
            
    except (ValueError, TypeError):
        return jsonify({'message': "Coordenadas inválidas"}), 400

    response, erro = update_device_coords(id_coleira, data, int(user_id))
    
    if erro:
        erro_info = ERRO.get(erro, {'message': 'Erro ao atualizar coordenadas', 'status_code': 400})
        return jsonify({'message': erro_info['message']}), erro_info['status_code']
    
    return jsonify({'message': 'Coordenadas atualizadas com sucesso'}), 200


@coleira_bp.route('/api/coleira/<int:id_coleira>/settings', methods=['PATCH', 'PUT'])
@jwt_required(locations=["cookies"])
def updateSettings(id_coleira):
    data = request.json

    if not data:
        return jsonify({'message': "Requisição inválida"}), 400

    user_id = get_jwt_identity()
    
    if not user_id:
        return jsonify({'message': "Usuário não autenticado"}), 401

    allowed_fields = ['nomeColeira', 'distanciaMaxima']
    
    if not any(field in data for field in allowed_fields):
        return jsonify({'message': "Nenhum campo válido para atualizar"}), 400

    if 'nomeColeira' in data:
        nome = str(data.get('nomeColeira', '')).strip()
        if not nome:
            return jsonify({'message': "O nome da coleira não pode estar vazio"}), 400
        data['nomeColeira'] = nome

    if 'distanciaMaxima' in data:
        try:
            distancia = float(data.get('distanciaMaxima', 0))
            if distancia <= 0:
                return jsonify({'message': "A distância máxima deve ser maior que zero"}), 400
            data['distanciaMaxima'] = distancia
        except (ValueError, TypeError):
            return jsonify({'message': "Distância máxima inválida"}), 400

    response, erro = update_device_settings(id_coleira, data, int(user_id))
    
    if erro:
        erro_info = ERRO.get(erro, {'message': 'Erro ao atualizar configurações', 'status_code': 400})
        return jsonify({'message': erro_info['message']}), erro_info['status_code']
    
    return jsonify({'message': 'Configurações atualizadas com sucesso'}), 200


@coleira_bp.route("/api/coleira/mapa/<int:id_coleira>", methods=['POST'])
@jwt_required()
def mapa_coleira(id_coleira):
    data = request.json
    if not data:
        return jsonify({'message': 'Requisição inválida'}), 400

    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    distancia_maxima = data.get('distanciaMaxima', 100)

    if latitude is None or longitude is None:
        return jsonify({'message': 'Coordenadas são obrigatórias'}), 400

    try:
        latitude = float(latitude)
        longitude = float(longitude)
        distancia_maxima = float(distancia_maxima)

        if not (-90 <= latitude <= 90):
            return jsonify({'message': 'Latitude inválida'}), 400
        if not (-180 <= longitude <= 180):
            return jsonify({'message': 'Longitude inválida'}), 400

    except (ValueError, TypeError):
        return jsonify({'message': 'Coordenadas inválidas'}), 400

    user_id = get_jwt_identity()
    coleira, erro = get_coleira(id_coleira)

    if erro or not coleira:
        return jsonify({'message': 'Coleira não encontrada'}), 404
        
    if str(coleira.get('userid')) != str(user_id):
        return jsonify({'message': 'Não autorizado'}), 403

    # Criar mapa
    
    mapa = folium.Map(
        location=[latitude, longitude],
        control_scale=False,
        zoom_start=18,
        height="100%"
    )

    folium.TileLayer(
    tiles='https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
    attr='Google',
    name='Google Satellite',
    subdomains=['mt0','mt1','mt2','mt3'],
    min_zoom=1
    ).add_to(mapa)

    # Marker da coleira
    folium.Marker(
        [latitude, longitude],
        popup=f"{coleira.get('nomecoleira')}",
        icon=folium.Icon(color="red", icon="paw", prefix='fa')
    ).add_to(mapa)

    # Círculo de distância máxima

    coordenadasDoIF = {'latitude': -22.948797944778388, 'longitude': -46.55866095924524}
    
    folium.Circle(
        radius=distancia_maxima,
        location=[coordenadasDoIF['latitude'], coordenadasDoIF['longitude']],
        color="red",
        fill=True,
        fill_opacity=0.1,
    ).add_to(mapa)

    return mapa._repr_html_()


@coleira_bp.route("/api/coleira/mapa/simulacao", methods=["POST"])
@jwt_required(locations=["cookies"])
def mapa_simulacao():
    data = request.json or {}

    # Coordenadas base (IF)
    base_lat = -22.948797944778388
    base_lon = -46.55866095924524

    try:
        latitude = float(data.get("latitude", base_lat))
        longitude = float(data.get("longitude", base_lon))
        distancia_maxima = float(data.get("distanciaMaxima", 100))
    except (ValueError, TypeError):
        return jsonify({'message': 'Dados inválidos'}), 400

    # 🔀 Simulação de movimento
    import random
    latitude += random.uniform(-0.00005, 0.00005)
    longitude += random.uniform(-0.00005, 0.00005)

    # 🗺️ Mapa
    mapa = folium.Map(
        location=[latitude, longitude],
        zoom_start=18,
        control_scale=False,
        height="100%"
    )

    folium.TileLayer(
        tiles='https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr='Google',
        name='Google Satellite',
        subdomains=['mt0','mt1','mt2','mt3'],
    ).add_to(mapa)

    # Marker da coleira (simulada)
    folium.Marker(
        [latitude, longitude],
        popup="Coleira (Simulação)",
        icon=folium.Icon(color="blue", icon="paw", prefix="fa")
    ).add_to(mapa)

    # Círculo do raio permitido
    folium.Circle(
        location=[base_lat, base_lon],
        radius=distancia_maxima,
        color="red",
        fill=True,
        fill_opacity=0.15
    ).add_to(mapa)

    # ⚠️ IMPORTANTE: retorna HTML puro
    return Response(mapa._repr_html_(), mimetype="text/html")