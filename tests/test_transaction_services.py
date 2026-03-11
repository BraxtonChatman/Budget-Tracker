import pytest
from app.extensions import db
from app.models import Transaction, TransactionType
from app.services.transaction_services import edit_transaction_for_user, get_transaction_dashboard_data, add_transaction_for_user, delete_transaction_by_id, get_transaction_and_categories
from datetime import date
from decimal import Decimal

@pytest.mark.parametrize('tx_inputs, exp_totals', 
                         [
                            ([{'amount': 0, 'type': TransactionType.Income}], {'income': 0, 'expense': 0, 'net': 0}),
                            ([{'amount': 99.99, 'type': TransactionType.Income}], {'income': Decimal('99.99'), 'expense': 0, 'net': Decimal('99.99')}),
                            ([{'amount': 99.99, 'type': TransactionType.Expense}], {'income': Decimal('0'), 'expense': Decimal('99.99'), 'net': Decimal('-99.99')}),
                            ([{'amount': 99.99, 'type': TransactionType.Expense}], {'income': Decimal('0'), 'expense': Decimal('99.99'), 'net': Decimal('-99.99')}),
                            ([{'amount': 99.99, 'type': TransactionType.Expense}, {'amount': 100.01, 'type': TransactionType.Expense}], {'income': Decimal('0'), 'expense': Decimal('200.00'), 'net': Decimal('-200.00')}),
                            ([{'amount': 99.99, 'type': TransactionType.Income}, {'amount': 100.01, 'type': TransactionType.Income}], {'income': Decimal('200.00'), 'expense': Decimal('0.00'), 'net': Decimal('200.00')}),
                            ([{'amount': 125.45, 'type': TransactionType.Income}, {'amount': 23.12, 'type': TransactionType.Expense}], {'income': Decimal('125.45'), 'expense': Decimal('23.12'), 'net': Decimal('102.33')})
                         ])
def test_dashboard_totals(test_user, create_tx_for_testuser, tx_inputs, exp_totals):

    for tx in tx_inputs:
        new_tx = create_tx_for_testuser(tx['amount'], tx['type'])
        db.session.add(new_tx)
    db.session.commit()

    _, totals, _, errors = get_transaction_dashboard_data(test_user)

    assert totals['income'] == exp_totals['income']
    assert totals['expense'] == exp_totals['expense']
    assert totals['net'] == exp_totals['net']
    assert errors == []

def test_dashboard_empty_list(test_user, test_category):
    transactions, totals, categories, errors = get_transaction_dashboard_data(test_user)

    assert transactions == []
    assert totals['income'] == 0
    assert totals['expense'] == 0
    assert totals['net'] == 0
    assert categories == [test_category]
    assert errors == []

def test_dashboard_sorting_amount(test_user, test_tx_for_sorting):
    transactions, _, _, errors = get_transaction_dashboard_data(test_user, sort_by='amount')

    assert errors == []
    assert transactions[0] == test_tx_for_sorting[2]
    assert transactions[1] == test_tx_for_sorting[1]
    assert transactions[2] == test_tx_for_sorting[0]

def test_dashboard_sorting_date(test_user, test_tx_for_sorting):
    transactions, _, _, errors = get_transaction_dashboard_data(test_user, sort_by='date')

    assert errors == []
    assert transactions[0] == test_tx_for_sorting[0]
    assert transactions[1] == test_tx_for_sorting[1]
    assert transactions[2] == test_tx_for_sorting[2]

def test_dashboard_sorting_type(test_user, test_tx_for_sorting):
    transactions, _, _, errors = get_transaction_dashboard_data(test_user, sort_by='type')

    assert errors == []
    assert transactions[0] == test_tx_for_sorting[1]
    assert transactions[1] == test_tx_for_sorting[0]
    assert transactions[2] == test_tx_for_sorting[2]

def test_dashboard_cat_filtering1(test_user, test_tx_for_test_user2, test_category, test_category2):
    transactions, _, categories, errors = get_transaction_dashboard_data(test_user, category_filter=str(test_category2.id))
    assert transactions == [test_tx_for_test_user2]
    assert test_category in categories
    assert test_category2 in categories
    assert errors == []

def test_dashboard_cat_filtering2(test_user, test_tx_for_test_user, test_category, test_category2):
    transactions, _, categories, errors = get_transaction_dashboard_data(test_user, category_filter=str(test_category.id))
    assert transactions == [test_tx_for_test_user]
    assert test_category in categories
    assert test_category2 in categories
    assert errors == []

def test_dashboard_end_filtering(test_user, test_tx_for_test_user, test_category, test_category2):
    transactions, _, categories, errors = get_transaction_dashboard_data(test_user, end_date_str='2026-03-07')
    assert transactions == [test_tx_for_test_user]
    assert test_category in categories
    assert test_category2 in categories
    assert errors == []

