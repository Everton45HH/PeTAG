from flask import Blueprint, request, jsonify, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.coleira_service import *
from utils.error_messages import ERROR as ERRO
import folium

coleira_bp = Blueprint('coleiras', __name__, url_prefix='')

@coleira_bp.route('/api/coleira', methods=['POST'])
@jwt_required(locations=["cookies"])
def create():
    user_id = get_jwt_identity()
    response, erro = create_coleira(request.json, user_id)
    if erro:
        return jsonify({'message' : erro}) , 400
    return jsonify(response), 201

@coleira_bp.route('/api/coleiras', methods=['GET'])
@jwt_required(locations=["cookies"])
def list_coleiras():
    user_id = get_jwt_identity()
    lista, erro = get_all_coleiras(user_id)

    if erro:
        return jsonify({'message': 'Erro ao listar coleiras'}), 500
    return jsonify(lista), 200

@coleira_bp.route('/api/coleira/<int:id_coleira>', methods=['DELETE'])
@jwt_required(locations=["cookies"])
def deleteColeira(id_coleira):
    message, erro = delete_coleira(id_coleira)

    if erro:
        return jsonify({'message': erro}), 400

    return jsonify({'message': message}), 200

@coleira_bp.route('/api/coleira/settings', methods=['PUT'])
@jwt_required(locations=["cookies"])
def updateSettings():

    user_id = get_jwt_identity()

    print(request.json)

    lista, erro = update_coleira_settings(request.json , user_id)

    if erro:
        return jsonify({'message': 'Erro ao atualizar coleira'}), 500

    return jsonify(lista), 200

@coleira_bp.route('/api/coleira/coords', methods=['PUT'])
@jwt_required(locations=["cookies"])
def updateCoords():
    response, erro = update_coleira_coords(request.json)

    if erro:
        return jsonify({'message': erro}), 400
    
    return jsonify({'message': response}), 200

@coleira_bp.route("/api/coleira/mapa", methods=["POST"])
@jwt_required(locations=["cookies"])
def mapa_coleira():   
    data = request.json or {}

    latitude = data.get("latitude")
    longitude = data.get("longitude")
    distancia_maxima = data.get("distanciaMaxima", 10)
    id_coleira = data.get("idColeira")

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

    mapa = folium.Map(
        location=[latitude, longitude],
        zoom_start=18.4,
        control_scale=False,
        height="100%",
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