import { login } from "../api/auth.js";

export function showLoginView(onSuccess, onSwitchToRegister) {
    const app = document.getElementById("app");

    app.innerHTML = `
        <h2>Login</h2>

        <input id="username" placeholder="Username" />
        <input id="password" type="password" placeholder="Password" />

        <button id="loginBtn">Login</button>
        <button id="goToRegisterBtn">Register</button>

        <p id="error"></p>
    `;

    document.getElementById("loginBtn").onclick = async () => {
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        try {
            const user = await login(username, password);
            onSuccess(user);
        } catch (err) {
            document.getElementById("error").textContent = err.message;
        }
    };

    document.getElementById("goToRegisterBtn").onclick = async () => {
        onSwitchToRegister();
    }
}