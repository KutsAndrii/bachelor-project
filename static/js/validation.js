document.addEventListener('DOMContentLoaded', function () {
  const form = document.querySelector('form');
  const emailInput = document.getElementById('email');
  const passwordInput = document.getElementById('password');
  const confirmPasswordInput = document.getElementById('confirm-password');

  /**
   * Відображає повідомлення про помилку під полем вводу.
   *
   * @param {HTMLElement} element - Поле вводу, біля якого відображається помилка.
   * @param {string} message - Текст повідомлення.
   */
  function showError(element, message) {
      const existingError = element.parentElement.querySelector('.error-message');
      if (existingError) existingError.remove();

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

  /**
   * Видаляє всі попередні повідомлення про помилки з форми.
   */
  function clearErrors() {
      const errors = document.querySelectorAll('.error-message');
      errors.forEach(error => error.remove());
  }

  // Обробка події надсилання форми
  form.addEventListener('submit', function (e) {
      e.preventDefault(); // Зупиняємо стандартну відправку форми
      clearErrors(); // Скидаємо попередні помилки

      let hasError = false;

      // 🔸 Перевірка email
      const emailValue = emailInput.value.trim();
      const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
      if (!emailValue) {
          showError(emailInput, 'Email обов’язковий для заповнення.');
          hasError = true;
      } else if (!emailRegex.test(emailValue)) {
          showError(emailInput, 'Email має містити тільки допустимі символи.');
          hasError = true;
      }

      // 🔸 Перевірка пароля
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

      // 🔸 Перевірка підтвердження пароля
      const confirmPasswordValue = confirmPasswordInput.value.trim();
      if (!confirmPasswordValue) {
          showError(confirmPasswordInput, 'Підтвердження пароля обов’язкове.');
          hasError = true;
      } else if (passwordValue !== confirmPasswordValue) {
          showError(confirmPasswordInput, 'Паролі не співпадають.');
          hasError = true;
      }

      // Якщо помилок не виявлено — відправляємо форму
      if (!hasError) {
          form.submit();
      }
  });
});
