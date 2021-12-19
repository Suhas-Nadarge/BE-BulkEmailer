from flask import Flask , request
from flask_cors import CORS , cross_origin 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os



app = Flask(__name__)



CORS(app)

#Config Secret key and database URI
# refrence : https://newbedev.com/where-do-i-get-a-secret-key-for-flask
app.config['SECRET_KEY'] = '5792b192471948d429ad8339f6416749'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# 'mysql://username:password@localhost/db_name'
db = SQLAlchemy(app)

# Configure mail service
# refrence: https://pythonhosted.org/Flask-Mail/
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_ID')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
app.config['MAIL_USERNAME'] = 'acereddy8053@gmail.com'
app.config['MAIL_PASSWORD'] = 'suhas3679'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'acereddy8053@gmail.com'
mail = Mail(app)

#for passswd hashing 
bcrypt = Bcrypt(app)

# to handle user login
login_manager = LoginManager(app)
# to tell where to check login view
login_manager.login_view = 'login'


from flaskapp import routes