/**
 * Admin Panel Scripts
 * Handles admin dashboard, book management, user listing, and borrowing records.
 */

document.addEventListener('DOMContentLoaded', function () {
    const page = document.body.getAttribute('data-page');

    if (page === 'admin-dashboard') {
        if (!requireAdminAuth()) return;
        loadAdminDashboard();
    } else if (page === 'admin-books') {
        if (!requireAdminAuth()) return;
        loadAdminBooks();
        loadBookFormDropdowns();
    } else if (page === 'admin-users') {
        if (!requireAdminAuth()) return;
        loadAdminUsers();
    } else if (page === 'admin-borrowings') {
        if (!requireAdminAuth()) return;
        loadAdminBorrowings();
    }
});

/* ===================== ADMIN DASHBOARD ===================== */

async function loadAdminDashboard() {
    // Load stats
    const booksRes = await apiRequest('/api/books?per_page=1');
    const usersRes = await apiRequest('/api/admin/users');
    const borrowRes = await apiRequest('/api/admin/borrowings?per_page=1');

    if (booksRes.success && booksRes.pagination) {
        document.getElementById('stat-books').textContent = booksRes.pagination.total;
    }
    if (usersRes.success) {
        document.getElementById('stat-users').textContent = usersRes.data.length;
    }
    if (borrowRes.success && borrowRes.pagination) {
        document.getElementById('stat-borrowings').textContent = borrowRes.pagination.total;
    }

    // Recent borrowings
    const recentRes = await apiRequest('/api/admin/borrowings?per_page=5');
    if (recentRes.success) {
        const tbody = document.getElementById('recent-borrowings');
        if (tbody) {
            if (recentRes.data.length === 0) {
                tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted py-3">No records</td></tr>';
            } else {
                tbody.innerHTML = recentRes.data.map(function (b) {
                    const statusClass = getStatusBadgeClass(b.status);
                    return `<tr>
                        <td>${b.user ? b.user.full_name : 'N/A'}</td>
                        <td>${b.book ? b.book.title : 'N/A'}</td>
                        <td>${formatDate(b.borrow_date)}</td>
                        <td>${formatDate(b.due_date)}</td>
                        <td><span class="badge ${statusClass}">${b.status}</span></td>
                    </tr>`;
                }).join('');
            }
        }
    }
}

/* ===================== BOOK MANAGEMENT ===================== */

async function loadAdminBooks() {
    const tbody = document.getElementById('books-tbody');
    if (!tbody) return;

    const result = await apiRequest('/api/books?per_page=100');

    if (result.success) {
        if (result.data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="text-center text-muted py-3">No books added yet</td></tr>';
            return;
        }

        tbody.innerHTML = result.data.map(function (book) {
            const availBadge = book.is_available
                ? '<span class="badge badge-available">Available</span>'
                : '<span class="badge badge-unavailable">Unavailable</span>';

            return `<tr>
                <td><strong>${book.title}</strong></td>
                <td>${book.author ? book.author.name : 'N/A'}</td>
                <td>${book.isbn}</td>
                <td>${book.category ? book.category.name : 'N/A'}</td>
                <td>${book.available_copies}/${book.total_copies}</td>
                <td>${availBadge}</td>
                <td>
                    <button class="btn btn-sm btn-outline-primary me-1" onclick="editBook(${book.id})">Edit</button>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteBook(${book.id}, '${book.title.replace(/'/g, "\\'")}')">Delete</button>
                </td>
            </tr>`;
        }).join('');
    }
}

function toggleAuthorInput(mode = 'add', forceState = null) {
    const selectGroup = document.getElementById(`author-select-group-${mode}`);
    const inputGroup = document.getElementById(`author-input-group-${mode}`);
    const toggleText = document.getElementById(`author-toggle-text-${mode}`);
    const selectEl = document.getElementById(mode === 'add' ? 'book-author' : 'edit-book-author');
    const inputEl = document.getElementById(mode === 'add' ? 'new-author-name' : 'edit-new-author-name');

    if (!selectGroup || !inputGroup) return;

    const showInput = forceState !== null ? forceState : (inputGroup.style.display === 'none');

    if (showInput) {
        selectGroup.style.display = 'none';
        inputGroup.style.display = 'block';
        if (toggleText) toggleText.textContent = '← Pick Existing Author';
        if (inputEl) inputEl.focus();
    } else {
        selectGroup.style.display = 'block';
        inputGroup.style.display = 'none';
        if (toggleText) toggleText.textContent = '+ Type New Author';
        if (selectEl && selectEl.value === '__new__') selectEl.value = '';
    }
}

