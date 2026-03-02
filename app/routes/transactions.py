from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import Transaction, Category, TransactionType
from ..extensions import db
from datetime import datetime

transactions_bp = Blueprint('transactions', __name__, template_folder='../templates')

# --- INDEX ---
@transactions_bp.route('/')
@login_required
def index():
    # Get filters
    category_filter = request.args.get('category', type=int)
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    sort_by = request.args.get('sort_by', 'date')

    # Initial query
    query = Transaction.query.filter_by(user_id=current_user.id)

    # Apply filters
    if category_filter:
        query = query.filter_by(category_id=int(category_filter))
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            query = query.filter(Transaction.date >= start_date)
        except:
            flash('Invalid start date', 'error')
    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            query = query.filter(Transaction.date <= end_date)
        except:
            flash('Invalid end date', 'error')

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
        current_filter=int(category_filter) if category_filter else None,
        sort_by = sort_by if sort_by else 'date'
    )


# --- ADD TRANSACTION ---
@transactions_bp.route('/add', methods=['POST'])
@login_required
def add_transaction():
    errors, date, category, description, amount, type = validate_transaction_form(request.form)

    if errors:
        for e in errors:
            flash(e, 'error')
        return redirect(url_for('transaction.index'))

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
    return redirect(url_for('transaction.index', category=request.args.get('category')))


# --- EDIT TRANSACTION ---
@transactions_bp.route('/edit/<int:tx_id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(tx_id):
    tx = Transaction.query.filter_by(id=tx_id, user_id=current_user.id).first_or_404()

    if request.method == 'POST':
        errors, date, category, description, amount, type = validate_transaction_form(request.form)
        if errors:
            for e in errors:
                flash(e, 'error')
            return redirect(url_for('transaction.edit_transaction', tx_id=tx_id, category=request.args.get('category')))

        tx.date = date
        tx.category_id = category.id
        tx.description = description
        tx.amount = amount
        tx.type = type
        
        db.session.commit()
        flash("Transaction updated successfully.", 'success')
        return redirect(url_for('transaction.index', category=request.args.get('category')))
    
    categories = Category.query.all()
    return render_template('edit.html', transaction=tx, categories=categories)


# --- DELETE TRANSACTION ---
@transactions_bp.route('/delete/<int:tx_id>', methods=['POST'])
@login_required
def delete_transaction(tx_id):
    tx = Transaction.query.filter_by(id=tx_id, user_id=current_user.id).first_or_404()
    if tx:
        db.session.delete(tx)
        db.session.commit()
    return redirect(url_for('transaction.index', category=request.args.get('category')))