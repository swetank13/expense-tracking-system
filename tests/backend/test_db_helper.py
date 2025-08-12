import pytest
from unittest.mock import patch, MagicMock
from backend.db_helper import fetch_expenses_for_date, fetch_expense_summary


@patch('backend.db_helper.mysql.connector.connect')
def test_fetch_expenses_for_date_aug_15(mock_connect):
    """Test fetching expenses for a specific date with known data."""
    # Setup mock
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [{'amount': 10.0, 'category': 'Shopping', 'notes': 'Bought potatoes'}]
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_connection

    # Call the function
    expenses = fetch_expenses_for_date("2024-08-15")

    # Assertions
    mock_cursor.execute.assert_called_once_with("SELECT * FROM expenses WHERE expense_date = %s", ("2024-08-15",))
    assert len(expenses) == 1
    assert expenses[0]['amount'] == 10.0
    assert expenses[0]['category'] == "Shopping"
    assert expenses[0]["notes"] == "Bought potatoes"

@patch('backend.db_helper.mysql.connector.connect')
def test_fetch_expenses_for_date_invalid_date(mock_connect):
    """Test fetching expenses for a date with no records."""
    # Setup mock
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = []
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_connection

    # Call the function
    expenses = fetch_expenses_for_date("9999-08-15")

    # Assertions
    mock_cursor.execute.assert_called_once_with("SELECT * FROM expenses WHERE expense_date = %s", ("9999-08-15",))
    assert len(expenses) == 0

@patch('backend.db_helper.mysql.connector.connect')
def test_fetch_expense_summary_invalid_range(mock_connect):
    """Test fetching expense summary for a date range with no records."""
    # Setup mock
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = []
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_connection

    # Call the function
    summary = fetch_expense_summary("2099-01-01", "2099-12-31")

    # Assertions
    assert len(summary) == 0

# Mocking the mysql.connector.connect method
@patch('backend.db_helper.mysql.connector.connect')
def test_fetch_expenses_for_date_basic_functionality(mock_connect):
    """Test basic functionality of fetching expenses for a given date."""
    # Setup mock
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [{'amount': 100, 'category': 'Food', 'notes': 'Lunch'}]
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_connection

    # Call the function
    expenses = fetch_expenses_for_date("2024-09-30")

    # Assertions
    mock_cursor.execute.assert_called_once_with("SELECT * FROM expenses WHERE expense_date = %s", ("2024-09-30",))
    assert expenses == [{'amount': 100, 'category': 'Food', 'notes': 'Lunch'}]

@patch('backend.db_helper.mysql.connector.connect')
def test_fetch_expenses_for_date_no_results(mock_connect):
    """Test fetching expenses for a date with no records."""
    # Setup mock
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = []
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_connection

    # Call the function
    expenses = fetch_expenses_for_date("2024-09-30")

    # Assertions
    assert expenses == []

@patch('backend.db_helper.mysql.connector.connect')
def test_fetch_expenses_for_invalid_date(mock_connect):
    """Test fetching expenses with an invalid date format."""

    # Call the function with invalid date
    summery = fetch_expenses_for_date("2099-31-31")

    # Assertions
    assert len(summery) == 0

@patch('backend.db_helper.mysql.connector.connect')
def test_fetch_expenses_for_date_sql_error(mock_connect):
    """Test handling of SQL errors during fetching."""
    # Setup mock
    mock_cursor = MagicMock()
    mock_cursor.execute.side_effect = Exception("SQL Error")
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_connection

    # Call the function and expect an exception
    with pytest.raises(Exception, match="SQL Error"):
        fetch_expenses_for_date("2024-09-30")