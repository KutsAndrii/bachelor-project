document.addEventListener('DOMContentLoaded', function () {
  const form = document.querySelector('form');
  const emailInput = document.getElementById('email');
  const passwordInput = document.getElementById('password');

  /**
   * Відображає повідомлення про помилку під полем форми.
   *
   * @param {HTMLElement} element - Елемент форми.
   * @param {string} message - Текст помилки.
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
   * Видаляє всі повідомлення про помилки.
   */
  function clearErrors() {
      const errors = document.querySelectorAll('.error-message');
      errors.forEach(error => error.remove());
  }

  // Подія сабміту форми входу
  form.addEventListener('submit', function (e) {
      e.preventDefault();
      clearErrors();
      let hasError = false;

      // 🔸 Перевірка Email
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

      // Якщо все добре — відправка форми
      if (!hasError) {
          form.submit();
      }
  });
});
