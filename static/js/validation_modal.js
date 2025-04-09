document.addEventListener('DOMContentLoaded', function () {
  const form = document.querySelector('#addItemModal form');
  const itemNameInput = document.getElementById('item_name');
  const damageInput = document.getElementById('damage');
  const fireRateInput = document.getElementById('fire_rate');

  // Функція для створення блоку повідомлень про помилки
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

  // Очищення помилок
  function clearErrors() {
      const errors = document.querySelectorAll('.error-message');
      errors.forEach(error => error.remove());
  }

  form.addEventListener('submit', function (e) {
      e.preventDefault(); // Забороняємо відправку форми, якщо є помилки
      clearErrors(); // Очищуємо попередні помилки

      let hasError = false;

      // Перевірка Item Name
      const itemNameValue = itemNameInput.value.trim();
      const itemNameRegex = /^[a-zA-Z0-9]{1,}[a-zA-Z0-9\s]{0,14}$/; // Літери, цифри, максимум 1 пробіл, до 15 символів
      const spaceCount = (itemNameValue.match(/\s/g) || []).length;
      if (!itemNameValue) {
          showError(itemNameInput, 'Назва обов’язкова для заповнення.');
          hasError = true;
      } else if (!itemNameRegex.test(itemNameValue) || spaceCount > 1) {
          showError(itemNameInput, 'Назва повинна містити лише букви, цифри, максимум 1 пробіл і до 15 символів.');
          hasError = true;
      }

      // Перевірка Damage
      const damageValue = damageInput.value.trim();
      const damageRegex = /^\d{1,15}$/; // До 15 цифр
      if (!damageValue) {
          showError(damageInput, 'Шкода обов’язкова для заповнення.');
          hasError = true;
      } else if (!damageRegex.test(damageValue)) {
          showError(damageInput, 'Шкода повинна бути числом до 15 цифр.');
          hasError = true;
      }

      // Перевірка Fire Rate
      const fireRateValue = fireRateInput.value.trim();
      const fireRateRegex = /^\d{1,8}$/; // До 8 цифр
      if (!fireRateValue) {
          showError(fireRateInput, 'Пострілів в секунду обов’язкове для заповнення.');
          hasError = true;
      } else if (!fireRateRegex.test(fireRateValue)) {
          showError(fireRateInput, 'Пострілів в секунду повинно бути числом до 8 цифр.');
          hasError = true;
      }

      // Якщо помилок немає, відправляємо форму
      if (!hasError) {
          form.submit();
      }
  });
});
