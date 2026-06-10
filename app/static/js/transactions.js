
// ask about these
const modal = document.getElementById("edit-modal");
const editId = document.getElementById("edit-id");
const editDate = document.getElementById("edit-date");
const editCategory = document.getElementById("edit-category");
const editDescription = document.getElementById("edit-description");
const editAmount = document.getElementById("edit-amount");
const editType = document.getElementById("edit-type");

document.addEventListener("DOMContentLoaded", init);

async function init() {
    setupEventListeners();
    await refreshTransactions();
}

function setupEventListeners() {
    const tbody = document.querySelector("tbody");
    tbody.addEventListener("click", handleTableClick);
}

async function handleTableClick(event) {
    const deleteButton = event.target.closest(".js-delete-transaction");
    if(deleteButton) return handleDelete(deleteButton);

    const editButton = event.target.closest(".js-edit-transaction");
    if(editButton) return handleEdit(editButton);

    // if(!deleteButton) return;

    // const txId = deleteButton.dataset.transactionId;
    // const confirmed = confirm("Are you sure you want to delete this transaction?");
    // if(!confirmed) return;

    // try{
    //     const response = await fetch(`/api/transactions/${txId}`, {method: "DELETE"});
    //     let data;

    //     try{
    //         data = await response.json();
    //     } catch {
    //         alert("Invalid server response");
    //         return
    //     }

    //     if(!response.ok) {
    //         alert(data.errors?.join(", ") || "Delete failed");
    //         return;
    //     }
    //     await refreshTransactions();

    // } catch(err) {
    //     console.error(err);
    //     alert("An unexpected error occurred.");
    // }
}

async function handleDelete(deleteButton){
    const txId = deleteButton.dataset.transactionId;
    
    const confirmed = confirm("Are you sure you want to delete this transaction?");
    if(!confirmed) return;

    try{
        const response = await fetch(`/api/transactions/${txId}`, {method: "DELETE"});
        
        let data;
        try{
            data = await response.json();
        } catch {
            alert("Invalid server response");
            return
        }

        if(!response.ok) {
            alert(data.errors?.join(", ") || "Delete failed");
            return;
        }
        await refreshTransactions();

    } catch(err) {
        console.error(err);
        alert("An unexpected error occurred.");
    }
}

async function handleEdit(editButton){
    const txId = editButton.dataset.transactionId;
    
    try{
        const response = await fetch(`/api/transactions/${txId}`);
        
        let data;
        try{
            data = await response.json();
        } catch {
            alert("Invalid server response");
            return;
        }

        if(!response.ok){
            alert(data.errors?.join(", ") || "Failed to load transaction");
            return;
        }

        const tx = data.transaction;

        editId.value = tx.id;
        editDate.value = tx.date;
        editCategory.value = tx.category_id;
        editDescription.value = tx.description;
        editAmount.value = tx.amount;
        editType.value = tx.type;

        document.getElementById("edit-modal").classList.remove("hidden");

    } catch(err){
        console.error(err);
        alert("An unexpected error occurred.");
    }  
}

// cancel button
document.getElementById("cancel-edit").addEventListener("click", () => {document.getElementById("edit-modal").classList.add("hidden")});

// ask about this
// save button
document.getElementById("save-edit").addEventListener("click", async () => {
    const txId = editId.value;

    const payload = {
        date: editDate.value,
        category: editCategory.value,
        description: editDescription.value,
        amount: parseFloat(editAmount.value),
        type: editType.value
    };

    try{
        const response = await fetch(`/api/transactions/${txId}`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        let data;
        try{
            data = await response.json();
        } catch {
            alert("Invalid server response");
            return;
        }

        if(!response.ok) {
            alert(data.errors?.join(", ") || "Update failed");
            return;
        }

        await refreshTransactions();
        document.getElementById("edit-modal").classList.add("hidden");
    } 
    catch(err){
        console.error(err);
        alert("Unexpected error occurred.");
    }
});


// async function handleEditClick(event) {
//     const button = event.target.closest(".js-edit-transaction");
//     if(!button) return;

//     const txId = button.dataset.transactionId;


// }

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
                <button
                    class="form-button edit-button js-edit-transaction"
                    data-transaction-id="${t.id}">
                    Edit
                </button>
                <button 
                    class="form-button delete-button js-delete-transaction" 
                    data-transaction-id="${t.id}">
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