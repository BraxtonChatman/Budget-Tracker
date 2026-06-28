
export async function getMe() {
    try {
        const res = await fetch("/api/auth/me");

        if (res.status === 401){
            return null;
        }

        if (!res.ok) {
            throw new Error("Server error");
        }

        return await res.json();

    } catch (err) {
        throw new Error("Network error");
    }
}

export async function login(username, password) {
    const res = await fetch("/api/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password })
    });

    const data = await res.json();

    if (!res.ok) {
        throw new Error(data.errors?.join(", ") || "Login failed");
    }

    return data.user;
}

export async function logout() {
    await fetch("/api/auth/logout", {
        method: "POST"
    });
}

export async function register(username, password) {
    const res = await fetch("/api/auth/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password })
    });

    const data = await res.json();

    if(!res.ok) {
        throw new Error(data.errors?.join(", ") || "Registration failed");
    }

    return data.user;
}