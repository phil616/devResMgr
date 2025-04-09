import Cookies from "js-cookie";

function checkAuthorizaion() {
    console.log("Checking authorization");
    const token = Cookies.get("token");
    if (token) {
        return true
    } else {
        return false;
    }
}

function loadSessionToken() {
    const token = sessionStorage.getItem("token");
    if (token) {
        return token;
    } else {
        return null;
    }
}

function logout() {
    Cookies.remove("username");
    Cookies.remove("token");
    sessionStorage.removeItem("token");
}

export { checkAuthorizaion, logout, loadSessionToken };