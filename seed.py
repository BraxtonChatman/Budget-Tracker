import json
from datetime import datetime
from app import create_app
from app.extensions import db
from app.models import User, Transaction, TransactionType, Category

def load_seed_data():
    app = create_app()
    with app.app_context():
        db.create_all()
        with open('app/seed_data.json') as f:
            data = json.load(f)
        
        # Users
        for u in data.get('users', []):
            if not User.query.filter_by(username=u['username']).first():
                user = User(username=u['username'])
                user.set_password(u['password'])
                db.session.add(user)
        db.session.commit()

        # Categories
        for c in data.get('categories', []):
            if not Category.query.filter_by(name=c['name']).first():
                db.session.add(Category(name=c['name']))
        db.session.commit()

        # Transactions
        for t in data.get('transactions', []):
            user = User.query.filter_by(username=t['user']).first()
            category = Category.query.get(t['category_id'])
            if user and category:
                if Transaction.query.filter_by(user_id=user.id, description=t["description"], date=t["date"]).first():
                    continue  
                tx = Transaction(
                    user_id=user.id,
                    category_id=category.id,
                    type=TransactionType[t['type']],
                    amount=t['amount'],
                    description=t['description'],
                    date=datetime.strptime(t['date'], '%Y-%m-%d').date()
                )
                db.session.add(tx)
        db.session.commit()

if __name__=='__main__':
    load_seed_data()
    print('Demo Data Loaded')