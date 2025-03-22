from flask import Flask
from flasgger import Swagger
from src.database import db, migrate
from src.Application.Routes.HallsRoutes import hall_bp
from src.Application.Routes.TypeHallsRoutes import typehall_bp
from src.Application.Routes.ReservationRoutes import reservation_bp
from src.Application.Routes.UserRoutes import user_bp

def create_app():
    app = Flask(__name__)

    # Configuração do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@db/mydb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa o SQLAlchemy e o Migrate com o app
    db.init_app(app)
    migrate.init_app(app, db)

    # Inicializa o Swagger
    Swagger(app)

    # Registra as Blueprints
    app.register_blueprint(hall_bp)
    app.register_blueprint(typehall_bp)
    app.register_blueprint(reservation_bp)
    app.register_blueprint(user_bp)

    return app
