# Budget-Tracker

**Budget-Tracker** is a full-stack web application that helps users gain control of their personal finances by tracking income, expenses, and net balances in a simple, intuitive interface. Built with **Flask** and **SQLAlchemy**, this project demonstrates practical web development skills, database modeling, and maintainable Python application design.

## Demo

Deployed on Render: [https://budget-tracker-fko1.onrender.com/](https://budget-tracker-fko1.onrender.com/)

![Screenshot](./images/demo-main.png)

## Features

- Add, edit, and delete transactions with a clear income/expense distinction.
- Categorize transactions and filter by category.
- Calculate totals for income, expenses, and net balance dynamically.
- Flash messages for success/error feedback.
- Responsive interface using HTML/CSS templates.
- Validates user input (dates, amounts, transaction type).

## Tech Stack

- **Backend:** Flask  
- **Database:** SQLite with SQLAlchemy ORM  
- **Frontend:** Jinja2 templates, HTML/CSS  
- **Languages:** Python 3.x  
- **Libraries:** Flask, SQLAlchemy  

## Installation

1. Clone the repository:
   ~~~
   git clone https://github.com/your-username/budget-tracker.git  
   cd budget-tracker
   ~~~

2. Create and activate a virtual environment:


   **Linux/Mac:** 
   ~~~ 
   python -m venv venv  
   source venv/bin/activate  
   ~~~

   **Windows:**  
   ~~~
   python -m venv venv  
   venv\Scripts\activate  
   ~~~

3. Install dependencies:
   ~~~
   pip install -r requirements.txt
   ~~~

4. Run the application:
   ~~~
   python app.py
   ~~~

5. Open your browser and go to:  
   ~~~
   http://127.0.0.1:5000/
   ~~~

> Note: The app uses a local SQLite database `budget.db`. Initial categories are automatically seeded if none exist.

## Usage

- **Add a transaction:** Enter date, category, description, amount, and type (Income or Expense) and click "Add Transaction".  
- **Edit a transaction:** Click "Edit" next to a transaction, update fields, and submit.  
- **Delete a transaction:** Click "Delete" and confirm.  
- **Filter transactions:** Use the category dropdown to view specific categories.  
- **View totals:** Income, expenses, and net balance are displayed at the top.

## Project Structure

- `app.py` – Main Flask application  
- `models.py` – SQLAlchemy models (Transaction, Category)  
- `seed.py` – Development script for generating sample transactions (optional)  
- `templates/` – HTML templates (`index.html`, `edit.html`)  
- `static/` – CSS and static files (`style.css`)  
- `README.md` – Project documentation  
- `TODO.md` – Notes on current and future improvements  

## Technical Highlights

- Proper use of **Flask routes** and **Jinja2 templating**.  
- **ORM relationships** using SQLAlchemy for categories and transactions.  
- Input validation for dates, amounts, and transaction types.  
- Flash messages provide user feedback on form submissions.  
- **CSS Flexbox** for responsive layout and styled transaction table.  
- Designed with scalability in mind, including clear project structure and separation of concerns.

## Future Improvements

- Filter transactions by date range and keywords.  
- Display totals per category and monthly summaries.  
- Multi-user support with authentication.  
- Export transactions to CSV.  
- Add charts and analytics with Chart.js or Plotly.  
- Database migrations with Flask-Migrate.  
- Unit and integration tests.  
- Deployment to cloud platforms (Heroku, Render, Fly.io).  
- Refactor routes into blueprints and add layout templates for DRY HTML.

## Decisions

- Using `psycopg2-binary` for PostgreSQL integration for now to maintain deployment momentum.
- Will consider switching to `psycopg2` (non-binary) if scaling requirements or stability needs arise.

