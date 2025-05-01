from flask import Flask, render_template, redirect, url_for, request, flash
from datetime import datetime
from models import db, Product, Location, Movement
from forms import ProductForm, LocationForm, MovementForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e9b1c3d4e5f6a7b8c9d0e1f2a3b4c5d6'


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/inventory_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 280}

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(code=form.code.data, name=form.name.data)
        db.session.add(product)
        db.session.commit()
        flash('Product added!')
        return redirect(url_for('products'))
    return render_template('add_edit_product.html', form=form)

@app.route('/locations')
def locations():
    locations = Location.query.all()
    return render_template('locations.html', locations=locations)

@app.route('/locations/add', methods=['GET', 'POST'])
def add_location():
    form = LocationForm()
    if form.validate_on_submit():
        location = Location(code=form.code.data, name=form.name.data)
        db.session.add(location)
        db.session.commit()
        flash('Location added!')
        return redirect(url_for('locations'))
    return render_template('add_edit_location.html', form=form)

@app.route('/movements')
def movements():
    movements = Movement.query.order_by(Movement.timestamp.desc()).all()
    return render_template('movements.html', movements=movements)

@app.route('/movements/add', methods=['GET', 'POST'])
def add_movement():
    form = MovementForm()
    form.product_id.choices = [(p.id, p.name) for p in Product.query.all()]
    locations = Location.query.all()
    form.from_location_id.choices = [(-1, '---')] + [(l.id, l.name) for l in locations]
    form.to_location_id.choices = [(-1, '---')] + [(l.id, l.name) for l in locations]

    if form.validate_on_submit():
        from_location = form.from_location_id.data if form.from_location_id.data != -1 else None
        to_location = form.to_location_id.data if form.to_location_id.data != -1 else None
        movement = Movement(
            timestamp=datetime.now(),
            from_location_id=from_location,
            to_location_id=to_location,
            product_id=form.product_id.data,
            quantity=form.quantity.data
        )
        db.session.add(movement)
        db.session.commit()
        flash('Movement recorded!')
        return redirect(url_for('movements'))
    return render_template('add_edit_movement.html', form=form)

@app.route('/report')
def report():
    products = Product.query.all()
    locations = Location.query.all()
    report_data = []
    for product in products:
        for location in locations:
            in_count = db.session.query(db.func.sum(Movement.quantity)).filter(
                Movement.product_id == product.id,
                Movement.to_location_id == location.id
            ).scalar() or 0
            out_count = db.session.query(db.func.sum(Movement.quantity)).filter(
                Movement.product_id == product.id,
                Movement.from_location_id == location.id
            ).scalar() or 0
            quantity = in_count - out_count
            report_data.append({
                'product': product.name,
                'location': location.name,
                'quantity': quantity
            })
    return render_template('report.html', report_data=report_data)

if __name__ == '__main__':
    app.run(debug=True)
