from flask import Flask, render_template, request, redirect, url_for, flash
from models import Category, db, Transaction
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget.db'
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


# --- INDEX / LIST ---
@app.route('/')
def index():
    category_filter = request.args.get('category')
    if category_filter:
        transactions = Transaction.query.filter_by(category_id=int(category_filter)).all()
    else:
        transactions = Transaction.query.all()
        
    total = sum(t.amount for t in transactions)
    categories = Category.query.all()

    return render_template(
        'index.html', 
        transactions=transactions, 
        total=total, 
        categories=categories, 
        current_filter=int(category_filter) if category_filter else None
    )


# --- ADD TRANSACTION ---
@app.route('/add', methods=['POST'])
def add_transaction():
    errors, date, category, description, amount = validate_transaction_form(request.form)

    if errors:
        for e in errors:
            flash(e, 'error')
        return redirect(url_for('index'))

    new_transaction = Transaction(
        date=date, 
        category_id=category.id, 
        description=description, 
        amount=amount
    )
    db.session.add(new_transaction)
    db.session.commit()
    flash("Transaction added successfully.", 'success')
    return redirect(url_for('index'))


# --- EDIT TRANSACTION ---
@app.route('/edit/<int:tx_id>', methods=['GET', 'POST'])
def edit_transaction(tx_id):
    tx = Transaction.query.get_or_404(tx_id)

    if request.method == 'POST':
        errors, date, category, description, amount = validate_transaction_form(request.form)
        if errors:
            for e in errors:
                flash(e, 'error')
            return redirect(url_for('edit_transaction', tx_id=tx_id))

        tx.date = date
        tx.category_id = category.id
        tx.description = description
        tx.amount = amount
        
        db.session.commit()
        flash("Transaction updated successfully.", 'success')
        return redirect(url_for('index'))
    
    categories = Category.query.all()
    return render_template('edit.html', transaction=tx, categories=categories)


# --- DELETE TRANSACTION ---
@app.route('/delete/<int:tx_id>', methods=['POST'])
def delete_transaction(tx_id):
    tx = Transaction.query.get(tx_id)
    if tx:
        db.session.delete(tx)
        db.session.commit()
    return redirect(url_for('index'))


# --- Input Validation  Helper Function ---
def validate_transaction_form(form):
    date_str = form.get('date')
    category_id_str = form.get('category')
    description = form.get('description', '').strip()
    amount_str = form.get('amount')

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

    # Default description if empty
    if not description:
        description = "(No description)"
    
    return errors, date, category, description, amount


if __name__ == "__main__":
    app.run(debug=True)