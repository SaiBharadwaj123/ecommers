from flask import Flask, render_template, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Sample product data
products = [
    {'id': 1, 'name': 'Laptop', 'description': 'A powerful laptop', 'price': 1000},
    {'id': 2, 'name': 'Smartphone', 'description': 'An Android smartphone', 'price': 500},
    {'id': 3, 'name': 'Headphones', 'description': 'Noise-cancelling headphones', 'price': 200}
]

orders = []

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/shop')
def index():
    return render_template('index.html', products=products)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        cart = session.get('cart', [])
        cart.append(product)
        session['cart'] = cart
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total = sum(item['price'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/checkout')
def checkout():
    cart_items = session.pop('cart', [])
    total = sum(item['price'] for item in cart_items)
    if cart_items:
        orders.append({
            'id': len(orders) + 1,
            'items': ', '.join(item['name'] for item in cart_items),
            'total': total,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    return render_template('checkout.html', total=total)

@app.route('/orders')
def view_orders():
    return render_template('orders.html', orders=orders)

if __name__ == '__main__':
    app.run(debug=True)
