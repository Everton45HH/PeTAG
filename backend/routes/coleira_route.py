from flask import Blueprint, request, jsonify, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.coleira_service import *
from utils.error_messages import ERROR as ERRO
import folium
import math

coleira_bp = Blueprint('coleiras', __name__, url_prefix='')


@coleira_bp.route('/api/coleira', methods=['POST'])
@jwt_required()
def create():
    try:
        info = request.json

        if not info:
            return jsonify({'message': "Requisição inválida"}), 400

        user_id = get_jwt_identity()
        
        if not user_id:
            return jsonify({'message': "Usuário não autenticado"}), 401

        # Validar nome
        nome = str(info.get('nomeColeira', '')).strip()
        if not nome:
            return jsonify({'message': "O nome da coleira não pode estar vazio"}), 400

        # Verificar limite de coleiras
        coleiras_existentes, erro = get_all_coleiras(int(user_id))

        if erro:
            erro_info = ERRO.get(erro, {'message': 'Erro ao verificar coleiras', 'status_code': 500})
            return jsonify({'message': erro_info['message']}), erro_info['status_code']
        
        if coleiras_existentes and len(coleiras_existentes) >= 7:
            return jsonify({'message': "Limite de 7 coleiras atingido"}), 400
        
        # Validar distância
        try:
            distancia = float(info.get('distanciaMaxima', 0))
            distancia = math.ceil(distancia)
            
            if distancia < 1:
                return jsonify({'message': "A distância máxima deve ser pelo menos 1 metro"}), 400
            
            info['distanciaMaxima'] = distancia
        except (ValueError, TypeError):
            return jsonify({'message': "Distância máxima inválida"}), 400

        # Adicionar userID
        info['userID'] = int(user_id)

        # Coordenadas padrão (IF)
        coordenadasDoIF = {
            'latitude': -22.948797944778388,
            'longitude': -46.55866095924524
        }

        info.setdefault('latitude', coordenadasDoIF['latitude'])
        info.setdefault('longitude', coordenadasDoIF['longitude'])

        # Criar coleira
        response, erro = create_coleira(info)

        if erro:
            erro_info = ERRO.get(erro, {'message': 'Erro ao criar coleira', 'status_code': 500})
            return jsonify({'message': erro_info['message']}), erro_info['status_code']

        return jsonify({'message': 'Coleira criada com sucesso'}), 201

    except Exception as e:
        print(f"❌ Erro ao criar coleira: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'message': 'Erro interno ao criar coleira'}), 500


# ✅ Listar TODAS as coleiras de um usuário
@coleira_bp.route('/api/coleiras/<int:user_id>', methods=['GET'])
@jwt_required()
def listColeiras(user_id):
    try:
        current_user_id = get_jwt_identity()

        if not current_user_id:
            return jsonify({'message': "Usuário não autenticado"}), 401
        
        if int(current_user_id) != user_id:
            return jsonify({'message': "Não autorizado"}), 403
        
        lista, erro = get_all_coleiras(user_id)

        if erro:
            erro_info = ERRO.get(erro, {'message': 'Erro ao buscar coleiras', 'status_code': 500})
            return jsonify({'message': erro_info['message']}), erro_info['status_code']
        
        if not lista:
            return jsonify([]), 200
        
        return jsonify(lista), 200

    except Exception as e:
        print(f"❌ Erro ao listar coleiras: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'message': 'Erro interno'}), 500


# ✅ Buscar UMA coleira específica (se precisar no futuro)
@coleira_bp.route('/api/coleira/detalhes/<int:id_coleira>', methods=['GET'])
@jwt_required()
def getColeira(id_coleira):
    try:
        user_id = get_jwt_identity()

        if not user_id:
            return jsonify({'message': "Usuário não autenticado"}), 401
        
        coleira, erro = get_coleira(id_coleira)

        if erro:
            erro_info = ERRO.get(erro, {'message': 'Erro ao buscar coleira', 'status_code': 500})
            return jsonify({'message': erro_info['message']}), erro_info['status_code']
        
        if not coleira:
            return jsonify({'message': 'Coleira não encontrada'}), 404

        # ✅ Verificar se pertence ao usuário (userID camelCase)
        if str(coleira.get('userID')) != str(user_id):
            return jsonify({'message': 'Não autorizado'}), 403
        
        return jsonify(coleira), 200

    except Exception as e:
        print(f"❌ Erro ao buscar coleira: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'message': 'Erro interno'}), 500


# ✅ Deletar coleira
@coleira_bp.route('/api/coleira/<int:id_coleira>', methods=['DELETE'])
@jwt_required()
def deleteColeira(id_coleira):
    try:
        user_id = get_jwt_identity()

        if not user_id:
            return jsonify({'message': "Usuário não autenticado"}), 401

        response, erro = delete_coleira(id_coleira, int(user_id))

        if erro:
            erro_info = ERRO.get(erro, {"message": "Erro ao deletar coleira", "status_code": 500})
            return jsonify({"message": erro_info["message"]}), erro_info["status_code"]

        return jsonify({"message": "Coleira deletada com sucesso"}), 200

    except Exception as e:
        print(f"❌ Erro ao deletar coleira: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'message': 'Erro interno'}), 500


# ✅ Atualizar settings (nome e distância)
@coleira_bp.route('/api/coleira/<int:id_coleira>/settings', methods=['PUT'])
@jwt_required()
def updateSettings(id_coleira):
    try:
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
                if distancia < 1:
                    return jsonify({'message': "A distância máxima deve ser pelo menos 1 metro"}), 400
                data['distanciaMaxima'] = math.ceil(distancia)
            except (ValueError, TypeError):
                return jsonify({'message': "Distância máxima inválida"}), 400

        response, erro = update_device_settings(id_coleira, data, int(user_id))
        
        if erro:
            erro_info = ERRO.get(erro, {'message': 'Erro ao atualizar configurações', 'status_code': 400})
            return jsonify({'message': erro_info['message']}), erro_info['status_code']
        
        return jsonify({'message': 'Configurações atualizadas com sucesso'}), 200

    except Exception as e:
        print(f"❌ Erro ao atualizar settings: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'message': 'Erro interno'}), 500


# ✅ Atualizar coordenadas
@coleira_bp.route('/api/coleira/<int:id_coleira>/coords', methods=['PUT'])
@jwt_required()
def updateCoords(id_coleira):
    try:
        data = request.json
        
        if not data:
            return jsonify({'message': "Requisição inválida"}), 400

        user_id = get_jwt_identity()
        
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

    except Exception as e:
        print(f"❌ Erro ao atualizar coords: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'message': 'Erro interno'}), 500


# ✅ Gerar mapa

@coleira_bp.route("/api/coleira/mapa/<int:id_coleira>", methods=["POST"])
@jwt_required(locations=["cookies"])
def mapa_coleira(id_coleira):   
    data = request.json or {}

    latitude = data.get("latitude")
    longitude = data.get("longitude")
    distancia_maxima = data.get("distanciaMaxima", 100)

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

    mapa = folium.Map(
        location=[latitude, longitude],
        zoom_start=18.4,
        control_scale=False,
        height="100%",
        zoom_control=False
    )

    folium.TileLayer(
        tiles='https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr='Google',
        name='Google Satellite',
        subdomains=['mt0','mt1','mt2','mt3']
    ).add_to(mapa)

    folium.Marker(
        [latitude, longitude],
        popup=coleira.get('nomecoleira'),
        icon=folium.Icon(color="red", icon="paw", prefix='fa')
    ).add_to(mapa)

    coordenadasDoIF = {
        'latitude': -22.948797944778388,
        'longitude': -46.55866095924524
    }

    folium.Circle(
        location=[coordenadasDoIF['latitude'], coordenadasDoIF['longitude']],
        radius=distancia_maxima,
        color="red",
        fill=True,
        fill_opacity=0.15
    ).add_to(mapa)

    return Response(mapa._repr_html_(), mimetype="text/html")