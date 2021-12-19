from flask_mail import Message, smtplib
from flaskapp import mail, db
from flaskapp.models import User_history
from flask_login import current_user
import os

# refrence : https://pythonhosted.org/Flask-Mail/
def send_email(subject,content,recipients,username):


    with mail.connect() as conn:
        for user in recipients:

            html_message = content
            subject = subject
            msg = Message(recipients=[user],
                        html=html_message,
                        subject=subject)


            user_history = User_history(username=username,recipient_email_id=user,subject=subject,content=html_message)

            try:
                conn.send(msg)
                user_history.status = 'Success'

            except smtplib.SMTPRecipientsRefused as e:
                pass
            finally:
                db.session.add(user_history)
                db.session.commit()