document.addEventListener('DOMContentLoaded', function () {
    const cartToggle = document.getElementById('cart-toggle');
    const closeCart = document.getElementById('close-cart');
    const continueShoppingBtn = document.getElementById('continue-shopping'); 
    const cartSidebar = document.querySelector('.cart-sidebar');
    const overlay = document.querySelector('.overlay');


    function openCart() {
        cartSidebar.classList.add('open'); // Добавляем класс для показа корзины
        overlay.classList.add('open'); // Показываем подложку
        document.body.style.overflow = 'hidden'; // Блокируем прокрутку страницы
    }

    function closeCartFunc() {
        cartSidebar.classList.remove('open'); // Убираем класс для скрытия корзины
        overlay.classList.remove('open'); // Скрываем подложку
        document.body.style.overflow = ''; // Разрешаем прокрутку страницы
    }

    // Добавляем обработчики событий
    cartToggle.addEventListener('click', openCart);
    closeCart.addEventListener('click', closeCartFunc);

    if (continueShoppingBtn) {
        continueShoppingBtn.addEventListener('click', closeCartFunc);
    }

    overlay.addEventListener('click', closeCartFunc); // Закрытие по клику на подложку
});