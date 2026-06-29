
export async function getTransactions(filters = {}) {
    const params = new URLSearchParams();
    
    if (filters.category) params.append("category", filters.category);
    if (filters.start_date) params.append("start_date", filters.start_date);
    if (filters.end_date) params.append("end_date", filters.end_date);
    if (filters.sort_by) params.append("sort_by", filters.sort_by);

    const res = await fetch(`/api/transactions?${params.toString()}`);
    const data = await res.json();

    if(!res.ok) {
        throw new Error(data.errors?.join(", ") || "Failed to load transactions");
    }

    return data;
}

export async function getTransaction(txId) {
    const res = await fetch(`/api/transactions/${txId}`);
    const data = await res.json();

    if(!res.ok) {
        throw new Error(data.errors?.join(", ") || "Failed to load transaction");
    }

    return data;
}

export async function createTransaction(payload) {
    const res = await fetch(`/api/transactions`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });
    const data = await res.json();

    if(!res.ok){
        throw new Error(data.errors?.join(", ") || "Failed to add transaction");
    }

    return data;
}

export async function updateTransaction(txId, payload) {
    const res = await fetch(`/api/transactions/${txId}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });
    const data = await res.json();

    if(!res.ok){
        throw new Error(data.errors?.join(", ") || "Failed to edit transaction");
    }

    return data;
}

export async function deleteTransaction(txId) {
    const res = await fetch(`/api/transactions/${txId}`, {method: "DELETE"});
    const data = await res.json();
   
    if(!res.ok) {
        throw new Error(data.errors?.join(", ") || "Delete failed");
    }

    return data;
}