from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class ProductsDB(db.Model):
    __tablename__ = 'productsdb'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    product = db.relationship('OrdersDB', backref='product')

    def __repr__(self):
        return '<ProductsDB %r>' % self.name


class CostumersDB(db.Model):
    __tablename__ = 'costumersdb'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.Integer, nullable=False)
    costumer = db.relationship('OrdersDB', backref='costumer')

    def __repr__(self):
        return '<CostumersDB %r>' % self.name


class OrdersDB(db.Model):
    __tablename__ = 'orderdb'
    id = db.Column(db.Integer, primary_key=True)
    costumer_id = db.Column(db.Integer, db.ForeignKey('costumersdb.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('productsdb.id'))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    number = db.Column(db.Integer, default=1)

    def __repr__(self):
        return '<OrdersDB %r>' % self.id


# Принять id текущего пользователя
costumer_id = 1


@app.route("/", methods=['POST', 'GET'])
@app.route("/home", methods=['POST', 'GET'])
def index():
    global costumer_id
    # Создаём список со всеми товарами из базы,
    # для вывода на главную
    products = ProductsDB.query.order_by(ProductsDB.id.desc()).all()
    if request.method == "POST":
        product_id = int(request.form['product_id'])

        orders = OrdersDB.query.filter_by(costumer_id=costumer_id).all()
        for i in orders:
            if i.product_id == product_id:
                i.number += 1
                try:
                    db.session.commit()
                    return render_template("index.html", products=products)
                except:
                    return "Add fault!"

        order = OrdersDB(costumer_id=costumer_id, product_id=product_id)
        try:
            db.session.add(order)
            db.session.commit()
            return render_template("index.html", products=products)
        except:
            return "Add fault!"
    else:
        return render_template("index.html", products=products)


@app.route("/about")
def about():
    return render_template("about.html", costumer_id=costumer_id)


@app.route("/basket")
def basket():
    orders = OrdersDB.query.filter_by(costumer_id=costumer_id).all()
    products = []
    for i in orders:
        products.append(ProductsDB.query.filter_by(id=i.product_id).first())
    return render_template("basket.html", products=products, orders=orders)


@app.route("/add-product", methods=['POST', 'GET'])
def add_product():
    if request.method == "POST":
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']

        product = ProductsDB(name=name, price=price, description=description)

        try:
            db.session.add(product)
            db.session.commit()
            return redirect('/home')
        except:
            return "Add fault!"
    else:
        return render_template("add-product.html")


@app.route("/reg", methods=['POST', 'GET'])
def reg():
    if request.method == "POST":
        name = request.form['name']
        password = request.form['password']

        user = CostumersDB(name=name, password=password)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/home')
        except:
            return "Registration fault!"
    else:
        return render_template("reg.html")


if __name__ == "__main__":
    app.run(debug=True)
