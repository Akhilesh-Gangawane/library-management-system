/**
 * Books Page Scripts
 * Handles book listing, searching, filtering, and borrowing on the user-facing pages.
 */

let currentPage = 1;
const perPage = 12;

document.addEventListener('DOMContentLoaded', function () {
    loadBooks();
    loadFilters();

    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        let debounceTimer;
        searchInput.addEventListener('input', function () {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                currentPage = 1;
                loadBooks();
            }, 400);
        });
    }

    const categoryFilter = document.getElementById('category-filter');
    if (categoryFilter) {
        categoryFilter.addEventListener('change', function () {
            currentPage = 1;
            loadBooks();
        });
    }

    const authorFilter = document.getElementById('author-filter');
    if (authorFilter) {
        authorFilter.addEventListener('change', function () {
            currentPage = 1;
            loadBooks();
        });
    }

    const availableFilter = document.getElementById('available-filter');
    if (availableFilter) {
        availableFilter.addEventListener('change', function () {
            currentPage = 1;
            loadBooks();
        });
    }
});

async function loadFilters() {
    // Load categories
    const catResult = await apiRequest('/api/books/categories');
    if (catResult.success) {
        const catSelect = document.getElementById('category-filter');
        if (catSelect) {
            catResult.data.forEach(function (cat) {
                const opt = document.createElement('option');
                opt.value = cat.id;
                opt.textContent = cat.name;
                catSelect.appendChild(opt);
            });
        }
    }

    // Load authors
    const authResult = await apiRequest('/api/books/authors');
    if (authResult.success) {
        const authSelect = document.getElementById('author-filter');
        if (authSelect) {
            authResult.data.forEach(function (author) {
                const opt = document.createElement('option');
                opt.value = author.id;
                opt.textContent = author.name;
                authSelect.appendChild(opt);
            });
        }
    }
}

async function loadBooks() {
    const container = document.getElementById('books-container');
    const paginationEl = document.getElementById('pagination');

    if (!container) return;

    container.innerHTML = '<div class="loading-spinner"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div><p class="mt-2 text-muted">Loading books...</p></div>';

    // Build query params
    const params = new URLSearchParams();
    params.set('page', currentPage);
    params.set('per_page', perPage);

    const search = document.getElementById('search-input');
    if (search && search.value.trim()) {
        params.set('search', search.value.trim());
    }

    const catFilter = document.getElementById('category-filter');
    if (catFilter && catFilter.value) {
        params.set('category_id', catFilter.value);
    }

    const authFilter = document.getElementById('author-filter');
    if (authFilter && authFilter.value) {
        params.set('author_id', authFilter.value);
    }

    const availFilter = document.getElementById('available-filter');
    if (availFilter && availFilter.checked) {
        params.set('available_only', 'true');
    }

    const result = await apiRequest(`/api/books?${params.toString()}`);

    if (result.success) {
        if (result.data.length === 0) {
            container.innerHTML = '<div class="empty-state"><i class="bi bi-book"></i><p>No books found.</p></div>';
            if (paginationEl) paginationEl.innerHTML = '';
            return;
        }

        let html = '<div class="row g-3">';
        result.data.forEach(function (book) {
            html += renderBookCard(book);
        });
        html += '</div>';
        container.innerHTML = html;

        // Render pagination
        if (paginationEl && result.pagination) {
            paginationEl.innerHTML = renderPagination(result.pagination);
        }
    } else {
        container.innerHTML = '<div class="empty-state"><p>Failed to load books.</p></div>';
    }
}

