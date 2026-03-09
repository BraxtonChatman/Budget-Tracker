import pytest
from app.forms import validate_transaction_form
from app.models import TransactionType
from decimal import Decimal

def test_form_no_date(test_form):
    test_form['date'] = ''
    errors, date, *_ = validate_transaction_form(test_form)

    assert "Date is required." in errors
    assert date is None

def test_form_invalid_date(test_form):
    test_form['date'] = '3/2/1980'
    errors, date, *_ = validate_transaction_form(test_form)

    assert "Invalid date format." in errors
    assert date is None

def test_form_no_category(test_form):
    test_form['category'] = ''
    errors, _, category, *_ = validate_transaction_form(test_form)

    assert "Category is required." in errors
    assert category == None

def test_form_category_not_exist(test_form):
    test_form['category'] = '-9999'
    errors, _, category, *_ = validate_transaction_form(test_form)

    assert "Selected category does not exist." in errors
    assert category is None

def test_form_invalid_category(test_form):
    test_form['category'] = 'a'
    errors, _, category, *_ = validate_transaction_form(test_form)

    assert "Category ID must be a valid number." in errors
    assert category is None

def test_form_no_amount(test_form):
    test_form['amount'] = ''
    errors, _, _, _, amount, _ = validate_transaction_form(test_form)

    assert "Amount is required." in errors
    assert amount is None

@pytest.mark.parametrize("amount", ['0', '-10', '000', '0.0'])
def test_form_non_positive_amount(test_form, amount):
    test_form['amount'] = amount
    errors, *_ = validate_transaction_form(test_form)

    assert "Amount must be greater than zero." in errors

@pytest.mark.parametrize("amount_param", ['a', 'True', 'None', '123-'])
def test_form_invalid_amount(test_form, amount_param):
    test_form['amount'] = amount_param
    errors, _, _, _, amount, _ = validate_transaction_form(test_form)

    assert "Amount must be a valid number." in errors
    assert amount is None

@pytest.mark.parametrize("type_param", ['0', '-10', '0.0', 'a'])
def test_form_invalid_type(test_form, type_param):
    test_form['type'] = type_param
    errors, _, _, _, _, type = validate_transaction_form(test_form)

    assert "Type must be either 'Income' or 'Expense'." in errors
    assert type is None

def test_form_no_description(test_form):
    test_form['description'] = ''
    errors, _, _, description, *_ = validate_transaction_form(test_form)

    assert errors == []
    assert description == '(No description)'

def test_form_description_too_long(test_form):
    test_form['description'] = 201*'a'
    errors, _, _, description, *_ = validate_transaction_form(test_form)

    assert "Description must be 200 characters or fewer." in errors
    assert description == test_form['description']

def test_form_success(test_form, test_category):
    errors, date, category, description, amount, type = validate_transaction_form(test_form)

    assert errors == []
    assert date is not None
    assert category.id == test_category.id
    assert description == test_form['description'] or description == "(No description)"
    assert amount == Decimal(test_form['amount'])
    assert type in [TransactionType.Income, TransactionType.Expense]
