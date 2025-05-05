
document.addEventListener('DOMContentLoaded', function() {
    // Custom checkbox functionality
    const checkboxes = document.querySelectorAll('.custom-checkbox');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('click', function() {
            this.classList.toggle('checked');
            
            if (this.id === 'selectAll') {
                const isChecked = this.classList.contains('checked');
                document.querySelectorAll('.custom-checkbox:not(#selectAll):not(#consentCheckbox)').forEach(cb => {
                    if (isChecked) {
                        cb.classList.add('checked');
                    } else {
                        cb.classList.remove('checked');
                    }
                });
            }
            
            updateSelectAllState();
        });
    });
    
    // Quantity input functionality
    const decreaseButtons = document.querySelectorAll('.quantity-decrease');
    const increaseButtons = document.querySelectorAll('.quantity-increase');
    const quantityInputs = document.querySelectorAll('.product-quantity');
    
    decreaseButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            const input = document.querySelector(`.product-quantity[data-product-id="${productId}"]`);
            if (parseInt(input.value) > 1) {
                input.value = parseInt(input.value) - 1;
            }
        });
    });
    
    increaseButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            const input = document.querySelector(`.product-quantity[data-product-id="${productId}"]`);
            input.value = parseInt(input.value) + 1;
        });
    });
    
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            if (parseInt(this.value) < 1 || isNaN(parseInt(this.value))) {
                this.value = 1;
            }
        });
    });
    
    // Empty cart button
    const emptyCartBtn = document.getElementById('emptyCartBtn');
    emptyCartBtn.addEventListener('click', function() {
        if (confirm('Вы уверены, что хотите очистить корзину?')) {
            return
        }
    });
    
    // Checkout button
    const checkoutBtn = document.getElementById('checkoutBtn');
    checkoutBtn.addEventListener('click', function() {
        const consentCheckbox = document.getElementById('consentCheckbox');
        if (!consentCheckbox.classList.contains('checked')) {
            alert('Пожалуйста, дайте согласие на обработку ваших персональных данных, чтобы продолжить.');
            return;
        }
        window.location.href = '/buy';
    });
    
    // Continue shopping button
    const continueShoppingBtn = document.getElementById('continueShoppingBtn');
    continueShoppingBtn.addEventListener('click', function() {
        window.location.href = '/';
    });
});
