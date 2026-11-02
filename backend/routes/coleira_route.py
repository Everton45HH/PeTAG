from flask import Blueprint, request, jsonify, Response
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.coleira_service import (
    create_coleira,
    get_all_coleiras,
    delete_coleira,
    update_coleira_settings,
    update_coleira_coords,
    generate_map,
)

coleira_bp = Blueprint("coleiras", __name__, url_prefix="/api/coleiras")


@coleira_bp.route("/", methods=["POST"])
@jwt_required(locations=["cookies"])
def create_coleira_route():
    coleira = create_coleira(request.json, int(get_jwt_identity()))
    return jsonify(coleira), 201


@coleira_bp.route("/", methods=["GET"])
@jwt_required(locations=["cookies"])
def list_coleiras_route():
    coleiras = get_all_coleiras(int(get_jwt_identity()))
    return jsonify(coleiras), 200


@coleira_bp.route("/<int:id_coleira>", methods=["DELETE"])
@jwt_required(locations=["cookies"])
def delete_coleira_route(id_coleira):
    delete_coleira(id_coleira, int(get_jwt_identity()))
    return jsonify({"message": "Coleira removida com sucesso."}), 200


@coleira_bp.route("/configuracoes", methods=["PUT"])
@jwt_required(locations=["cookies"])
def update_settings_route():
    update_coleira_settings(request.json, int(get_jwt_identity()))
    return jsonify({"message": "Coleira atualizada com sucesso."}), 200


@coleira_bp.route("/coordenadas", methods=["PUT"])
@jwt_required(locations=["cookies"])
def update_coords_route():
    update_coleira_coords(request.json)
    return jsonify({"message": "Coordenadas atualizadas com sucesso."}), 200

@coleira_bp.route("/mapa", methods=["POST"])
@jwt_required(locations=["cookies"])
def mapa_coleira_route():
    html = generate_map(request.json, int(get_jwt_identity()))
    return Response(html, mimetype="text/html")
