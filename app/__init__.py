import os
from flask import Flask, jsonify, request, redirect
from .extensions import db, login_manager
from .models import User, Category
from .routes.auth import auth_bp
from .routes.transactions import transactions_bp
from .api.transactions import api_transactions_bp
from .api.auth import api_auth_bp
from .filters import format_currency
from .config import DevConfig, ProdConfig, TestConfig

def create_app(config_name = None):
    app = Flask(__name__, instance_relative_config=True)

    # configure app
    if config_name == 'testing':
        app.config.from_object(TestConfig)
        app.config['SECRET_KEY'] = 'testkey'
    elif config_name == 'production':
        app.config.from_object(ProdConfig)
        if 'SECRET_KEY' not in os.environ:
            raise RuntimeError("SECRET_KEY environment variable is required for production!")
        app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    else:
        app.config.from_object(DevConfig)
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'devkey')

    # Adjust SQLite path dynamically
    if not app.config.get("TESTING", False) and app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite:///'):
        db_path = os.path.join(app.instance_path, 'budget.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    
    # initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # User loader
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))
    
    # Unauthorized login handler
    @login_manager.unauthorized_handler
    def unauthorized():
        if request.path.startswith("/api"):
            return jsonify({"errors": ["Unauthorized"]}), 401
        return redirect('/login')
    
    # register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(transactions_bp)

    app.register_blueprint(api_transactions_bp)
    app.register_blueprint(api_auth_bp)

    # filters
    app.add_template_filter(format_currency)

    return app

