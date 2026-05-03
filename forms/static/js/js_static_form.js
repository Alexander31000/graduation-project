document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.querySelector('input[type="file"]');
    const previewBox = document.getElementById('imagePreview');

    // Предпросмотр изображения
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                previewBox.innerHTML = ''; // Очищаем текст внутри

                reader.onload = function(e) {
                    previewBox.style.backgroundImage = `url(${e.target.result})`;
                    previewBox.style.borderStyle = 'solid';
                }
                reader.readAsDataURL(file);
            }
        });
    }

    // Простая анимация кнопки при отправке
    const form = document.getElementById('bookForm');
    form.addEventListener('submit', function() {
        const btn = this.querySelector('.btn-primary');
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Сохранение...';
        btn.style.opacity = '0.7';
        btn.style.pointerEvents = 'none';
    });
});
