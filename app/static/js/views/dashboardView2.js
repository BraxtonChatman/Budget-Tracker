import { initTransactions } from "../controllers/transactionsController.js";
import { logout } from "../api/auth.js";

export function showDashboardView(user, onLogout) {
    const app = document.getElementById("app");

    app.innerHTML = `
    <div class="container py-4">

        <!-- HEADER -->
        <header class="d-flex justify-content-between align-items-center mb-4">
            <h1 class="h3 m-0">Budget Tracker</h1>

            <div class="d-flex align-items-center gap-3">
                <span class="text-muted">Logged in as: ${user.username}</span>
                <button id="logoutBtn" class="btn btn-outline-danger btn-sm">Logout</button>
            </div>
        </header>

        <!-- MAIN -->
        <main class="d-flex flex-column gap-4">

            <!-- SUMMARY -->
            <section>
                <h2 class="h5 mb-3">Summary</h2>

                <div class="row g-3">
                    <div class="col-md-4">
                        <div class="card p-3">
                            <div class="text-muted">Income</div>
                            <div id="total-income" class="fs-4"></div>
                        </div>
                    </div>

                    <div class="col-md-4">
                        <div class="card p-3">
                            <div class="text-muted">Expense</div>
                            <div id="total-expense" class="fs-4"></div>
                        </div>
                    </div>

                    <div class="col-md-4">
                        <div class="card p-3">
                            <div class="text-muted">Net</div>
                            <div id="net-total" class="fs-4"></div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- ADD TRANSACTION -->
            <section>
                <h2 class="h5 mb-3">Add Transaction</h2>

                <div class="card p-3">
                    <form id="add-transaction-form" class="row g-3">
                        <div class="col-md-2">
                            <input id="add-date" type="date" class="form-control" required>
                        </div>

                        <div class="col-md-2">
                            <select id="add-category" class="form-select" required></select>
                        </div>

                        <div class="col-md-3">
                            <input id="add-description" class="form-control" placeholder="Description">
                        </div>

                        <div class="col-md-2">
                            <input id="add-amount" type="number" step="0.01" class="form-control" placeholder="Amount" required>
                        </div>

                        <div class="col-md-2">
                            <select id="add-type" class="form-select" required>
                                <option value="Expense">Expense</option>
                                <option value="Income">Income</option>
                            </select>
                        </div>

                        <div class="col-md-1 d-grid">
                            <button class="btn btn-success">Add</button>
                        </div>
                    </form>
                </div>
            </section>

            <!-- TRANSACTIONS -->
            <section>
                <h2 class="h5 mb-3">Transactions</h2>

                <div class="card p-3">

                    <!--FILTERS -->
                    <form id="filter-form" class="row g-2 mb-3">
                        <div class="col-md-3">
                            <select id="filter-category" class="form-select"></select>
                        </div>

                        <div class="col-md-2">
                            <input id="filter-start-date" type="date" class="form-control">
                        </div>

                        <div class="col-md-2">
                            <input id="filter-end-date" type="date" class="form-control">
                        </div>

                        <div class="col-md-2">
                            <select id="filter-sort-by" class="form-select">
                                <option value="date">Date</option>
                                <option value="amount">Amount</option>
                                <option value="type">Type</option>
                            </select>
                        </div>

                        <div class="col-md-3 gap-2">
                            <button class="btn btn-primary">Apply</button>
                            <button type="button" id="filter-reset" class="btn btn-outline-secondary">Reset</button>
                        </div>
                    </form>

                    <!-- TABLE -->
                    <div class="table-responsive">
                        <table class="table table-hover align-middle">
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
                </div>
            </section>
        
        </main>
    </div>

    <!-- MODAL -->
    <div class="modal fade" id="edit-modal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Edit Transaction</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>

                <div class="modal-body d-flex flex-column gap-2">
                    <input type="date" id="edit-date" class="form-control">
                    <select id="edit-category" class="form-select"></select>
                    <input type="text" id="edit-description" class="form-control">
                    <input type="number" id="edit-amount" class="form-control">
                    <select id="edit-type" class="form-select">
                        <option value="Expense">Expense</option>
                        <option value="Income">Income</option>
                    </select>

                    <input type="hidden" id="edit-id">
                </div>

                <div class="modal-footer">
                    <button id="save-edit" class="btn btn-success">Save</button>
                    <button class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                </div>
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