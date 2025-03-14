from flask import Flask
from src.database import db, migrate

def create_app():
    # Cria a instância do Flask
    app = Flask(__name__)

    # Configuração do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@db/mydb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa o SQLAlchemy e o Migrate com o app
    db.init_app(app)
    migrate.init_app(app, db)

    # Importa e registra as rotas
    from src.routes import main_routes
    app.register_blueprint(main_routes)

    return app