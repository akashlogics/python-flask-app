from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('inventory.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database
def init_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS Product ...')
    conn.execute('CREATE TABLE IF NOT EXISTS Location ...')
    conn.execute('CREATE TABLE IF NOT EXISTS ProductMovement ...')
    conn.commit()
    conn.close()

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Product routes
@app.route('/products')
def view_products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM Product').fetchall()
    conn.close()
    return render_template('products.html', products=products)

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        # Extract form data and insert into database
        return redirect(url_for('view_products'))
    return render_template('add_product.html')

# Similar routes for edit/delete products, locations, movements

# Report route
@app.route('/report')
def report():
    conn = get_db_connection()
    report_data = conn.execute('SELECT p.name, l.name, ...').fetchall()
    conn.close()
    return render_template('report.html', report_data=report_data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

def init_db():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Product
                 (product_id TEXT PRIMARY KEY, name TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS Location
                 (location_id TEXT PRIMARY KEY, name TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS ProductMovement
                 (movement_id TEXT PRIMARY KEY, timestamp DATETIME,
                  from_location TEXT, to_location TEXT, product_id TEXT, qty INTEGER)''')
    conn.commit()
    conn.close()