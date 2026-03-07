import os
from flask import Flask
from .extensions import db, login_manager
from .models import User, Category
from .routes.auth import auth_bp
from .routes.transactions import transactions_bp
from .filters import format_currency
from .config import DevConfig, ProdConfig, TestConfig

def create_app(config_name = None):
    app = Flask(__name__, instance_relative_config=True)

    # configure app
    if config_name == 'testing':
        app.config.from_object(TestConfig)
    elif config_name == 'production':
        app.config.from_object(ProdConfig)
    else:
        app.config.from_object(DevConfig)
    
    # initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # User loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(transactions_bp)

    # filters
    app.add_template_filter(format_currency)

    # Create tables and seed demo account
    with app.app_context():
        db.create_all()
        if not Category.query.first():
            for name in ['Food', 'Rent', 'Transport', 'Entertainment', 'Utilities', 'Other']:
                db.session.add(Category(name=name))
            db.session.commit()

    return app