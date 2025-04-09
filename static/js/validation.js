document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm-password');
  
    // Функція для створення блоку повідомлень про помилки
    function showError(element, message) {
      // Видаляємо попереднє повідомлення, якщо існує
      const existingError = element.parentElement.querySelector('.error-message');
      if (existingError) existingError.remove();
  
      // Створюємо новий елемент для помилки
      const error = document.createElement('div');
      error.textContent = message;
      error.classList.add('error-message');
      error.style.color = 'white';
      error.style.backgroundColor = 'red';
      error.style.marginTop = '5px';
      error.style.padding = '5px';
      error.style.borderRadius = '5px';
      element.parentElement.appendChild(error);
    }
  
    // Очищення помилок
    function clearErrors() {
      const errors = document.querySelectorAll('.error-message');
      errors.forEach(error => error.remove());
    }
  
    form.addEventListener('submit', function (e) {
      e.preventDefault(); // Забороняємо відправку форми, якщо є помилки
      clearErrors(); // Очищуємо попередні помилки
  
      let hasError = false;
  
      // Перевірка Email
      const emailValue = emailInput.value.trim();
      const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
      if (!emailValue) {
        showError(emailInput, 'Email обов’язковий для заповнення.');
        hasError = true;
      } else if (!emailRegex.test(emailValue)) {
        showError(emailInput, 'Email має містити тільки допустимі символи.');
        hasError = true;
      }
  
      // Перевірка Password
      const passwordValue = passwordInput.value.trim();
      if (!passwordValue) {
        showError(passwordInput, 'Пароль обов’язковий для заповнення.');
        hasError = true;
      } else if (passwordValue.includes(' ')) {
        showError(passwordInput, 'Пароль не повинен містити пробілів.');
        hasError = true;
      } else if (passwordValue.length < 4 || passwordValue.length > 12) {
        showError(passwordInput, 'Пароль має бути від 4 до 12 символів.');
        hasError = true;
      }
  
      // Перевірка Confirm Password
      const confirmPasswordValue = confirmPasswordInput.value.trim();
      if (!confirmPasswordValue) {
        showError(confirmPasswordInput, 'Підтвердження пароля обов’язкове.');
        hasError = true;
      } else if (passwordValue !== confirmPasswordValue) {
        showError(confirmPasswordInput, 'Паролі не співпадають.');
        hasError = true;
      }
  
      // Якщо помилок немає, відправляємо форму
      if (!hasError) {
        form.submit();
      }
    });
  });
  