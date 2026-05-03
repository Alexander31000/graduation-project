// Данные о книгах
const books = Array.from({ length: 20 }, (_, i) => ({
    id: i + 1,
    title: `Книга Высокого Рейтинга №${i + 1}`,
    author: `Автор ${i + 1}`,
    rating: (Math.random() * (5 - 4.5) + 4.5).toFixed(1)
}));

// Рендер книг
const bookGrid = document.getElementById('bookGrid');

function displayBooks(items) {
//     bookGrid.innerHTML = items.map(book => `
//        <div class="book-card">
//            <div class="book-img"><i class="fas fa-book-open fa-3x"></i></div>
//            <div class="book-title">${book.title}</div>
//            <div class="author">${book.author}</div>
//            <div class="rating"><i class="fas fa-star"></i> ${book.rating}</div>
//            <button class="add-btn" style="width:100%; padding: 8px; cursor:pointer; background: #3498db; border:none; color:white; border-radius:5px;">В корзину</button>
//        </div>
//    `).join('');
}

// Управление меню
const burgerBtn = document.getElementById('burgerBtn');
const sideMenu = document.getElementById('sideMenu');
const overlay = document.getElementById('overlay');

function toggleMenu() {
    sideMenu.classList.toggle('active');
    overlay.classList.toggle('active');
}

burgerBtn.addEventListener('click', toggleMenu);
overlay.addEventListener('click', toggleMenu);

// Поиск
const searchInput = document.getElementById('searchInput');
searchInput.addEventListener('input', (e) => {
    const term = e.target.value.toLowerCase();
    const filtered = books.filter(b =>
        b.title.toLowerCase().includes(term) ||
        b.author.toLowerCase().includes(term)
    );
    displayBooks(filtered);
});

// Инициализация
displayBooks(books);
