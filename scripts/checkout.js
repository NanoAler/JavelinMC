document.addEventListener("DOMContentLoaded", function () {
    const checkoutBtn = document.getElementById("checkout-btn");
    const checkoutModal = document.getElementById("checkout-modal");
    const closeCheckoutModal = document.getElementById("close-checkout-modal");
    const checkoutForm = document.getElementById("checkout-form");

    checkoutBtn.addEventListener("click", function () {
      checkoutModal.classList.remove("hidden");
      document.body.style.overflow = "hidden";
    });

    closeCheckoutModal.addEventListener("click", function () {
      checkoutModal.classList.add("hidden");
      document.body.style.overflow = "";
    });

    checkoutForm.addEventListener("submit", function (e) {
      e.preventDefault();
      const name = document.getElementById("name").value;
      const telegram = document.getElementById("telegram").value;

      if (name && telegram) {
        checkoutModal.classList.add("hidden");
        document.body.style.overflow = "";

        const successModal = document.createElement("div");
        successModal.className =
          "fixed inset-0 bg-black bg-opacity-50 z-[60] flex items-center justify-center";
        successModal.innerHTML = `
          <div class="bg-white rounded-lg shadow-xl p-6 max-w-sm w-full mx-4">
            <div class="text-center">
              <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <i class="ri-check-line ri-2x text-green-500"></i>
              </div>
              <h3 class="text-xl font-bold text-gray-800 mb-2">Заказ успешно оформлен!</h3>
              <p class="text-gray-600 mb-6">Мы свяжемся с вами в Telegram в ближайшее время.</p>
              <button class="w-full py-3 bg-primary text-white font-medium rounded-button hover:bg-primary/90" onclick="this.parentElement.parentElement.parentElement.remove()">
                Закрыть
              </button>
            </div>
          </div>
        `;
        document.body.appendChild(successModal);
      }
    });
  });