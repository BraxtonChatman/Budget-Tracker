from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import Category, db, Transaction, TransactionType, User
import seed
from datetime import datetime
import os

app = Flask(__name__, instance_relative_config=True)

db_path = os.path.join(app.instance_path, 'budget.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SECRET_KEY', 'devkey')

db.init_app(app)

# Create Database tables
with app.app_context():
    db.create_all()
    if not Category.query.first():
        for name in ['Food', 'Rent', 'Transport', 'Entertainment', 'Utilities', 'Other']:
            db.session.add(Category(name=name))
        db.session.commit()
    seed.create_demo_account()

# Handle login manager setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- REGISTER USER ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash("Username already exists", "error")
            return redirect(url_for('register'))
        
        user = User(username=username)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Account created. Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')


# --- LOGIN ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash("Invalid credentials", "error")

    return render_template('login.html')


# -- LOGOUT ---
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# --- INDEX / LIST ---
@app.route('/')
@login_required
def index():
    category_filter = request.args.get('category')
    if category_filter:
        transactions = Transaction.query.filter_by(category_id=int(category_filter), user_id=current_user.id).all()
    else:
        transactions = Transaction.query.filter_by(user_id=current_user.id)
        
    total_income = sum(t.amount for t in transactions if t.type.value == 'Income')
    total_expense = sum(t.amount for t in transactions if t.type.value == 'Expense')
    net_total = total_income - total_expense
    categories = Category.query.all()

    return render_template(
        'index.html', 
        transactions=transactions, 
        total_income=total_income,
        total_expense=total_expense,
        net_total=net_total,
        categories=categories, 
        current_filter=int(category_filter) if category_filter else None
    )


# --- ADD TRANSACTION ---
@app.route('/add', methods=['POST'])
@login_required
def add_transaction():
    errors, date, category, description, amount, type = validate_transaction_form(request.form)

    if errors:
        for e in errors:
            flash(e, 'error')
        return redirect(url_for('index'))

    new_transaction = Transaction(
        date=date, 
        category_id=category.id, 
        description=description, 
        amount=amount,
        type=type
    )
    new_transaction.user_id = current_user.id
    db.session.add(new_transaction)
    db.session.commit()
    flash("Transaction added successfully.", 'success')
    return redirect(url_for('index'))


# --- EDIT TRANSACTION ---
@app.route('/edit/<int:tx_id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(tx_id):
    tx = Transaction.query.filter_by(id=tx_id, user_id=current_user.id).first_or_404()

    if request.method == 'POST':
        errors, date, category, description, amount, type = validate_transaction_form(request.form)
        if errors:
            for e in errors:
                flash(e, 'error')
            return redirect(url_for('edit_transaction', tx_id=tx_id))

        tx.date = date
        tx.category_id = category.id
        tx.description = description
        tx.amount = amount
        tx.type = type
        
        db.session.commit()
        flash("Transaction updated successfully.", 'success')
        return redirect(url_for('index'))
    
    categories = Category.query.all()
    return render_template('edit.html', transaction=tx, categories=categories)


# --- DELETE TRANSACTION ---
@app.route('/delete/<int:tx_id>', methods=['POST'])
@login_required
def delete_transaction(tx_id):
    tx = Transaction.query.filter_by(id=tx_id, user_id=current_user.id).first_or_404()
    if tx:
        db.session.delete(tx)
        db.session.commit()
    return redirect(url_for('index'))


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


# --- INPUT VALIDATION HELPER ---
def validate_transaction_form(form):
    date_str = form.get('date')
    category_id_str = form.get('category')
    description = form.get('description', '').strip()
    amount_str = form.get('amount')
    type_str = form.get('type')

    # Validation
    errors = []

    # Validate date
    date = None
    if not date_str:
        errors.append("Date is required.")
    else:
        try: 
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            errors.append("Invalid date format.")

    # Validate category
    category = None
    if not category_id_str:
        errors.append("Category is required.")
    else:
        try:
            category_id = int(category_id_str)
            category = Category.query.get(category_id)
            if not category:
                errors.append("Selected category does not exist.")
        except ValueError:
            errors.append("Category ID must be a valid number.")

    # Validate amount
    amount = None
    if not amount_str:
        errors.append("Amount is required.")
    else:
        try:
            amount = float(amount_str)
            if amount <= 0:
                errors.append("Amount must be greater than zero.")
        except (TypeError, ValueError):
            errors.append("Amount must be a valid number.")

    # Validate type
    type = None
    if type_str not in ['Income', 'Expense']:
        errors.append("Type must be either 'Income' or 'Expense'.")
    else:
        type = TransactionType(type_str)

    # Default description if empty
    if not description:
        description = "(No description)"
    
    return errors, date, category, description, amount, type


if __name__ == "__main__":
    app.run(debug=True)