import os.path

import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger

logger = setup_logger('db_helper')

@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="abc@123",
        database="expense_manager"
    )

    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    cursor.close()
    connection.close()


def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    try:
        with get_db_cursor(commit=False) as cursor:
            cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
            expenses_for_date = cursor.fetchall()
            return expenses_for_date
    except Exception as e:
        logger.error(f"Error in fetch_expenses_for_date: {e}")
        return []

def delete_expenses_for_date(expense_date):
    logger.info(f"delete_expenses_for_date called with {expense_date}")
    try:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))
    except Exception as e:
        logger.error(f"Error in delete_expenses_for_date: {e}")
        return []

def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expense called with date: {expense_date}, amount: {amount}, category: {category}, notes: {notes}")
    try:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(
                "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
                (expense_date, amount, category, notes)
            )
    except Exception as e:
        logger.error(f"Error in insert_expense: {e}")
        return []

def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary called with start: {start_date} end: {end_date}")
    try:
        with get_db_cursor(commit=False) as cursor:
            cursor.execute(
                '''SELECT category, SUM(amount) as total 
                   FROM expenses WHERE expense_date
                   BETWEEN %s and %s  
                   GROUP BY category;''',
                (start_date, end_date)
            )
            data = cursor.fetchall()
            return data
    except Exception as e:
        logger.error(f"Error in fetch_expense_summary: {e}")
        return []

def get_total_expense_by_category(start_date, end_date):
    logger.info(f"get_total_expense_by_category from {start_date} to {end_date}")
    try:
        with get_db_cursor(commit=False) as cursor:
            cursor.execute(
                '''
                SELECT category, SUM(amount) as total
                FROM expenses
                WHERE expense_date BETWEEN %s AND %s
                GROUP BY category
                ORDER BY total DESC
                ''',
                (start_date, end_date)
            )
            return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error in get_total_by_category: {e}")
        return []


def get_monthly_summary(year):
    logger.info(f"get_monthly_summary called for year: {year}")
    try:
        with get_db_cursor() as cursor:
            cursor.execute(
                '''
                SELECT 
                    MONTH(expense_date) AS month,
                    SUM(amount) as total
                FROM expenses
                WHERE YEAR(expense_date) = %s
                GROUP BY MONTH(expense_date)
                ORDER BY MONTH(expense_date)
                ''',
                (year,)
            )
            return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error in get_monthly_summary: {e}")
        return []


def get_recent_expenses(limit=10):
    logger.info(f"get_recent_expenses called with limit: {limit}")
    try:
        with get_db_cursor() as cursor:
            cursor.execute(
                "SELECT * FROM expenses ORDER BY expense_date DESC, id DESC LIMIT %s",
                (limit,)
            )
            return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error fetching recent expenses: {e}")
        return []


if __name__ == "__main__":
    expenses = fetch_expenses_for_date("2024-09-30")
    print(expenses)
    # delete_expenses_for_date("2024-08-25")
    summary = fetch_expense_summary("2024-08-01", "2024-08-05")
    for record in summary:
        print(record)
    total_expense = get_total_expense_by_category("2024-08-01", "2024-08-05")
    print(total_expense)
    monthly_expense = get_monthly_summary("2024")
    print(monthly_expense)
    latest_expense = get_recent_expenses()
    print(latest_expense)
