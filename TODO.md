# Budget Tracker
- [X] Flask app running
- [X] SQLite database
- [X] SQLAlchemy models
- [X] Add / Edit / Delete transactions
- [X] Category filtering
- [X] Basic total calculation
- [X] Initial seed categories

---

## Now (Current Focus)
- [X] Polish date and amount handling
    * ~~Ensure proper validation: prevent negative amounts, invalid dates, empty descriptions~~
    * ~~Handle empty states gracefully (no transactions)~~
- [ ] Add income vs expense distinction
- [ ] Enhance UI/UX
    * Make forms and transaction lists more visually appealing
    * Add confirmation modals for delete actions
    * Use CSS Grid/Flexbox for better responsive layout
- [ ] Show totals per category, not just overall total
- [ ] Filtering / Searching
    * Date range filtering
    * Combine category + date filters
- [ ] Replace deprecated `Query.get()` with `db.session.get()`
- [ ] Add basic flash messages (success / error feedback)
- [ ] Better project structure
    * Split Flask routes into routes.py or a blueprint
    * Organize templates and static files clearly
---

## Next (Near-Term Improvements)
- [ ] Add monthly total view
- [ ] Add running balance calculation
- [ ] Add CSV export
- [ ] Authentication / Users
    * Add multiple users with login/logout
    * Transactions tied to a specific user
- [ ] Analytics / Charts
    * Use Chart.js or Plotly (matplotlib?) to show spending trends over time
- [ ] API Layer
    * Add a REST API for transactions: GET, POST, DELETE, PATCH
- [ ] Database Migrations
    * Integrate Flask-Migrate for proper schema evolution
- [ ] Testing
    * Unit tests for routes and models
    * Integration tests for the full workflow
- [ ] Deployment
    * Deploy to Heroku / Render / Fly.io

---

## Data Modeling Improvements

- [ ] Add proper `created_at` timestamp column
- [ ] Add cascade delete from Category → Transactions (ondelete='CASCADE')
- [ ] Move category seeding into a separate function
- [ ] Refactor database initialization for cleaner structure

---

## Production Thinking (Early Awareness)

- [ ] Add CSRF protection (Flask-WTF or manual token)
- [ ] Separate config into development vs production
- [ ] Understand app factory pattern
- [ ] Add basic logging

---

## Bugs / Cleanup
- [ ] Improve UI styling (consistent spacing & layout)
- [ ] Format currency to 2 decimal places
- [ ] Add empty-state message when no transactions exist
- [ ] Fix transaction display for long descriptions (overflow/ellipsis)

---

## Concepts Learned
- Flask request lifecycle
- Jinja2 templating & loops
- SQLAlchemy relationships & foreign keys
- HTTP methods, POST vs GET
- Database migrations & versioning