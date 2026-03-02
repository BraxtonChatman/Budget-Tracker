import random
from datetime import datetime, timedelta
from app.extensions import db
from app.models import db, Category, Transaction, TransactionType, User

def create_demo_account():
    demo_username = 'demo'
    demo_password = 'demo1234'

    demo_user = User.query.filter_by(username=demo_username).first()
    if not demo_user:
        demo_user = User(username = demo_username)
        demo_user.set_password(demo_password)
        db.session.add(demo_user)
        db.session.commit()

    # Populate demo account transactions
    if Transaction.query.filter_by(user_id=demo_user.id).first():
        return
    
    categories = Category.query.all()
    types = [TransactionType('Income'), TransactionType('Expense')]

    for i in range(30):
        category = random.choice(categories)
        tx_type = random.choice(types)
        amount = round(random.uniform(10, 500), 2)
        date = datetime.today() - timedelta(days=random.randint(0,30))
        description = f"Demo transaction {i+1}"

        demo_tx = Transaction(
            date=date,
            category_id=category.id,
            description=description,
            amount=amount,
            type=tx_type,
            user_id=demo_user.id
        )
        db.session.add(demo_tx)
    db.session.commit()

