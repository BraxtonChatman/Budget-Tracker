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
- [ ] Update TODO and README
- [ ] Testing
    * Unit tests for models and routes
    * Integration tests: add → edit → delete → verify totals
- [ ] Database Migrations
    * Integrate Flask-Migrate for schema evolution
- [ ] Enhance UI/UX
    * Make forms and transaction lists more visually appealing
    * ~~Add confirmation modals for delete actions~~
    * Use CSS Grid/Flexbox for better responsive layout
    * Improve edit page layout to match index page
    * Handle long descriptions with ellipsis or tooltip
- [ ] Filtering / Searching
    * ~~Keep category filter after editing a transaction~~
    * ~~Sort transactions descending by date~~
    * ~~Add date range filtering~~
    * Add keyword search on descriptions
    * ~~Combine category + date filters~~
    * Keep sort by and date filters after editing a transaction
- [ ] Better project structure
    * ~~Move category seeding into `seed.py~~`
    * Create `layout.html` base template for common HTML
    * Make CSS widths flexible instead of fixed 150px
    * ~~Split Flask routes into `routes.py` or a blueprint~~
    * Organize templates and static files clearly
- [X] Add basic flash messages (success / error feedback)
- [X] Show totals per category, not just overall total
- [X] Add income vs expense distinction
    * ~~Optional: use SQLAlchemy Enum for `type` field~~
- [X] Polish date and amount handling
    * ~~Ensure proper validation: prevent negative amounts, invalid dates, empty descriptions~~
    * ~~Handle empty states gracefully (no transactions)~~
    * ~~Ensure `edit.html` date input uses `transaction.date.strftime('%Y-%m-%d')`~~
    * ~~Display amounts as currency (`$12.34`) in templates~~

---

## Next (Near-Term Improvements)
- [ ] Add monthly total view
    * Group transactions by month and sum income/expense
    * Display in a separate table or section on index page
- [ ] Add running balance calculation
    * Show cumulative balance per transaction
- [ ] Add CSV export
    * Build `/export` route to download CSV of transactions
    * Optionally include filters in export
- [X] Authentication / Users
    * ~~Add multiple users with login/logout~~
    * ~~Transactions tied to a specific user~~
- [ ] Analytics / Charts
    * Use Chart.js or Plotly to show spending trends over time
- [ ] API Layer
    * Add a REST API for transactions: GET, POST, DELETE, PATCH
- [X] Deployment
    * ~~Deploy to Heroku / Render / Fly.io~~
    * ~~Include README with setup and features~~

---

## Data Modeling Improvements
- [ ] Add proper `created_at` and `updated_at` timestamp columns
- [ ] Add cascade delete from Category → Transactions (`ondelete='CASCADE'`)
- [ ] Refactor database initialization for cleaner structure
- [ ] Move category seeding into a separate function

---

## Production Thinking (Early Awareness)
- [ ] Add CSRF protection (Flask-WTF or manual token)
- [ ] Separate config into development vs production
- [ ] Learn app factory pattern
- [ ] Add basic logging for errors and debugging

---

## Bugs / Cleanup
- [ ] Improve UI styling (consistent spacing & layout)
- [ ] Format currency to 2 decimal places with `$`
- [ ] Add empty-state message when no transactions exist
- [ ] Fix transaction display for long descriptions (overflow/ellipsis)

---

## Concepts Learned
- Flask request lifecycle
- Jinja2 templating & loops
- SQLAlchemy relationships & foreign keys
- HTTP methods, POST vs GET
- Database migrations & versioning
- Data validation best practices
- Flash messages & user feedback
- Filtering, sorting, and aggregation
- Basic responsive CSS layout