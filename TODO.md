# Budget Tracker
- [x] Flask app running
- [x] SQLite database
- [x] SQLAlchemy models
- [x] Add / Edit / Delete transactions
- [x] Category filtering
- [x] Basic total calculation
- [x] Initial seed categories

---

## Now (Current Focus)
- [ ] Date range filter
- [ ] Date range sorting
- [ ] Add basic input validation (empty fields, invalid amounts)
- [ ] Replace deprecated `Query.get()` with `db.session.get()`
- [ ] Handle missing transaction errors consistently
- [ ] Add basic flash messages (success / error feedback)

---

## Next (Near-Term Improvements)
- [ ] Add monthly total view
- [ ] Add income vs expense distinction
- [ ] Add running balance calculation
- [ ] Add CSV export

---

## Data Modeling Improvements

- [ ] Add proper `created_at` timestamp column
- [ ] Add cascade delete from Category → Transactions
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