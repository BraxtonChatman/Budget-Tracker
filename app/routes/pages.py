from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Category

pages_bp = Blueprint("pages", __name__)

@pages_bp.route("/")
def index():
    categories = Category.query.all()

    return render_template(
        "index.html",
        categories=categories
    )