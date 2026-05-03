document.getElementById('registrationForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    const matchError = document.getElementById('match-error');

    // Проверка совпадения паролей
    if (password !== confirmPassword) {
        matchError.style.display = 'block';
        document.getElementById('confirm-password').style.borderColor = '#e74c3c';
        return;
    } else {
        matchError.style.display = 'none';
        document.getElementById('confirm-password').style.borderColor = '#ddd';
    }

    // Собираем данные
    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries());

    console.log('Данные формы:', data);
    alert('Регистрация прошла успешно! (Данные выведены в консоль)');
});