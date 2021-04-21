from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Products_DB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Products_DB %r>' %self.id


'''class CostumersDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<CostumersDB %r>' %self.id

'''
'''class OrdersDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    costumer_id = db.Column(db.Integer, db.ForeignKey('CostumersDB.id', ondelete='CASCADE'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('ProductsDB.id', ondelete='CASCADE'), nullable=False, index=True)
    date = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())

    def __repr__(self):
        return '<OrdersDB %r>' % self.id
'''

@app.route("/")
@app.route("/home")
def index():
    products = Products_DB.query.order_by(Products_DB.id).all()
    return render_template("index.html", products=products)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/basket")
def basket():

    return render_template("basket.html")


@app.route("/add-product", methods=['POST', 'GET'])
def add_product():
    if request.method == "POST":
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']

        product = Products_DB(name=name, price=price, description=description)

        try:
            db.session.add(product)
            db.session.commit()
            return redirect('/home')
        except:
            return "Add fault!"
    else:
        return render_template("add-product.html")


if __name__ == "__main__":
    app.run(debug=True)