function renderBookCard(book) {
    const availBadge = book.is_available
        ? '<span class="badge badge-available">Available</span>'
        : '<span class="badge badge-unavailable">Unavailable</span>';

    const coverHtml = book.cover_image
        ? `<img src="${book.cover_image}" class="book-cover" alt="${book.title}">`
        : `<div class="book-cover-placeholder"><i class="bi bi-book"></i></div>`;

    return `
        <div class="col-sm-6 col-md-4 col-lg-3">
            <div class="card book-card" onclick="window.location.href='/books/${book.id}'">
                ${coverHtml}
                <div class="card-body">
                    <h6 class="card-title mb-1">${book.title}</h6>
                    <p class="text-muted-custom mb-1">${book.author ? book.author.name : 'Unknown Author'}</p>
                    <p class="text-muted-custom mb-2" style="font-size:0.8rem;">${book.category ? book.category.name : ''}</p>
                    <div class="d-flex justify-content-between align-items-center">
                        ${availBadge}
                        <small class="text-muted">${book.available_copies}/${book.total_copies}</small>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function renderPagination(pagination) {
    if (pagination.total_pages <= 1) return '';

    let html = '<nav><ul class="pagination pagination-sm justify-content-center">';

    // Previous
    html += `<li class="page-item ${pagination.has_prev ? '' : 'disabled'}">
        <a class="page-link" href="#" onclick="goToPage(${currentPage - 1}); return false;">Previous</a>
    </li>`;

    // Page numbers
    for (let i = 1; i <= pagination.total_pages; i++) {
        if (i === currentPage) {
            html += `<li class="page-item active"><span class="page-link">${i}</span></li>`;
        } else if (Math.abs(i - currentPage) <= 2 || i === 1 || i === pagination.total_pages) {
            html += `<li class="page-item"><a class="page-link" href="#" onclick="goToPage(${i}); return false;">${i}</a></li>`;
        } else if (Math.abs(i - currentPage) === 3) {
            html += '<li class="page-item disabled"><span class="page-link">...</span></li>';
        }
    }

    // Next
    html += `<li class="page-item ${pagination.has_next ? '' : 'disabled'}">
        <a class="page-link" href="#" onclick="goToPage(${currentPage + 1}); return false;">Next</a>
    </li>`;

    html += '</ul></nav>';
    return html;
}

function goToPage(page) {
    currentPage = page;
    loadBooks();
    window.scrollTo(0, 0);
}

/**
 * Book Detail Page Functions
 */
async function loadBookDetail(bookId) {
    const container = document.getElementById('book-detail');
    if (!container) return;

    const result = await apiRequest(`/api/books/${bookId}`);

    if (result.success) {
        const book = result.data;
        document.getElementById('book-title').textContent = book.title;
        document.getElementById('book-author').textContent = book.author ? book.author.name : 'Unknown';
        document.getElementById('book-category').textContent = book.category ? book.category.name : 'N/A';
        document.getElementById('book-isbn').textContent = book.isbn;
        document.getElementById('book-publisher').textContent = book.publisher || 'N/A';
        document.getElementById('book-year').textContent = book.published_year || 'N/A';
        document.getElementById('book-description').textContent = book.description || 'No description available.';
        document.getElementById('book-copies').textContent = `${book.available_copies} of ${book.total_copies}`;

        const statusEl = document.getElementById('book-status');
        if (book.is_available) {
            statusEl.innerHTML = '<span class="badge badge-available">Available</span>';
        } else {
            statusEl.innerHTML = '<span class="badge badge-unavailable">Unavailable</span>';
        }

        // Show borrow button only for logged-in users and available books
        const borrowBtn = document.getElementById('borrow-btn');
        if (borrowBtn) {
            if (isLoggedIn() && !isAdmin() && book.is_available) {
                borrowBtn.style.display = 'inline-block';
                borrowBtn.onclick = function () { borrowBook(book.id); };
            } else if (!isLoggedIn()) {
                borrowBtn.style.display = 'inline-block';
                borrowBtn.textContent = 'Login to Borrow';
                borrowBtn.onclick = function () { window.location.href = '/login'; };
            } else {
                borrowBtn.style.display = 'none';
            }
        }

        container.style.display = 'block';
    } else {
        container.innerHTML = '<div class="empty-state"><p>Book not found.</p></div>';
    }
}

async function borrowBook(bookId) {
    if (!requireAuth()) return;

    const btn = document.getElementById('borrow-btn');
    btn.disabled = true;
    btn.textContent = 'Processing...';

    const result = await apiRequest('/api/borrowings', {
        method: 'POST',
        body: JSON.stringify({ book_id: bookId }),
    });

    btn.disabled = false;
    btn.textContent = 'Borrow This Book';

    if (result.success) {
        showAlert('alert-container', 'Book borrowed successfully! Due in 14 days.', 'success');
        btn.style.display = 'none';
        // Refresh the book detail to update availability
        loadBookDetail(bookId);
    } else {
        showAlert('alert-container', result.message || 'Failed to borrow book.');
    }
}
