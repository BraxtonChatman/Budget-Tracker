import { logout } from "../api/auth.js";

export function showDashboardView(user, onLogout) {
    const app = document.getElementById("app");

    app.innerHTML = `
        <h2>Welcome ${user.username}</h2>

        <button id="logoutBtn">Logout</button>

        <div id="dashboard">
            Loading transactions...
        </div>
    `;

    document.getElementById("logoutBtn").onclick = async () => {
        await logout();
        onLogout();
    };
}