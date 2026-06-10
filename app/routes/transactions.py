from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.transaction_services import add_transaction_for_user, delete_transaction_by_id, edit_transaction_for_user, get_transaction_and_categories, get_transaction_dashboard_data

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

    transactions, totals, categories, errors = get_transaction_dashboard_data(
        current_user, 
        category_filter, 
        sort_by, 
        start_date_str, 
        end_date_str
    )

    for e in errors:
        flash(e, 'error')

    return render_template(
        'index.html', 
        transactions=transactions, 
        total_income=totals['income'],
        total_expense=totals['expense'],
        net_total=totals['net'],
        categories=categories, 
        current_filter=int(category_filter) if category_filter else None,
        sort_by = sort_by if sort_by else 'date'
    )


# --- ADD TRANSACTION ---
@transactions_bp.route('/add', methods=['POST'])
@login_required
def add_transaction():
    success, errors, tx = add_transaction_for_user(current_user, request.form)
    if not success:
        for e in errors:
            flash(e, 'error')
    else:
        flash("Transaction added successfully.", 'success')
    return redirect(url_for('transactions.index', category=request.args.get('category')))


# --- EDIT TRANSACTION ---
@transactions_bp.route('/edit/<int:tx_id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(tx_id):
    category_filter = request.args.get('category')

    if request.method == 'POST':
        success, errors, tx = edit_transaction_for_user(current_user, tx_id, request.form)
        
        if not success:
            for e in errors:
                flash(e, 'error')
        else:
            flash("Transaction updated successfully.", 'success')
        return redirect(url_for('transactions.index', category=category_filter))
    
    tx, categories = get_transaction_and_categories(current_user, tx_id)
    return render_template('edit.html', transaction=tx, categories=categories)

