import random
from datetime import datetime, timedelta
from models import db, Category, Transaction
from app import app


def seed_random_transactions(n=20):
    with app.app_context():
        categories = Category.query.all()
        if not categories:
            print("No categories found.")
            return

        descriptions = [
            "Groceries", "Gas", "Dinner", "Coffee", "Rent payment",
            "Internet bill", "Gym membership", "Movie ticket",
            "Uber ride", "Clothes", "Books", "Concert ticket",
            "Electric bill", "Water bill", "Subscription",
            "Parking", "Haircut", "Pharmacy", "Gift", "Travel"
        ]

        for _ in range(n):
            random_category = random.choice(categories)
            random_amount = round(random.uniform(5, 500), 2)
            random_days_ago = random.randint(0, 90)
            random_date = datetime.today().date() - timedelta(days=random_days_ago)
            random_type = random.choice(["Income", "Expense"])

            tx = Transaction(
                date=random_date,
                category_id=random_category.id,
                description=random.choice(descriptions),
                amount=random_amount,
                type=random_type
            )

            db.session.add(tx)

        db.session.commit()
        print(f"{n} random transactions added.")


if __name__ == "__main__":
    seed_random_transactions(20)