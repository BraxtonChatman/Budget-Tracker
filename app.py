from flask import Flask, render_template, request, redirect, url_for
from models import db, Transaction

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create Database tables
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    category_filter = request.args.get('category')
    if category_filter:
        transactions = Transaction.query.filter_by(category=category_filter).all()
    else:
        transactions = Transaction.query.all()
        
    total = sum(t.amount for t in transactions)
    categories = [c[0] for c in db.session.query(Transaction.category).distinct().all()]

    return render_template('index.html', transactions=transactions, total=total, categories=categories, current_filter=category_filter)

@app.route('/add', methods=['POST'])
def add_transaction():
    date = request.form['date']
    category = request.form['category']
    description = request.form['description']
    amount = float(request.form['amount'])

    new_transaction = Transaction(date=date, category=category, description=description, amount=amount)
    db.session.add(new_transaction)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/delete/<int:tx_id>', methods=['POST'])
def delete_transaction(tx_id):
    tx = Transaction.query.get(tx_id)
    if tx:
        db.session.delete(tx)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)