function toggleCategoryInput(mode = 'add', forceState = null) {
    const selectGroup = document.getElementById(`category-select-group-${mode}`);
    const inputGroup = document.getElementById(`category-input-group-${mode}`);
    const toggleText = document.getElementById(`category-toggle-text-${mode}`);
    const selectEl = document.getElementById(mode === 'add' ? 'book-category' : 'edit-book-category');
    const inputEl = document.getElementById(mode === 'add' ? 'new-category-name' : 'edit-new-category-name');

    if (!selectGroup || !inputGroup) return;

    const showInput = forceState !== null ? forceState : (inputGroup.style.display === 'none');

    if (showInput) {
        selectGroup.style.display = 'none';
        inputGroup.style.display = 'block';
        if (toggleText) toggleText.textContent = '← Pick Existing Category';
        if (inputEl) inputEl.focus();
    } else {
        selectGroup.style.display = 'block';
        inputGroup.style.display = 'none';
        if (toggleText) toggleText.textContent = '+ Type New Category';
        if (selectEl && selectEl.value === '__new__') selectEl.value = '';
    }
}

async function loadBookFormDropdowns() {
    // Authors
    const authRes = await apiRequest('/api/books/authors');
    if (authRes.success) {
        const authorSelects = document.querySelectorAll('.author-select');
        authorSelects.forEach(function (sel) {
            const currentVal = sel.value;
            sel.innerHTML = '<option value="">Select Author</option><option value="__new__">+ Type New Author...</option>';
            authRes.data.forEach(function (a) {
                const opt = document.createElement('option');
                opt.value = a.id;
                opt.textContent = a.name;
                sel.appendChild(opt);
            });
            if (currentVal && currentVal !== '__new__') {
                sel.value = currentVal;
            }

            // Dropdown change listener
            sel.onchange = function () {
                if (this.value === '__new__') {
                    const mode = this.id.includes('edit') ? 'edit' : 'add';
                    toggleAuthorInput(mode, true);
                }
            };
        });
    }

    // Categories
    const catRes = await apiRequest('/api/books/categories');
    if (catRes.success) {
        const catSelects = document.querySelectorAll('.category-select');
        catSelects.forEach(function (sel) {
            const currentVal = sel.value;
            sel.innerHTML = '<option value="">Select Category</option><option value="__new__">+ Type New Category...</option>';
            catRes.data.forEach(function (c) {
                const opt = document.createElement('option');
                opt.value = c.id;
                opt.textContent = c.name;
                sel.appendChild(opt);
            });
            if (currentVal && currentVal !== '__new__') {
                sel.value = currentVal;
            }

            // Dropdown change listener
            sel.onchange = function () {
                if (this.value === '__new__') {
                    const mode = this.id.includes('edit') ? 'edit' : 'add';
                    toggleCategoryInput(mode, true);
                }
            };
        });
    }
}

