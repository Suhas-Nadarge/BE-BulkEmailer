from flaskapp import app ,db ,bcrypt ,send_mail
from flask import request
from  flaskapp.models import User , User_history
from flask_login import login_user , current_user , logout_user , login_required
from flask_jsonpify import jsonify




@app.route("/")
def index():
    return jsonify({'text':'Home Page'}) 


@app.route("/register",methods=['GET','POST'])
def register():

    # get json data
    data = request.get_json()

    if request.method == 'POST':

        # check if user is already logged in
        if current_user.is_authenticated:
            return jsonify({'status':'fail','massage':'user is already logged in'}) , 404

        # extract user info
        username = data['username']
        email = data['email']
        password = data['password']
        
        #Get user from DB with same username
        user = User.query.filter_by(username=username).first()

        if user:
            return jsonify({'status': 'fail', 'message': 'User already registered.'}), 500
        
        # Get user from DB with same email
        user = User.query.filter_by(email=email).first()

        if user:
            return jsonify({'status': 'fail', 'message': 'User already registered.'}) ,500

        # hash password
        hashed_passwd = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create user object and save to DB
        user = User(username=username,email=email,password=hashed_passwd)
        db.session.add(user)
        db.session.commit()

        massage = f"User {username} successfully added " , 200

        return jsonify({'status': 'success', 'message': massage})

    return jsonify({'data':'something'}) , 500


@app.route("/login",methods=['POST'])
def login():
    

    data = request.get_json()

    # check if user is already logged in
    if current_user.is_authenticated:
            return jsonify({'status':'fail','massage':'user is already logged in'}) ,500
    
    username = data['username']
    password = data['password']
    
    # filter out user from log in username passed
    user = User.query.filter_by(username=data['username']).first()
    
    # check if user exists and password is correct
    if user and bcrypt.check_password_hash(user.password,password):
        # log in user
        login_user(user)
        massage = f"User {username} logged in "
        return jsonify({'status':'success','massage':massage}) ,200
    else:
        return jsonify({'status':'fail','massage':'something went wrong'}), 401

    return jsonify({'data':'something'})

@app.route("/logout",methods=['POST'])
def logout():
    # logout user
    logout_user()
    return  jsonify({'status':'success','massage':'logged out'})


@app.route("/send_email",methods=['GET','POST'])
# @login_required
def send_email():
    
    data = request.get_json()

    username = data['username']
    subject = data['subject']
    email_body = data['email_body']
    recipients = data['recipients'].split(',')

    # call function to send email
    send_mail.send_email(subject,email_body,recipients,username)

    massage = f"Send Email opreation done"

    return jsonify({'status': 'success', 'message': massage})





@app.route("/get_history",methods=['GET','POST'])
# @login_required
def get_history():

    data = request.get_json()
    username  = data['username']

    user_history = User_history.query.filter_by(username=username).all()

    #list of json
    list_of_json = []
    for row in user_history:
        user_dict = { 'id' : row.id,
                    'username': row.username,
                    'recipient_email_id': row.recipient_email_id,
                    'subject': row.subject,
                    'content':row.content,
                    'email_datetime':row.email_datetime,
                    'status': row.status
        }

        
        list_of_json.append(user_dict)
    

    return jsonify(list_of_json) , 200

    

@app.route("/delete_history",methods=['POST'])
# @login_required
def delete_history():

    data = request.get_json()

    is_all = data['is_all']


    if is_all: 
        try:
            num_rows_deleted = db.session.query(User_history).delete()
            db.session.commit()
            return jsonify({'status': 'success','massge': f"deleted {num_rows_deleted} row"}) , 200
        except:
            db.session.rollback()
            return jsonify({'status': 'failed','massage': "something went wrong"}) , 500
    else:

        id_to_delete = data['id']


        try:
            record_obj = User_history.query.filter_by(id=id_to_delete).first()
            db.session.delete(record_obj)
            db.session.commit()
            return jsonify({'status': 'success','massge': f"deleted row with id , {id_to_delete}"}) , 200
        except:
            db.session.rollback()
            return jsonify({'status': 'failed','massage': "something went wrong"}) , 500


        