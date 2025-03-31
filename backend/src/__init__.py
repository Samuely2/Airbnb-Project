from flask import Flask, jsonify, request
from flask_cors import CORS
from src.database import db, migrate
from src.Application.Routes.HallsRoutes import hall_bp
from src.Application.Routes.ReservationRoutes import reservation_bp
from src.Application.Routes.UserRoutes import user_bp

def create_app():
    app = Flask(__name__)

    # Configurações do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@db/mydb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicialização do banco de dados e migrações
    db.init_app(app)
    migrate.init_app(app, db)

    # Configuração do CORS
    CORS(app,
         origins=["http://localhost:3000"],  # Permite apenas o frontend
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         expose_headers=["Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    # Registro dos blueprints
    app.register_blueprint(hall_bp)
    app.register_blueprint(reservation_bp)
    app.register_blueprint(user_bp)

    # Middleware para adicionar cabeçalhos CORS em todas as respostas
    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Expose-Headers"] = "Authorization"
        return response
    return app