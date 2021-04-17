from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
db = SQLAlchemy(app)


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Integer)

    def __repr__(self):
        return '<Products %r>' %self.id

@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")


@app.route("/user/<string:name>/<int:id>")
def user(name, id):
    return "Hi, " + name + ": " + str(id)

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
