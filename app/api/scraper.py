from flask import Blueprint, request, jsonify
from app.services.scraper_service import run_scraper

scraper_bp = Blueprint("scraper", __name__)


@scraper_bp.route("/scrape/<farmacia>", methods=["POST"])
def scrape(farmacia):
    body = request.get_json() or {}
    query = body.get("query")

    if not query:
        return jsonify({"error": "campo 'query' é obrigatório"}), 400

    try:
        result = run_scraper(farmacia, query)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
