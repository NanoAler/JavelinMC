from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import re
import telebot  # Импортируем telebot

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Настройка лимитера для ограничения количества запросов
limiter = Limiter(get_remote_address, app=app)

# Ключи reCAPTCHA (замените их на свои)
RECAPTCHA_SECRET_KEY = "key"
RECAPTCHA_SITE_KEY = "key"

# Токен Telegram-бота (замените на ваш токен)
TELEGRAM_BOT_TOKEN = "token"
# ID чата администратора (замените на ваш ID чата)
TELEGRAM_CHAT_ID = "chatid"

# Инициализация Telegram-бота
telegram_bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Список товаров
products = [
    {"id": 1, "name": "Купюра", "price": 1500, "description": "Основная валюта на нашем сервере. Используется для покупки модулей и патронов", "image": "5k_rub.jpg"},
    {"id": 2, "name": "Коробка", "price": 2000, "description": "Запакованая коробка. Используется для покупки техники и оружия", "image": "box.jpg"},
    {"id": 3, "name": "[Premium] SCAR-H", "price": 3000, "description": "Премиум оружие SCAR-H Урон 13,75 Скорострельность 600 выстрелов в минуту Кол-во патрон в магазине 31 Калибр .308", "image": "SCAR-H.jpg"},
    {"id": 4, "name": "[Premium] AA12", "price": 3000, "description": "Премиум оружие AA12 Урон 30 Скорострельность 336 выстрелов в минуту Кол-во патронов в магази 30 Калибр 12 Gauge", "image": "AA12.jpg"},
    {"id": 5, "name": "[Premium] Лазер", "price": 3000, "description": "Премиум обвес оружия. Обычный лазер улучшающий характеристики вашего оружия!", "image": "module.jpg"}
]

def validate_telegram(username):
    """Проверка формата Telegram username"""
    return re.fullmatch(r'^(?=.{5,32}$)[a-zA-Z0-9]+(_[a-zA-Z0-9]+)*$', username) is not None

@app.route('/')
def index():
    """Страница с товарами"""
    cart_items = session.get('cart', [])
    session['counter'] = len(cart_items)
    counter = session.get('counter', 0) 
    return render_template('index.html', products=products, counter=counter)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    """Добавление товара в корзину"""
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(product_id)
    session.modified = True
    session['counter'] = len(session['cart'])
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    """Страница корзины"""
    cart_items = session.get('cart', [])
    cart_details = []
    total_price = 0
    counter = session.get('counter', 0)

    for product_id in cart_items:
        product = next((p for p in products if p["id"] == product_id), None)
        if product:
            cart_details.append(product)
            total_price += product['price']

    return render_template('cart.html', cart=cart_details, total_price=total_price, counter=counter)

@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    """Удаление одного экземпляра товара из корзины"""
    if 'cart' in session and product_id in session['cart']:
        session['cart'].remove(product_id)  # Удаляем только один экземпляр
        session.modified = True
    session['counter'] = len(session.get('cart', []))
    return redirect(url_for('cart'))

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    """Очистка корзины"""
    session.pop('cart', None)
    session['counter'] = 0  
    return redirect(url_for('cart'))

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Страница подробного описания товара"""
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return "Товар не найден", 404
    return render_template('product_detail.html', product=product)

@app.route('/buy', methods=['GET', 'POST'])
@limiter.limit("5 per 20 minutes")  # Лимит: 5 запросов с одного IP за 20 минут
def buy():
    """Страница покупки"""
    if request.method == 'POST':
        name = request.form['name']
        telegram = request.form['telegram']
        recaptcha_response = request.form['g-recaptcha-response']

        # Проверка reCAPTCHA
        import requests
        data = {
            'secret': RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data).json()
        if not response.get('success'):
            flash('Ты чё мудак капчу не прошел?', 'error')
            return render_template('buy.html', site_key=RECAPTCHA_SITE_KEY)

        # Проверка валидности данных
        if not name or not telegram:
            flash('Пожалуйста, заполните все поля.', 'error')
            return render_template('buy.html', site_key=RECAPTCHA_SITE_KEY)

        if not validate_telegram(telegram):
            flash('Неверное имя пользователя Telegram. Он должен начинаться с "@" и содержать только буквенно-цифровые символы.',
                  'error')
            return render_template('buy.html', site_key=RECAPTCHA_SITE_KEY)

        # Получаем содержимое корзины перед её очисткой
        cart_items = session.get('cart', [])
        if not cart_items:
            flash('Ваша корзина пуста. Пожалуйста, добавьте товары, прежде чем продолжить.', 'error')
            return redirect(url_for('cart'))

        # Отправляем данные в Telegram-чат
        send_order_to_telegram(name, telegram, cart_items)

        # Очищаем корзину после успешной покупки
        session.pop('cart', None)

        return f"Спасибо, {name}! Ваш заказ оформлен. Мы свяжемся с вами через Telegram: {telegram}"

    return render_template('buy.html', site_key=RECAPTCHA_SITE_KEY)

def send_order_to_telegram(name, telegram, cart_items):
    """Отправка данных о заказе в Telegram-чат"""
    try:
        # Формируем список товаров
        cart_details = []
        for product_id in cart_items:
            product = next((p for p in products if p["id"] == product_id), None)
            if product:
                cart_details.append(product)

        # Формируем сообщение
        message = f"Новый заказ:\n"
        message += f"Имя: {name}\n"
        message += f"Telegram: @{telegram}\n"
        message += "Список товаров:\n"
        for product in cart_details:
            message += f"- {product['name']} - {product['price']} руб.\n"

        # Отправляем сообщение в Telegram
        telegram_bot.send_message(TELEGRAM_CHAT_ID, message)
    except Exception as e:
        print(f"Ошибка при отправке сообщения в Telegram: {e}")

if __name__ == '__main__':
    app.run(debug=True)
