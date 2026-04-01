from flask import Flask
from app.api.prices import prices_bp
from app.api.scraper import scraper_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(prices_bp)
    app.register_blueprint(scraper_bp)
    return app
