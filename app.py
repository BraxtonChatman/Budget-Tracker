from flask import Flask, render_template, request, redirect, url_for
from models import Category, db, Transaction
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    date_str = request.form['date']
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    category_id = int(request.form['category'])
    description = request.form['description']
    amount = float(request.form['amount'])

    new_transaction = Transaction(
        date=date, 
        category_id=category_id, 
        description=description, 
        amount=amount
    )
    db.session.add(new_transaction)
    db.session.commit()

    return redirect(url_for('index'))

# --- DELETE TRANSACTION ---
@app.route('/delete/<int:tx_id>', methods=['POST'])
def delete_transaction(tx_id):
    tx = Transaction.query.get(tx_id)
    if tx:
        db.session.delete(tx)
        db.session.commit()
    return redirect(url_for('index'))

# --- EDIT TRANSACTION ---
@app.route('/edit/<int:tx_id>', methods=['GET', 'POST'])
def edit_transaction(tx_id):
    tx = Transaction.query.get_or_404(tx_id)

    if request.method == 'POST':
        date_str = request.form['date']
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        tx.date = date
        tx.category_id = int(request.form['category'])
        tx.description = request.form['description']
        tx.amount = float(request.form['amount'])
        db.session.commit()
        return redirect(url_for('index'))
    
    categories = Category.query.all()
    return render_template('edit.html', transaction=tx, categories=categories)

if __name__ == "__main__":
    app.run(debug=True)