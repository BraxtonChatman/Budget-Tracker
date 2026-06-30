import {
    getTransaction,
    getTransactions,
    createTransaction,
    updateTransaction,
    deleteTransaction
} from "../api/transactions.js";

let cahcedCategories = [];
let editModalInstance = null;

export async function initTransactions() {
    cahcedCategories = [];
    editModalInstance = null;

    const dom = cacheDOM();
    wireEvents(dom);
    await loadCategories(dom);
    await loadTransactions(dom);
}

function cacheDOM() {
    return {
        totalIncome: document.getElementById("total-income"),
        totalExpense: document.getElementById("total-expense"),
        netTotal: document.getElementById("net-total"),

        filterForm: document.getElementById("filter-form"),
        filterCategory: document.getElementById("filter-category"),
        filterStartDate: document.getElementById("filter-start-date"),
        filterEndDate: document.getElementById("filter-end-date"),
        filterSortBy: document.getElementById("filter-sort-by"),
        filterResetBtn: document.getElementById("filter-reset"),

        modal: document.getElementById("edit-modal"),

        editId: document.getElementById("edit-id"),
        editDate: document.getElementById("edit-date"),
        editCategory: document.getElementById("edit-category"),
        editDescription: document.getElementById("edit-description"),
        editAmount: document.getElementById("edit-amount"),
        editType: document.getElementById("edit-type"),

        addForm: document.getElementById("add-transaction-form"),
        addDate: document.getElementById("add-date"),
        addCategory: document.getElementById("add-category"),
        addDescription: document.getElementById("add-description"),
        addAmount: document.getElementById("add-amount"),
        addType: document.getElementById("add-type"),

        tbody: document.querySelector("tbody"),

        cancelEditBtn: document.getElementById("cancel-edit"),
        saveEditBtn: document.getElementById("save-edit")
    };
}

function wireEvents(dom) {
    dom.tbody.addEventListener("click", (e) => handleTableClick(e, dom));
    dom.addForm.addEventListener("submit", (e) => handleAdd(e, dom));

    // dom.cancelEditBtn.onclick = () => {
    //     closeModal();
    // };

    dom.modal.addEventListener("hidden.bs.modal", () => {
        dom.editId.value = "";
        dom.editDate.value = "";
        dom.editCategory.value = "";
        dom.editDescription.value = "";
        dom.editAmount.value = "";
        dom.editType.value = "Expense";
    })

    dom.saveEditBtn.onclick = () => {
        handleSave(dom);
    };

    dom.filterForm.addEventListener("submit", (e) => {
        e.preventDefault();
        loadTransactions(dom);
    })

    dom.filterResetBtn.onclick = async () => {
        dom.filterCategory.value = "";
        dom.filterStartDate.value = "";
        dom.filterEndDate.value = "";
        dom.filterSortBy.value = "date";

        await loadTransactions(dom);
    }
}

async function loadTransactions(dom) {
    try {
        const filters = {
            category: dom.filterCategory?.value || "",
            start_date: dom.filterStartDate?.value || "",
            end_date: dom.filterEndDate?.value || "",
            sort_by: dom.filterSortBy?.value || "date"
        };

        const data = await getTransactions(filters);

        renderTransactions(dom, data.transactions);
        renderTotals(dom, data.totals);

    } catch (err) {
        alert(err.message);
    }
}

async function loadCategories(dom) {
    const data = await getTransactions();
    cahcedCategories = data.categories;

    renderCategories(dom, cahcedCategories);
}

async function handleAdd(event, dom) {
    event.preventDefault();

    const payload = {
        date: dom.addDate.value,
        category: dom.addCategory.value,
        description: dom.addDescription.value,
        amount: dom.addAmount.value,
        type: dom.addType.value
    };

    try {
        await createTransaction(payload);
        dom.addForm.reset();
        await loadTransactions(dom);

    } catch (err) {
        alert(err.message);
    }

}

async function handleTableClick(event, dom) {
    const deleteBtn = event.target.closest(".js-delete-transaction");
    if(deleteBtn) return handleDelete(deleteBtn.dataset.transactionId, dom);

    const editBtn = event.target.closest(".js-edit-transaction");
    if(editBtn) return handleEdit(editBtn.dataset.transactionId, dom);
}

async function handleDelete(txId, dom) {
    const confirmed = confirm("Delete this transaction?");
    if (!confirmed) return;

    try {
        await deleteTransaction(txId);
        await loadTransactions(dom);

    } catch (err) {
        alert(err.message);
    }
}

async function handleEdit(txId, dom) {
    try {
        const data = await getTransaction(txId);
        const tx = data.transaction;

        dom.editId.value = tx.id;
        dom.editDate.value = tx.date;
        dom.editCategory.value = tx.category_id;
        dom.editDescription.value = tx.description;
        dom.editAmount.value = tx.amount;
        dom.editType.value = tx.type;

        if (!editModalInstance) {
            editModalInstance = new bootstrap.Modal(dom.modal);
        }
        editModalInstance.show();

    } catch (err) {
        alert(err.message);
    }
}

async function handleSave(dom) {
    const txId = dom.editId.value;
    if(!txId) return alert("Missing transaction id");

    const payload = {
        date: dom.editDate.value,
        category: dom.editCategory.value,
        description: dom.editDescription.value,
        amount: parseFloat(dom.editAmount.value),
        type: dom.editType.value
    };

    try {
        await updateTransaction(txId, payload);
        closeModal();
        await loadTransactions(dom);

    } catch(err) {
        alert(err.message);
    }
}

function closeModal() {
    if (editModalInstance) {
        editModalInstance.hide();
    }
}

function renderTransactions(dom, transactions) {
    dom.tbody.innerHTML = "";

    transactions.forEach(t => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${t.date}</td>
            <td>${t.category_name}</td>
            <td>${t.description}</td>
            <td>${t.type === "Income" ? formatCurrency(t.amount) : ""}</td>
            <td>${t.type === "Expense" ? formatCurrency(t.amount) : ""}</td>
            <td>
                <button class="js-edit-transaction" data-transaction-id="${t.id}">Edit</button>
                <button class="js-delete-transaction" data-transaction-id="${t.id}">Delete</button>
            </td>
        `;

        dom.tbody.appendChild(row);
    });
}

function renderTotals(dom, totals) {
    dom.totalIncome.textContent = formatCurrency(totals.income);
    dom.totalExpense.textContent = formatCurrency(totals.expense);
    dom.netTotal.textContent = formatCurrency(totals.net);
}

function renderCategories(dom, categories) {
    populateCategorySelect(dom.addCategory, categories);
    populateCategorySelect(dom.editCategory, categories);
    populateCategorySelect(dom.filterCategory, categories, true);

    dom.filterCategory.value = "";
}

function populateCategorySelect(select, categories, includeAll = false) {
    select.innerHTML = "";

    if (includeAll) {
        select.appendChild(new Option("All", ""));
    }

    categories.forEach(category => {
        select.appendChild(new Option(category.name, category.id));
    });
}

function formatCurrency(value) {
    return `$${Number(value).toFixed(2)}`;
}

