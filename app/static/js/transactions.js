
document.addEventListener("DOMContentLoaded", async () => {
    await refreshTransactions();
});


document.addEventListener("DOMContentLoaded", () => {
    const tbody = document.querySelector("tbody");

    tbody.addEventListener("click", async (event) => {
        const button = event.target.closest(".js-delete-transaction");

        if (!button) {
            return;
        }

        const txId = button.dataset.transactionId;

        const confirmed = confirm(
            "Are you sure you want to delete this transaction?"
        );

        if (!confirmed) {
            return;
        }

        try {
            const response = await fetch(`/api/transactions/${txId}`, {
                method: "DELETE"
            });

            const data = await response.json();

            if (!response.ok) {
                alert(data.errors?.join(", ") || "Delete failed");
                return;
            }

            await refreshTransactions();
        }
        catch (error) {
            console.error(error);
            alert("An unexpected error occurred.");
        }
    });
});

function renderTransactions(transactions) {
    const tbody = document.querySelector("tbody");
    tbody.innerHTML = "";

    transactions.forEach(t => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${t.date}</td>
            <td>${t.category_name}</td>
            <td>${t.description}</td>
            <td>${t.type === "Income" ? formatCurrency(t.amount) : ""}</td>
            <td>${t.type === "Expense" ? formatCurrency(t.amount) : ""}</td>
            <td>
                <a href="/edit/${t.id}" class="form-button edit-button">Edit</a>
                <button class="form-button delete-button js-delete-transaction" data-transaction-id="${t.id}">
                    Delete
                </button>
            </td>
        `;

        tbody.appendChild(row);
    });
}

function renderTotals(totals) {
    document.getElementById("total-income").textContent = formatCurrency(totals.income);
    document.getElementById("total-expense").textContent = formatCurrency(totals.expense);
    document.getElementById("net-total").textContent = formatCurrency(totals.net);
}

async function refreshTransactions() {
    const response = await fetch('/api/transactions');
    const data = await response.json();

    if(!response.ok) {
        alert(data.errors?.join(", ") || "Failed to load data");
        return;
    }

    renderTransactions(data.transactions);
    renderTotals(data.totals);
}

function formatCurrency(value) {
    return `$${Number(value).toFixed(2)}`;
}