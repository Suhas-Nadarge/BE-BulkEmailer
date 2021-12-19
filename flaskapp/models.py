from flaskapp import db,login_manager
# This will allow us to use is_authenticated , is_active ,ethods for current_user
from flask_login import UserMixin 
from datetime import datetime

# refrence for user login: https://flask-login.readthedocs.io/en/latest/

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    password = db.Column(db.String(60),nullable=False)

    def __repr__(self):
        return f"User('{self.username},{self.email}')"



class User_history(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(120),nullable=False)
    recipient_email_id = db.Column(db.String(120),nullable=False)
    subject = db.Column(db.String(200),nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(8),nullable=False,default = 'Failed')
    email_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    def __repr__(self):
        return f"User_history('{self.sender_email_id},{self.recipient_email_id},{self.subject},{self.status}')"