def test_dashboard_end_filtering_empty(test_user, test_category, test_category2):
    transactions, _, categories, errors = get_transaction_dashboard_data(test_user, start_date_str='2026-03-01')
    assert transactions == []
    assert test_category in categories
    assert test_category2 in categories
    assert errors == []

def test_dashboard_start_filtering(test_user, test_tx_for_test_user2, test_category, test_category2):
    transactions, _, categories, errors = get_transaction_dashboard_data(test_user, start_date_str='2026-03-07')
    assert transactions == [test_tx_for_test_user2]
    assert test_category in categories
    assert test_category2 in categories
    assert errors == []

def test_dashboard_start_filtering_empty(test_user, test_category, test_category2):
    transactions, _, categories, errors = get_transaction_dashboard_data(test_user, start_date_str='2026-03-10')
    assert transactions == []
    assert test_category in categories
    assert test_category2 in categories
    assert errors == []

def test_get_dashboard_invalid_end_date(test_user, test_tx_for_test_user, test_category):
    transactions, totals, categories, errors = get_transaction_dashboard_data(test_user, end_date_str='-9')

    assert transactions == [test_tx_for_test_user]
    assert categories == [test_category]
    assert 'Invalid end date' in errors
    assert totals['net'] == Decimal('-25.50')
    assert totals['income'] == Decimal('0.00')
    assert totals['expense'] == Decimal('25.50')

def test_get_dashboard_invalid_start_date(test_user, test_tx_for_test_user, test_category):
    transactions, totals, categories, errors = get_transaction_dashboard_data(test_user, start_date_str='-9')

    assert transactions == [test_tx_for_test_user]
    assert categories == [test_category]
    assert 'Invalid start date' in errors
    assert totals['net'] == Decimal('-25.50')
    assert totals['income'] == Decimal('0.00')
    assert totals['expense'] == Decimal('25.50')

def test_get_dashboard_success(test_user, test_tx_for_test_user, test_category):
    transactions, totals, categories, errors = get_transaction_dashboard_data(test_user)

    assert transactions == [test_tx_for_test_user]
    assert categories == [test_category]
    assert errors == []
    assert totals['net'] == Decimal('-25.50')
    assert totals['income'] == Decimal('0.00')
    assert totals['expense'] == Decimal('25.50')

def test_add_transaction_fail(test_user, invalid_form):
    success, errors = add_transaction_for_user(test_user, invalid_form)

    assert success is False
    assert "Invalid date format." in errors

def test_add_transaction_success(test_user, test_form):
    success, errors = add_transaction_for_user(test_user, test_form)

    assert success is True
    assert errors == []

def test_edit_transaction_no_tx(test_user, test_form):
    success, errors = edit_transaction_for_user(test_user, 9999, test_form)

    assert success is False
    assert "Transaction not found." in errors

def test_edit_transaction_invalid_form(test_user, test_tx_for_test_user, invalid_form):
    success, errors = edit_transaction_for_user(test_user, test_tx_for_test_user.id, invalid_form)

    assert success is False
    assert errors != []

def test_edit_transaction_user_boundary(another_user, test_form, test_tx_for_test_user):
    success, errors = edit_transaction_for_user(another_user, test_tx_for_test_user.id, test_form)

    assert success is False
    assert "Transaction not found." in errors
    
def test_edit_transaction_success(test_user, test_tx_for_test_user, test_form):
    success, errors = edit_transaction_for_user(test_user, test_tx_for_test_user.id, test_form)

    assert success is True
    assert errors == []

def test_get_transaction_and_categories_success(test_user, test_tx_for_test_user, test_category):
    tx, categories = get_transaction_and_categories(test_user, test_tx_for_test_user.id)

    assert tx == test_tx_for_test_user
    assert categories == [test_category]

def test_get_transaction_and_categories_not_found(test_user):
    tx, categories = get_transaction_and_categories(test_user, 1)

    assert tx == None
    assert categories == []

def test_get_transaction_and_categories_no_tx(test_user, test_category):
    tx, categories = get_transaction_and_categories(test_user, 1)

    assert tx == None
    assert categories == [test_category]

def test_delete_transaction_success(test_user, test_tx_for_test_user):
    success = delete_transaction_by_id(test_user, test_tx_for_test_user.id)

    assert success is True

def test_delete_transaction_not_found(test_user):
    success = delete_transaction_by_id(test_user, 9999)

    assert success is False

def test_delete_transaction_user_boundary(another_user, test_tx_for_test_user):
    success = delete_transaction_by_id(another_user, test_tx_for_test_user.id)

    assert success is False
