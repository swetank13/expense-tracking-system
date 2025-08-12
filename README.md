# Expense Management System

This project is an expense management system that consists of a Streamlit frontend application and a FastAPI backend server.


## Project Structure

- **frontend/**: Contains the Streamlit application code.
- **backend/**: Contains the FastAPI backend server code.
- **resources/**: Contains screenshots and other documents.
- **tests/**: Contains the test cases for both frontend and backend.
- **requirements.txt**: Lists the required Python packages.
- **README.md**: Provides an overview and instructions for the project.


## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/expense-management-system.git
   cd expense-management-system
   ```
1. **Initial Setup for Project**:
   ```commandline
   Use Pycharm, Create python .venv at your project level. At bottom right IDE should display below
   Python 3.10(expense-tracking-system)
   ```
1. **Install dependencies:**:   
   ```commandline
    pip install -r requirements.txt
   ```
1. **Run the FastAPI server:**:   
   ```commandline
    uvicorn server.server:app --reload

   Run the command at project level <expense-tracking-system> uvicorn backend.server:app –reload
   
   Then you can use request and test the connection from postman (Ex: get method: http://127.0.0.1:8000/expenses/2024-08-15)

   Please refer postman collection in resources folder.
   ```
1. **Run the Streamlit app:**:   
   ```commandline
    streamlit run frontend/app.py

   At project level <expense-tracking-system> we need to run the command `streamlit run frontend/app.py`
   ```


