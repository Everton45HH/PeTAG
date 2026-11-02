import math
import folium
from dao.coleiraDAO import ColeiraDAO
from utils.error_messages import AppError
from DEFAULT_CONFIGS.default_configs import MAX_COLLARS, CENTER_COORDINATES

daoService = ColeiraDAO()


# Funções auxiliares
def _parse_distancia(valor):
    try:
        distancia = math.ceil(float(valor))
    except (ValueError, TypeError, OverflowError):
        raise AppError("INVALID_DISTANCE")

    if distancia < 1:
        raise AppError("INVALID_DISTANCE")

    return distancia


def _parse_coordenadas(latitude, longitude):
    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except (ValueError, TypeError):
        raise AppError("INVALID_COORDINATES")

    if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
        raise AppError("INVALID_COORDINATES")

    return latitude, longitude


# Funções de rota-service


def create_coleira(info, user_id):
    for campo in ("nomeColeira", "distanciaMaxima"):
        if not str(info.get(campo) or "").strip():
            raise AppError("MISSING_FIELDS")

    nome = str(info["nomeColeira"]).strip()
    distancia = _parse_distancia(info["distanciaMaxima"])

    latitude, longitude = _parse_coordenadas(
        info.get("latitude", CENTER_COORDINATES["latitude"]),
        info.get("longitude", CENTER_COORDINATES["longitude"]),
    )

    if len(get_all_coleiras(user_id)) >= MAX_COLLARS:
        raise AppError("LIMIT_REACHED")

    return daoService.create(
        {
            "nomeColeira": nome,
            "distanciaMaxima": distancia,
            "userID": user_id,
            "latitude": latitude,
            "longitude": longitude,
        }
    )


def get_all_coleiras(user_id):
    return daoService.get_all_coleiras_by_user(user_id)


def get_coleira(id_coleira, user_id):
    return daoService.get_by_id(id_coleira)


def delete_coleira(id_coleira, user_id):
    daoService.delete(id_coleira, user_id)


def update_coleira_settings(info, user_id):
    for campo in ("idColeira", "nomeColeira"):
        if not str(info.get(campo) or "").strip():
            raise AppError("MISSING_FIELDS")

    if not (get_coleira(info["idColeira"],user_id)):
        raise AppError("COLLAR_NOT_FOUND")

    return daoService.update_settings(
        info["idColeira"],
        user_id,
        {
            "nomeColeira": info["nomeColeira"],
            "distanciaMaxima": _parse_distancia(info.get("distanciaMaxima")),
        },
    )


def update_coleira_coords(info):

    for campo in ("idColeira", "latitude", "longitude"):
        if not info.get(campo):
            raise AppError("MISSING_FIELDS")

    id_coleira = info.get("idColeira")
    latitude, longitude = _parse_coordenadas(info["latitude"], info["longitude"])

    daoService.update_coords(
        id_coleira,
        {"latitude": latitude, "longitude": longitude},
    )


def generate_map(info, user_id):
    id_coleira = info.get("idColeira")

    if not id_coleira or info.get("latitude") is None or info.get("longitude") is None:
        raise AppError("MISSING_FIELDS")

    latitude, longitude = _parse_coordenadas(info["latitude"], info["longitude"])
    coleira = get_coleira(id_coleira, user_id)

    mapa = folium.Map(
        location=[latitude, longitude],
        zoom_start=18,
        control_scale=False,
        height="100%",
    )

    folium.TileLayer(
        tiles="https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
        attr="Google",
        name="Google Satellite",
        subdomains=["mt0", "mt1", "mt2", "mt3"],
    ).add_to(mapa)

    folium.Marker(
        [latitude, longitude],
        popup=coleira["nomeColeira"],
        icon=folium.Icon(color="red", icon="paw", prefix="fa"),
    ).add_to(mapa)

    folium.Circle(
        location=[CENTER_COORDINATES["latitude"], CENTER_COORDINATES["longitude"]],
        radius=coleira["distanciaMaxima"],
        color="red",
        fill=True,
        fill_opacity=0.15,
    ).add_to(mapa)

    return mapa._repr_html_()
