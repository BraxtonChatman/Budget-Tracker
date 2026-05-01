from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.services.transaction_services import (
    add_transaction_for_user, 
    delete_transaction_by_id, 
    edit_transaction_for_user, 
    get_transaction_and_categories, 
    get_transaction_dashboard_data
)

api_transactions_bp = Blueprint('api_transactions', __name__, url_prefix='/api/transactions')

# --- GET TRANSACTIONS (ALL) ---
@api_transactions_bp.route('', methods=['GET'])
@login_required
def get_transactions():
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

    return jsonify({
        'transactions': [t.to_dict() for t in transactions],
        'totals': totals,
        'categories': [c.to_dict() for c in categories],
        'errors': errors
    })


# --- GET TRANSACTION (id) ---
@api_transactions_bp.route('/<int:tx_id>', methods=['GET'])
@login_required
def get_transaction(tx_id):    
    tx, categories = get_transaction_and_categories(current_user, tx_id)

    if not tx:
        return jsonify({'error': 'Transaction not found'}), 404

    return jsonify({
        'transaction': tx.to_dict(),
        'categories': [c.to_dict() for c in categories]
    })


# --- POST TRANSACTION ---
@api_transactions_bp.route('', methods=['POST'])
@login_required
def post_transaction():
    pass


# --- PATCH TRANSACTION (id) ---
@api_transactions_bp.route('/<int:tx_id>', methods=['PATCH'])
@login_required
def update_transaction(tx_id):
    pass


# --- DELETE TRANSACTION (id) ---
@api_transactions_bp.route('/<int:tx_id>', methods=['DELETE'])
@login_required
def delete_transaction(tx_id):
    pass