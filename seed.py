import json
from datetime import datetime
import argparse
from app import create_app
from app.extensions import db
from app.models import User, Transaction, TransactionType, Category    

def seed_data():
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

def main():
    parser = argparse.ArgumentParser(description='Seed the data')
    parser.add_argument('--env', default='dev', choices=['dev', 'production'], help='Environment: dev or production')
    parser.add_argument('--reset', action='store_true', help='Drop tables first')

    args = parser.parse_args()

    app = create_app(args.env)

    with app.app_context():
        if args.reset:
            db.drop_all()
        
        db.create_all()
        seed_data()
        print("Database Seeded.")

if __name__=='__main__':
    main()