import { getMe } from "./api/auth.js";
import { showRegisterView } from "./views/registerView.js";
import { showLoginView } from "./views/loginView.js";
import { showDashboardView } from "./views/dashboardView.js";

document.addEventListener("DOMContentLoaded", init);

async function init() {
    await routeToApp();
}

async function routeToApp() {
    const user = await getMe();

    if (!user) {
        showLogin();
        return;
    }
    showDashboard(user);
}

function showLogin() {
    showLoginView(
        onLoginSuccess,
        showRegister
    );
}

function showRegister() {
    showRegisterView(
        onRegisterSuccess,
        showLogin
    );
}

function showDashboard(user) {
    showDashboardView(
        user,
        onLogout
    );
}

function onLoginSuccess(user){
    showDashboard(user);
}

function onRegisterSuccess(user) {
    showDashboard(user);
}

function onLogout() {
    showLogin();
}
