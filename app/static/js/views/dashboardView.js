import { logout } from "../api/auth.js";
import { initTransactions } from "../controllers/transactionsController.js";

export function showDashboardView(user, onLogout) {
    const app = document.getElementById("app");

    app.innerHTML = `
        <h1>Budget Tracker</h1>
        <div class="nav-bar">
            <span>Logged in as: ${user.username}</span>
            <button id="logoutBtn" class="form-button add-button">Logout</button>
        </div>

        <div id="message-container"></div>

        <!-- Totals Headers -->
        <h2>Totals</h2>
        <p>
            Income: <strong id="total-income"></strong> |
            Expense: <strong id="total-expense"></strong> |
            Net Total: <strong id="net-total"></strong>
        </p>

        <!-- Add Transaction -->
        <h2>Add Transaction</h2>
        <div class="form-container">
            <form id="add-transaction-form">    
                <input id="add-date" type="date" name="date" class="form-input" required>
                <select id="add-category" name="category" class="form-input" required></select>
                <input id="add-description" type="text" name="description" class="form-input" placeholder="Description">
                <input id="add-amount" type="number" step="0.01" name="amount" class="form-input" placeholder="Amount" required>
                <select id="add-type" name="type" class="form-input" required>
                    <option value="Expense">Expense</option>
                    <option value="Income">Income</option>
                </select>
                <button type="submit" class="form-button add-button">Add Transaction</button>
            </form>
        </div>

        <h2>Transactions</h2>
        <!-- Transaction Filtering & Sorting -->
        <form id="filter-form">
            <label for="category">Category:</label>
            <select name="category" id="filter-category">
            </select>

            <label for="start_date">From:</label>
            <input type="date" id="filter-start-date" name="start_date" value="">

            <label for="end_date">To:</label>
            <input type="date" id="filter-end-date" name="end_date" value="">

            <label for="sort_by">Sort by:</label>
            <select name="sort_by" id="filter-sort-by">
                <option value="date">Date</option>
                <option value="amount">Amount</option>
                <option value="type">Type</option>
            </select>

            <button type="submit">Apply</button>
            <button type="button" id="filter-reset">Reset</button>
        </form>
        <br>

        <!-- Transaction Table -->
        <div class="transaction-container">
            <table class="transaction-table">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Category</th>
                        <th>Description</th>
                        <th>Income</th>
                        <th>Expense</th>
                        <th>Actions</th>
                    </tr>
                </thead>

                <tbody></tbody>
            </table>
        </div>

        <!-- Edit modal -->
        <div id="edit-modal" class="modal hidden">
            <div class="modal-content">
                <h2>Edit Transactions</h2>
                <input type="date" id="edit-date" class="form-input">
                <select id="edit-category" class="form-input"></select>
                <input type="text" id="edit-description" class="form-input">
                <input type="number" id="edit-amount" step="0.01" class="form-input">
                <select id="edit-type" class="form-input">
                    <option value="Expense">Expense</option>
                    <option value="Income">Income</option>
                </select>

                <input type="hidden" id="edit-id">
                <!-- <div style="margin-top: 10px;"> -->
                <div class="modal-buttons">
                    <button id="save-edit" class="form-button add-button">Save</button>
                    <button id="cancel-edit" class="form-button delete-button">Cancel</button>
                </div>
            </div>
        </div>
    `;

    document.getElementById("logoutBtn").onclick = async () => {
        await logout();
        onLogout();
    };

    requestAnimationFrame(() => {
        initTransactions();
    });
    
}