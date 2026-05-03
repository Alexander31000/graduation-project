document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('input, textarea, select');

    // Подсветка измененных полей
    inputs.forEach(input => {
        input.addEventListener('change', function() {
            this.style.borderColor = '#3498db';
            this.style.backgroundColor = '#f0f7ff';
        });
    });

    document.querySelectorAll('.image-edit-item input[type="file"]').forEach(input => {
    input.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            const reader = new FileReader();
            const preview = this.closest('.image-edit-item').querySelector('img');
            reader.onload = e => { preview.src = e.target.result; };
            reader.readAsDataURL(this.files[0]);
        }
    });
});


    // Простая проверка перед отправкой
    const form = document.querySelector('.book-form');
    form.addEventListener('submit', function(e) {
        const title = document.querySelector('[name="title"]').value;
        if (title.length < 2) {
            e.preventDefault();
            alert('Название книги слишком короткое!');
        }
    });
});
