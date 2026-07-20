import { login } from "../api/auth.js";

export function showLoginView(onSuccess, onSwitchToRegister) {
    const app = document.getElementById("app");

    app.innerHTML = `
        <div class="container py-5">
            <div class="card p-4 mx-auto" style="max-width: 400px;">
                <h2 class="h3 text-center mb-4">Login</h2>

                <div class="mb-3">
                    <input 
                        id="username" 
                        class="form-control"
                        placeholder="Username" 
                    />
                </div>

                <div class="mb-3">
                    <input 
                        id="password" 
                        type="password" 
                        class="form-control"
                        placeholder="Password" 
                    />
                </div>

                <button id="loginBtn" class="btn btn-primary w-100 mb-2">
                    Login
                </button>

                <button id="goToRegisterBtn" class="btn btn-outline-secondary w-100">
                    Register
                </button>

                <p id="error" class="text-danger mt-3"></p>
            </div>
        </div>
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