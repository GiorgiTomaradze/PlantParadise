from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config["SECRET_KEY"]= "Z7$gT4p&xK2@vN3#rH!wL8Qf"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Plantparadise.db"


db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'