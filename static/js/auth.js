/**
 * Authentication Scripts
 * Handles login and registration form submissions.
 */

document.addEventListener('DOMContentLoaded', function () {
    // If already logged in, redirect appropriately
    if (isLoggedIn()) {
        const user = getCurrentUser();
        if (user && user.is_admin) {
            window.location.href = '/admin';
        } else {
            window.location.href = '/dashboard';
        }
        return;
    }

    // Login form handler
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    // Registration form handler
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }
});

async function handleLogin(e) {
    e.preventDefault();

    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const submitBtn = e.target.querySelector('button[type="submit"]');

    if (!email || !password) {
        showAlert('alert-container', 'Please fill in all fields.');
        return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = 'Signing in...';

    const result = await apiRequest('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
    });

    submitBtn.disabled = false;
    submitBtn.textContent = 'Sign In';

    if (result.success) {
        localStorage.setItem('token', result.data.access_token);
        localStorage.setItem('user', JSON.stringify(result.data.user));

        if (result.data.user.is_admin) {
            window.location.href = '/admin';
        } else {
            window.location.href = '/dashboard';
        }
    } else {
        showAlert('alert-container', result.message || 'Login failed.');
    }
}

async function handleRegister(e) {
    e.preventDefault();

    const fullName = document.getElementById('full-name').value.trim();
    const email = document.getElementById('email').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    const submitBtn = e.target.querySelector('button[type="submit"]');

    if (!fullName || !email || !password) {
        showAlert('alert-container', 'Please fill in all required fields.');
        return;
    }

    if (password !== confirmPassword) {
        showAlert('alert-container', 'Passwords do not match.');
        return;
    }

    if (password.length < 6) {
        showAlert('alert-container', 'Password must be at least 6 characters.');
        return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = 'Creating Account...';

    const result = await apiRequest('/api/auth/register', {
        method: 'POST',
        body: JSON.stringify({
            full_name: fullName,
            email: email,
            password: password,
            phone: phone || null,
        }),
    });

    submitBtn.disabled = false;
    submitBtn.textContent = 'Create Account';

    if (result.success) {
        localStorage.setItem('token', result.data.access_token);
        localStorage.setItem('user', JSON.stringify(result.data.user));
        window.location.href = '/dashboard';
    } else {
        showAlert('alert-container', result.message || 'Registration failed.');
    }
}
