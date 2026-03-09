import pytest
from app.extensions import db
from app.models import Transaction, TransactionType
from app.services.transaction_services import edit_transaction_for_user

@pytest.mark.skip(reason="Test not yet implemented")
def test_add_transaction_fail():
    pass

@pytest.mark.skip(reason="Test not yet implemented")
def test_add_transaction_success():
    pass

@pytest.mark.skip(reason="Test not yet implemented")
def test_edit_transaction_no_tx():
    pass

@pytest.mark.skip(reason="Test not yet implemented")
def test_edit_transaction_invalid_tx():
    pass

def test_edit_transaction_user_boundary(another_user, test_form, test_tx_for_test_user):
    success, errors = edit_transaction_for_user(another_user, test_tx_for_test_user.id, test_form)

    assert success is False
    assert "Transaction not found." in errors
    

@pytest.mark.skip(reason="Test not yet implemented")
def test_edit_transaction_success():
    pass

@pytest.mark.skip(reason="Test not yet implemented")
def test_get_transaction_and_categories_success():
    pass

@pytest.mark.skip(reason="Test not yet implemented")
def test_get_transaction_and_categories_not_found():
    pass

@pytest.mark.skip(reason="Test not yet implemented")
def test_delete_transaction_success():
    pass

@pytest.mark.skip(reason="Test not yet implemented")
def test_delete_transaction_not_found():
    pass

@pytest.mark.skip(reason="Test not yet implemented")
def test_delete_transaction_user_boundary():
    pass

@pytest.mark.skip(reason="Test not yet implemented")
def test_get_dashboard_invalid_start_date():
    pass

@pytest.mark.skip(reason="Test not yet implemented")
def test_get_dashboard_invalid_end_date():
    pass

@pytest.mark.skip(reason="Test not yet implemented")
def test_get_dashboard_success():
    pass

# Add tests for dashboard sorting and filtering
# Add validate_transaction_form regression test
# Add test for get_transaction_dashboard_data with empty list
# Test calculation totals