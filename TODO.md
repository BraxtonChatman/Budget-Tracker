# Budget Tracker Development Roadmap
# Current Priorities
## Testing
- [ ] Unit tests for models
- [ ] Unit tests for services
- [ ] Integration test: add → edit → delete → verify totals
- [ ] Configure pytest test environment

## Database
- [ ] Integrate Flask-Migrate
- [ ] Add created_at timestamp to Transaction
- [ ] Add updated_at timestamp to Transaction
- [ ] Add cascade delete (Category → Transactions)

## Security
- [ ] Add CSRF protection (Flask-WTF or manual token)
- [ ] Improve password validation rules

---

# UI / UX Improvements

- [ ] Create base `layout.html` template
- [ ] Improve edit page layout
- [ ] Improve spacing and typography
- [ ] Handle long descriptions with ellipsis or tooltip
- [ ] Make CSS layout fully responsive

---

# Feature Enhancements

## Search & Filtering
- [ ] Keyword search on transaction descriptions
- [ ] Persist filters after editing transactions

## Analytics
- [ ] Monthly totals view
- [ ] Running balance calculation
- [ ] Spending charts (Chart.js)

## Export
- [ ] CSV export endpoint
- [ ] Export filtered transactions

---

# API Layer

- [ ] Add REST API for transactions
- [ ] GET /transactions
- [ ] POST /transactions
- [ ] PATCH /transactions/<id>
- [ ] DELETE /transactions/<id>

---

# DevOps / Production

- [ ] Logging for errors and debugging
- [ ] Production configuration improvements
- [ ] Environment variable management
- [ ] Dockerize application (optional)

---

# Learning Topics

- Flask request lifecycle
- Jinja2 templating
- SQLAlchemy relationships
- Input validation
- Authentication with Flask-Login
- Filtering, sorting, and aggregation
- Application factory architecture