// Add Book
const addBookForm = document.getElementById('add-book-form');
if (addBookForm) {
    addBookForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        // Check author
        let authorId = null;
        let newAuthorName = null;
        const authorInputGroup = document.getElementById('author-input-group-add');
        const isNewAuthor = authorInputGroup && authorInputGroup.style.display !== 'none';

        if (isNewAuthor) {
            newAuthorName = document.getElementById('new-author-name').value.trim();
            if (!newAuthorName) {
                showAlert('book-alert', 'Please enter an author name.');
                return;
            }
        } else {
            const val = document.getElementById('book-author').value;
            if (!val || val === '__new__') {
                showAlert('book-alert', 'Please select or type an author.');
                return;
            }
            authorId = parseInt(val);
        }

        // Check category
        let categoryId = null;
        let newCategoryName = null;
        const catInputGroup = document.getElementById('category-input-group-add');
        const isNewCat = catInputGroup && catInputGroup.style.display !== 'none';

        if (isNewCat) {
            newCategoryName = document.getElementById('new-category-name').value.trim();
            if (!newCategoryName) {
                showAlert('book-alert', 'Please enter a category name.');
                return;
            }
        } else {
            const val = document.getElementById('book-category').value;
            if (!val || val === '__new__') {
                showAlert('book-alert', 'Please select or type a category.');
                return;
            }
            categoryId = parseInt(val);
        }

        const data = {
            title: document.getElementById('book-title').value.trim(),
            isbn: document.getElementById('book-isbn').value.trim(),
            description: document.getElementById('book-description').value.trim() || null,
            publisher: document.getElementById('book-publisher').value.trim() || null,
            published_year: parseInt(document.getElementById('book-year').value) || null,
            total_copies: parseInt(document.getElementById('book-copies').value) || 1,
            author_id: authorId,
            new_author_name: newAuthorName,
            category_id: categoryId,
            new_category_name: newCategoryName,
        };

        const result = await apiRequest('/api/admin/books', {
            method: 'POST',
            body: JSON.stringify(data),
        });

        if (result.success) {
            showAlert('book-alert', 'Book added successfully!', 'success');
            addBookForm.reset();
            toggleAuthorInput('add', false);
            toggleCategoryInput('add', false);
            loadAdminBooks();
            loadBookFormDropdowns(); // Refresh dropdowns with any newly created author/category
            const modal = bootstrap.Modal.getInstance(document.getElementById('addBookModal'));
            if (modal) modal.hide();
        } else {
            showAlert('book-alert', result.message || 'Failed to add book.');
        }
    });
}

async function editBook(bookId) {
    const result = await apiRequest(`/api/books/${bookId}`);
    if (!result.success) return;

    const book = result.data;
    document.getElementById('edit-book-id').value = book.id;
    document.getElementById('edit-book-title').value = book.title;
    document.getElementById('edit-book-isbn').value = book.isbn;
    document.getElementById('edit-book-description').value = book.description || '';
    document.getElementById('edit-book-publisher').value = book.publisher || '';
    document.getElementById('edit-book-year').value = book.published_year || '';
    document.getElementById('edit-book-copies').value = book.total_copies;
    document.getElementById('edit-book-available').value = book.available_copies;

    // Reset toggle states to pick from list
    toggleAuthorInput('edit', false);
    toggleCategoryInput('edit', false);

    document.getElementById('edit-book-author').value = book.author_id;
    document.getElementById('edit-book-category').value = book.category_id;

    const modal = new bootstrap.Modal(document.getElementById('editBookModal'));
    modal.show();
}

const editBookForm = document.getElementById('edit-book-form');
if (editBookForm) {
    editBookForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        const bookId = document.getElementById('edit-book-id').value;

        // Author
        let authorId = null;
        let newAuthorName = null;
        const authorInputGroup = document.getElementById('author-input-group-edit');
        if (authorInputGroup && authorInputGroup.style.display !== 'none') {
            newAuthorName = document.getElementById('edit-new-author-name').value.trim();
        } else {
            const val = document.getElementById('edit-book-author').value;
            if (val && val !== '__new__') authorId = parseInt(val);
        }

        // Category
        let categoryId = null;
        let newCategoryName = null;
        const catInputGroup = document.getElementById('category-input-group-edit');
        if (catInputGroup && catInputGroup.style.display !== 'none') {
            newCategoryName = document.getElementById('edit-new-category-name').value.trim();
        } else {
            const val = document.getElementById('edit-book-category').value;
            if (val && val !== '__new__') categoryId = parseInt(val);
        }

        const data = {
            title: document.getElementById('edit-book-title').value.trim(),
            isbn: document.getElementById('edit-book-isbn').value.trim(),
            description: document.getElementById('edit-book-description').value.trim() || null,
            publisher: document.getElementById('edit-book-publisher').value.trim() || null,
            published_year: parseInt(document.getElementById('edit-book-year').value) || null,
            total_copies: parseInt(document.getElementById('edit-book-copies').value) || 1,
            available_copies: parseInt(document.getElementById('edit-book-available').value) || 0,
            author_id: authorId,
            new_author_name: newAuthorName,
            category_id: categoryId,
            new_category_name: newCategoryName,
        };

        const result = await apiRequest(`/api/admin/books/${bookId}`, {
            method: 'PUT',
            body: JSON.stringify(data),
        });

        if (result.success) {
            showAlert('book-alert', 'Book updated successfully!', 'success');
            loadAdminBooks();
            loadBookFormDropdowns();
            const modal = bootstrap.Modal.getInstance(document.getElementById('editBookModal'));
            if (modal) modal.hide();
        } else {
            showAlert('book-alert', result.message || 'Failed to update book.');
        }
    });
}

