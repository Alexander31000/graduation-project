document.getElementById('loginForm').addEventListener('submit', function(event) {
    const usernameInput = document.getElementById('username').value;
    const passwordInput = document.getElementById('password').value;
    const messageElement = document.getElementById('message');

    // Простая проверка на пустые поля
    if (usernameInput.trim() === '' || passwordInput.trim() === '') {
        event.preventDefault(); // Остановить отправку формы
        messageElement.textContent = 'Пожалуйста, заполните все поля.';
    } else {
        messageElement.textContent = '';
        console.log('Попытка входа для:', usernameInput);
        // В реальном приложении здесь форма отправится на сервер Django
    }
});
