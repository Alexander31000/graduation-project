document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('rent-form');
    const checkboxes = form.querySelectorAll('input[type="checkbox"]');
    const countDisplay = document.getElementById('selected-count');
    const priceDisplay = document.getElementById('total-price');

    // Предположим, средняя цена за книгу 50 руб/день (для демонстрации)
    const PRICE_PER_DAY = 50;

    function updateSummary() {
        let selectedCount = 0;
        checkboxes.forEach(cb => {
            if (cb.checked) selectedCount++;
        });

        countDisplay.textContent = selectedCount;

        // Примерный расчет: кол-во книг * константу
        // Для точного расчета нужно передать цены из Django в data-атрибуты
        priceDisplay.textContent = selectedCount * PRICE_PER_DAY;
    }

    checkboxes.forEach(cb => {
        cb.addEventListener('change', updateSummary);


    });
});

const checkboxes = document.querySelectorAll(
    'input[type="checkbox"]'
);

const selectedList = document.getElementById(
    'selected-books-list'
);

const countSpan = document.getElementById(
    'selected-count'
);

function updateSelectedBooks() {

    selectedList.innerHTML = '';

    let count = 0;

    checkboxes.forEach(checkbox => {

        if (checkbox.checked) {

            count++;

            const li = document.createElement('li');

            const label = checkbox.parentElement.innerText;

            li.textContent = label;

            selectedList.appendChild(li);
        }
    });

    countSpan.textContent = count;
}

checkboxes.forEach(checkbox => {

    checkbox.addEventListener(
        'change',
        updateSelectedBooks
    );

});

updateSelectedBooks();
const searchInput = document.getElementById('book-search');

searchInput.addEventListener('keyup', function () {

    const searchValue = this.value.toLowerCase();

    const labels = document.querySelectorAll(
        '.books-selection label'
    );

    labels.forEach(label => {

        const text = label.innerText.toLowerCase();

        if (text.includes(searchValue)) {
            label.style.display = 'block';
        } else {
            label.style.display = 'none';
        }

    });

});

