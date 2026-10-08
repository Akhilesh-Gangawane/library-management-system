/**
 * Utility Functions
 * Common helper functions used across the frontend.
 */

const API_BASE = '';

/**
 * Make an authenticated API request.
 * Automatically attaches the JWT token from localStorage.
 */
async function apiRequest(url, options = {}) {
    const token = localStorage.getItem('token');
    const headers = {
        'Content-Type': 'application/json',
        ...(options.headers || {}),
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(`${API_BASE}${url}`, {
            ...options,
            headers,
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('API request failed:', error);
        return { success: false, message: 'Network error. Please try again.' };
    }
}

/**
 * Get the currently stored user object from localStorage.
 */
function getCurrentUser() {
    const userStr = localStorage.getItem('user');
    if (userStr) {
        try {
            return JSON.parse(userStr);
        } catch {
            return null;
        }
    }
    return null;
}

/**
 * Check if a user is currently logged in.
 */
function isLoggedIn() {
    return !!localStorage.getItem('token');
}

/**
 * Check if the current user is an admin.
 */
function isAdmin() {
    const user = getCurrentUser();
    return user && user.is_admin;
}

/**
 * Log the user out by clearing stored credentials and redirecting.
 */
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login';
}

/**
 * Show a Bootstrap alert message inside a container element.
 */
function showAlert(containerId, message, type = 'danger') {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
    }
}

/**
 * Format a date string for display.
 */
function formatDate(dateStr) {
    if (!dateStr) return '—';
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
    });
}

/**
 * Get an appropriate CSS class for a borrowing status badge.
 */
function getStatusBadgeClass(status) {
    switch (status) {
        case 'borrowed': return 'badge-borrowed';
        case 'returned': return 'badge-returned';
        case 'overdue': return 'badge-overdue';
        default: return 'bg-secondary';
    }
}

/**
 * Update the navbar based on login state.
 * Shows/hides appropriate nav items.
 */
function updateNavbar() {
    const user = getCurrentUser();
    const loggedIn = isLoggedIn();

    const guestNav = document.getElementById('guest-nav');
    const userNav = document.getElementById('user-nav');
    const adminNav = document.getElementById('admin-nav');
    const userNameEl = document.getElementById('nav-user-name');

    if (guestNav) guestNav.style.display = loggedIn ? 'none' : 'flex';
    if (userNav) userNav.style.display = loggedIn ? 'flex' : 'none';
    if (adminNav) adminNav.style.display = (loggedIn && user && user.is_admin) ? 'flex' : 'none';
    if (userNameEl && user) userNameEl.textContent = user.full_name;
}

/**
 * Require authentication for the current page.
 * Redirects to login if not authenticated.
 */
function requireAuth() {
    if (!isLoggedIn()) {
        window.location.href = '/login';
        return false;
    }
    return true;
}

/**
 * Require admin role for the current page.
 * Redirects to home if not an admin.
 */
function requireAdminAuth() {
    if (!isLoggedIn()) {
        window.location.href = '/login';
        return false;
    }
    if (!isAdmin()) {
        window.location.href = '/';
        return false;
    }
    return true;
}

// Update navbar on every page load
document.addEventListener('DOMContentLoaded', updateNavbar);
