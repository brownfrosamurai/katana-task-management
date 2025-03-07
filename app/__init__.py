from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restful import Api, Resource

from app.utils.config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)

  CORS(app, resources={r"/*": {"origins": "*"}})  # Allows all origins

  # Security configurations
  app.config["SESSION_COOKIE_HTTPONLY"] = True
  app.config["REMEMBER_COOKIE_HTTPONLY"] = True
  app.config["SESSION_COOKIE_SECURE"] = True  # Only for HTTPS

  db.init_app(app)
  jwt.init_app(app)

  with app.app_context():
    from app.models import task

    from app.v1.routes.tasks import tasks_bp
    from app.v1.routes.analytics import analytics_bp
    from app.v1.routes.auth import auth_bp

    app.register_blueprint(tasks_bp, url_prefix='/v1/tasks')
    app.register_blueprint(analytics_bp, url_prefix='/v1/tasks/analytics')
    app.register_blueprint(auth_bp, url_prefix='/v1/auth')

    db.create_all()

  return app
