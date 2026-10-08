/**
 * Dashboard Scripts
 * Handles user dashboard, borrowing history, and profile pages.
 */

document.addEventListener('DOMContentLoaded', function () {
    const page = document.body.getAttribute('data-page');

    if (page === 'dashboard') {
        if (!requireAuth()) return;
        loadDashboard();
    } else if (page === 'history') {
        if (!requireAuth()) return;
        loadHistory();
    } else if (page === 'profile') {
        if (!requireAuth()) return;
        loadProfile();
    }
});

async function loadDashboard() {
    const user = getCurrentUser();
    const welcomeEl = document.getElementById('welcome-name');
    if (welcomeEl) welcomeEl.textContent = user ? user.full_name : 'User';

    // Load active borrowings
    const result = await apiRequest('/api/borrowings/my-history?per_page=50');

    if (result.success) {
        const active = result.data.filter(function (b) { return b.status === 'borrowed'; });
        const returned = result.data.filter(function (b) { return b.status === 'returned'; });

        document.getElementById('active-count').textContent = active.length;
        document.getElementById('returned-count').textContent = returned.length;
        document.getElementById('total-count').textContent = result.data.length;

        // Render active borrowings table
        const tbody = document.getElementById('active-borrowings');
        if (tbody) {
            if (active.length === 0) {
                tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted py-3">No active borrowings</td></tr>';
            } else {
                tbody.innerHTML = active.map(function (b) {
                    return `<tr>
                        <td>${b.book ? b.book.title : 'N/A'}</td>
                        <td>${b.book ? b.book.author : 'N/A'}</td>
                        <td>${formatDate(b.borrow_date)}</td>
                        <td>${formatDate(b.due_date)}</td>
                        <td>
                            <button class="btn btn-sm btn-outline-primary" onclick="returnBook(${b.id})">
                                Return
                            </button>
                        </td>
                    </tr>`;
                }).join('');
            }
        }
    }
}

async function returnBook(borrowingId) {
    const result = await apiRequest(`/api/borrowings/${borrowingId}/return`, {
        method: 'PUT',
    });

    if (result.success) {
        showAlert('alert-container', 'Book returned successfully!', 'success');
        loadDashboard();
    } else {
        showAlert('alert-container', result.message || 'Failed to return book.');
    }
}

async function loadHistory() {
    const tbody = document.getElementById('history-tbody');
    if (!tbody) return;

    const result = await apiRequest('/api/borrowings/my-history?per_page=50');

    if (result.success) {
        if (result.data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted py-3">No borrowing history</td></tr>';
            return;
        }

        tbody.innerHTML = result.data.map(function (b) {
            const statusClass = getStatusBadgeClass(b.status);
            return `<tr>
                <td>${b.book ? b.book.title : 'N/A'}</td>
                <td>${formatDate(b.borrow_date)}</td>
                <td>${formatDate(b.due_date)}</td>
                <td>${formatDate(b.return_date)}</td>
                <td><span class="badge ${statusClass}">${b.status}</span></td>
            </tr>`;
        }).join('');
    }
}

async function loadProfile() {
    const result = await apiRequest('/api/auth/profile');

    if (result.success) {
        const u = result.data;
        document.getElementById('profile-name').textContent = u.full_name;
        document.getElementById('profile-email').textContent = u.email;
        document.getElementById('profile-phone').textContent = u.phone || 'Not set';
        document.getElementById('profile-role').textContent = u.is_admin ? 'Administrator' : 'Member';
        document.getElementById('profile-joined').textContent = formatDate(u.created_at);

        // Pre-fill edit form
        document.getElementById('edit-name').value = u.full_name;
        document.getElementById('edit-phone').value = u.phone || '';
    }

    const profileForm = document.getElementById('profile-form');
    if (profileForm) {
        profileForm.addEventListener('submit', handleProfileUpdate);
    }
}

async function handleProfileUpdate(e) {
    e.preventDefault();

    const fullName = document.getElementById('edit-name').value.trim();
    const phone = document.getElementById('edit-phone').value.trim();

    const result = await apiRequest('/api/auth/profile', {
        method: 'PUT',
        body: JSON.stringify({
            full_name: fullName || null,
            phone: phone || null,
        }),
    });

    if (result.success) {
        // Update localStorage
        const user = getCurrentUser();
        if (user) {
            user.full_name = result.data.full_name;
            user.phone = result.data.phone;
            localStorage.setItem('user', JSON.stringify(user));
        }
        showAlert('profile-alert', 'Profile updated successfully!', 'success');
        loadProfile();
        updateNavbar();
    } else {
        showAlert('profile-alert', result.message || 'Failed to update profile.');
    }
}
