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
