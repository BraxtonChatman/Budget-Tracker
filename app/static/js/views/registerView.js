import { register } from "../api/auth.js";

export function showRegisterView(onSuccess, onBackToLogin) {
    const app = document.getElementById("app");

    app.innerHTML = `
        <h2>Register</h2>

        <input id="username" placeholder="Username" />
        <input id="password" type="password" placeholder="Password" />

        <button id="registerBtn">Create Account</button>
        <button id="backToLoginBtn">Back to Login</button>

        <p id="error"></p>
    `;

    document.getElementById("registerBtn").onclick = async () => {
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        try {
            const user = await register(username, password);
            onSuccess(user);
        } catch (err) {
            document.getElementById("error").textContent = err.message;
        }
    };

    document.getElementById("backToLoginBtn").onclick = () => {
        onBackToLogin();
    };
}