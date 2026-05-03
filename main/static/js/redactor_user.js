document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('updateForm');
    const passwordInput = document.getElementById('id_password');

    form.addEventListener('submit', function(e) {
        const passwordValue = passwordInput.value;

        // Если пароль введён, но он короче 8 символов
        if (passwordValue.length > 0 && passwordValue.length < 8) {
            e.preventDefault();
            alert('Если вы меняете пароль, он должен быть не менее 8 символов!');
        }
    });

    // Визуальный отклик при вводе
    passwordInput.addEventListener('input', function() {
        if (this.value.length > 0) {
            this.style.borderColor = '#fdcb6e'; // Предупреждающий цвет
        } else {
            this.style.borderColor = '#dfe6e9';
        }
    });
});
