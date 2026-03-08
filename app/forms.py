from datetime import datetime
from decimal import Decimal
from .models import Category, TransactionType

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
            amount = Decimal(amount_str)
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
    if len(description) > 200:
        errors.append("Description must be 200 characters or fewer.")
    
    return errors, date, category, description, amount, type