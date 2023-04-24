from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]='mysql+pymysql://root:19982804@localhost:3306/invoice'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "59ceec65a970fa3b1a00830e53081eb6f565c272"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


with app.app_context():
    db.create_all()

with app.app_context():
    from routes.add import *


if __name__ == "__main__":
    app.run(debug=True)