async function deleteBook(bookId, title) {
    if (!confirm(`Are you sure you want to delete "${title}"?`)) return;

    const result = await apiRequest(`/api/admin/books/${bookId}`, {
        method: 'DELETE',
    });

    if (result.success) {
        showAlert('book-alert', 'Book deleted successfully!', 'success');
        loadAdminBooks();
    } else {
        showAlert('book-alert', result.message || 'Failed to delete book.');
    }
}

// Add Author
const addAuthorForm = document.getElementById('add-author-form');
if (addAuthorForm) {
    addAuthorForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        const data = {
            name: document.getElementById('author-name').value.trim(),
            bio: document.getElementById('author-bio').value.trim() || null,
        };

        const result = await apiRequest('/api/admin/authors', {
            method: 'POST',
            body: JSON.stringify(data),
        });

        if (result.success) {
            showAlert('book-alert', 'Author added successfully!', 'success');
            addAuthorForm.reset();
            loadBookFormDropdowns();
            const modal = bootstrap.Modal.getInstance(document.getElementById('addAuthorModal'));
            if (modal) modal.hide();
        } else {
            showAlert('book-alert', result.message || 'Failed to add author.');
        }
    });
}

// Add Category
const addCategoryForm = document.getElementById('add-category-form');
if (addCategoryForm) {
    addCategoryForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        const data = {
            name: document.getElementById('category-name').value.trim(),
            description: document.getElementById('category-description').value.trim() || null,
        };

        const result = await apiRequest('/api/admin/categories', {
            method: 'POST',
            body: JSON.stringify(data),
        });

        if (result.success) {
            showAlert('book-alert', 'Category added successfully!', 'success');
            addCategoryForm.reset();
            loadBookFormDropdowns();
            const modal = bootstrap.Modal.getInstance(document.getElementById('addCategoryModal'));
            if (modal) modal.hide();
        } else {
            showAlert('book-alert', result.message || 'Failed to add category.');
        }
    });
}

/* ===================== USER MANAGEMENT ===================== */

async function loadAdminUsers() {
    const tbody = document.getElementById('users-tbody');
    if (!tbody) return;

    const result = await apiRequest('/api/admin/users');

    if (result.success) {
        if (result.data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted py-3">No users</td></tr>';
            return;
        }

        tbody.innerHTML = result.data.map(function (u) {
            const roleBadge = u.is_admin
                ? '<span class="badge bg-primary">Admin</span>'
                : '<span class="badge bg-secondary">User</span>';

            return `<tr>
                <td>${u.full_name}</td>
                <td>${u.email}</td>
                <td>${u.phone || '—'}</td>
                <td>${roleBadge}</td>
                <td>${formatDate(u.created_at)}</td>
            </tr>`;
        }).join('');
    }
}

/* ===================== BORROWING RECORDS ===================== */

async function loadAdminBorrowings() {
    const tbody = document.getElementById('borrowings-tbody');
    if (!tbody) return;

    let url = '/api/admin/borrowings?per_page=50';

    const statusFilter = document.getElementById('status-filter');
    if (statusFilter && statusFilter.value) {
        url += `&status=${statusFilter.value}`;
    }

    const result = await apiRequest(url);

    if (result.success) {
        if (result.data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center text-muted py-3">No records found</td></tr>';
            return;
        }

        tbody.innerHTML = result.data.map(function (b) {
            const statusClass = getStatusBadgeClass(b.status);
            return `<tr>
                <td>${b.user ? b.user.full_name : 'N/A'}</td>
                <td>${b.book ? b.book.title : 'N/A'}</td>
                <td>${formatDate(b.borrow_date)}</td>
                <td>${formatDate(b.due_date)}</td>
                <td>${formatDate(b.return_date)}</td>
                <td><span class="badge ${statusClass}">${b.status}</span></td>
            </tr>`;
        }).join('');
    }
}

// Status filter change
document.addEventListener('DOMContentLoaded', function () {
    const statusFilter = document.getElementById('status-filter');
    if (statusFilter) {
        statusFilter.addEventListener('change', loadAdminBorrowings);
    }
});
