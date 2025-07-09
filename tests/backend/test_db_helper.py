from backend import db_helper


def test_fetch_expenses_for_date_aug_15():
    expenses = db_helper.fetch_expenses_for_date("2024-08-15")

    assert len(expenses) == 1
    assert expenses[0]['amount'] == 10.0
    assert expenses[0]['category'] == "Shopping"
    assert expenses[0]["notes"] == "Bought potatoes"


def test_fetch_expenses_for_date_invalid_date():
    expenses = db_helper.fetch_expenses_for_date("9999-08-15")

    assert len(expenses) == 0


def test_fetch_expense_summary_invalid_range():
    summary = db_helper.fetch_expense_summary("2099-01-01", "2099-12-31")
    assert len(summary) == 0

# get_total_expense_by_category(start_date, end_date)
#     [{'month': 8, 'total': 5222.0}, {'month': 9, 'total': 4790.0}]
#      {'category': 'Shopping', 'total': 670.0}, {'category': 'Entertainment', 'total': 225.0},
#      {'category': 'Other', 'total': 90.0}]
# get_monthly_summary(year),
# get_recent_expenses(limit=10)

def test_get_total_expense_by_category_valid():
    total_expense_by_category = db_helper.get_total_expense_by_category("2024-08-01", "2024-08-05")

    assert total_expense_by_category[0]['category'] == "Rent"
    assert total_expense_by_category[0]['total'] == 2777.0
    assert len(total_expense_by_category) == 5


def test_get_total_expense_by_category_invalid():
    total_expense_by_category = db_helper.get_total_expense_by_category("2099-01-01", "2099-12-31")
    assert len(total_expense_by_category) == 0


def test_get_monthly_summary_valid():
    get_monthly_summary = db_helper.get_monthly_summary("2024")
    assert get_monthly_summary[0]['month'] == 8
    assert get_monthly_summary[0]['total'] == 5222.0
    assert len(get_monthly_summary) == 2


def test_get_monthly_summary_invalid():
    get_monthly_summary = db_helper.get_monthly_summary("2028")
    assert len(get_monthly_summary) == 0


def test_get_recent_expenses_valid():
    get_recent_expenses = db_helper.get_recent_expenses()
    assert get_recent_expenses[0]['id'] == 67
    assert get_recent_expenses[0]['amount'] == 100.0
    assert get_recent_expenses[0]['category'] == "Food"
    assert get_recent_expenses[0]['notes'] == "Salad"


def test_get_recent_expenses_count():
    get_recent_expenses = db_helper.get_recent_expenses()
    assert len(get_recent_expenses) == 10