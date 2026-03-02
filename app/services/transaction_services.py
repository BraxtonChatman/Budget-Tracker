from app.models import Transaction, Category
from app.extensions import db
from app.forms import validate_transaction_form
from datetime import datetime

def get_transaction_dashboard_data(user, category_filter=None, sort_by=None, start_date_str=None, end_date_str=None):
    """
    Returns:
        transactions: list of Transaction
        totals: dict with income, expense, balance
        categories: list of Category
    """
    # Initial query
    query = Transaction.query.filter_by(user_id=user.id)

    # Apply category filter 
    if category_filter:
        query = query.filter_by(category_id=int(category_filter))

    # Parse date filters
    errors = []
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            query = query.filter(Transaction.date >= start_date)
        except ValueError:
            errors.append('Invalid start date')
    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            query = query.filter(Transaction.date <= end_date)
        except ValueError:
            errors.append('Invalid end date')

    # Apply sorting
    if sort_by == 'date':
        query = query.order_by(Transaction.date.desc())
    elif sort_by == 'amount':
        query = query.order_by(Transaction.amount.desc())
    elif sort_by == 'type':
        query = query.order_by(Transaction.type, Transaction.date.desc(), Transaction.amount.desc()) 
    else:
        query = query.order_by(Transaction.date.desc())

    transactions = query.all()

    # Calculate totals
    totals = {}
    totals['income'] = sum(t.amount for t in transactions if t.type.value == 'Income')
    totals['expense'] = sum(t.amount for t in transactions if t.type.value == 'Expense')
    totals['net'] = totals['income'] - totals['expense']

    categories = Category.query.all()

    return transactions, totals, categories, errors

def add_transaction_for_user(user, form):
    """
    Validates the form and creates a transaction for the given user.
    Returns (success: bool, errors: list[str])
    """
    errors, date, category, description, amount, type = validate_transaction_form(form)
    if errors:
        return False, errors

    new_transaction = Transaction(
        date=date, 
        category_id=category.id, 
        description=description, 
        amount=amount,
        type=type,
        user_id = user.id
    )
    db.session.add(new_transaction)
    db.session.commit()
    return True, None

def edit_transaction_for_user(user, tx_id, form):
    """
    Validates the form and edits a transaction for the given user.
    Returns (success: bool, errors: list[str])
    """
    tx = Transaction.query.filter_by(id=tx_id, user_id=user.id).first()
    if not tx:
        return False, ["Transaction not found."]
    
    errors, date, category, description, amount, type = validate_transaction_form(form)
    if errors:
        return False, errors

    tx.date = date
    tx.category_id = category.id
    tx.description = description
    tx.amount = amount
    tx.type = type
    
    db.session.commit()
    return True, []
    
def get_transaction_and_categories(user, tx_id):
    """
    Returns the transaction object and all categories (for GET form rendering).
    """
    tx = Transaction.query.filter_by(id=tx_id, user_id=user.id).first_or_404()
    categories = Category.query.all()
    return tx, categories

def delete_transaction_by_id(user, tx_id):
    """
    Deletes transaction with the given id for the given user.
    Returns (success: bool)
    """
    tx = Transaction.query.filter_by(id=tx_id, user_id=user.id).first_or_404()
    if tx:
        db.session.delete(tx)
        db.session.commit()
        return True
    
    return False
