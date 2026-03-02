import os
from flask import Flask
from .extensions import db, login_manager
from .models import User, Category
from .routes.auth import auth_bp
from .routes.transactions import transactions_bp



def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # configure app
    db_path = os.path.join(app.instance_path, 'budget.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}' 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = os.environ.get('SECRET_KEY', 'devkey')

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

    from . import seed

    # Create tables and seed demo account
    with app.app_context():
        db.create_all()
        if not Category.query.first():
            for name in ['Food', 'Rent', 'Transport', 'Entertainment', 'Utilities', 'Other']:
                db.session.add(Category(name=name))
            db.session.commit()
        seed.create_demo_account()

    # --- TEMPLATE FILTERS ---
    @app.template_filter()
    def format_currency(value, show_sign=False):
        try:
            value = float(value)
        except (TypeError, ValueError):
            return "$0.00"

        formatted = "${:,.2f}".format(abs(value))

        if show_sign:
            if value < 0:
                return f"-{formatted}"
            else:
                return formatted
        return formatted

    return app