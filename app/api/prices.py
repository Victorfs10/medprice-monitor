from flask import Blueprint, jsonify
from app.services.price_service import get_precos, get_preco_by_id

prices_bp = Blueprint("prices", __name__)


@prices_bp.route("/precos", methods=["GET"])
def list_precos():
    return jsonify(get_precos()), 200


@prices_bp.route("/precos/<int:id>", methods=["GET"])
def get_preco(id):
    preco = get_preco_by_id(id)
    if not preco:
        return jsonify({"error": "não encontrado"}), 404
    return jsonify(preco), 200
