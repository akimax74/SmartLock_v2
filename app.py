import uuid
from flask import Flask, request, jsonify, render_template
from servo import lock as servo_lock, unlock as servo_unlock
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

app = Flask(__name__)
engine = create_engine('sqlite:///db.User')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.User'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Session = sessionmaker(autocommit = False, autoflush = True, bind= engine)  

class User(db.Model):
    __tablename__ = 'user'
    token = db.Column(db.String(36), primary_key=True)  
    name = db.Column(db.String(128), nullable=False)

    def __init__(self, name):
        self.token = str(uuid.uuid4())  
        self.name = name

is_unlocked = True

@app.route("/", methods=['GET'])
def top():
    token = request.args['token']
    user = User.query.get(token)
    if user:
        return render_template('index.html', login_name=user.name, token=user.token)
    return "User not found", 404


@app.route("/lock", methods=['GET'])
def lock_route():
    global is_unlocked  
    token = request.args['token']
    print(token) 
    user = User.query.get(token)
    if user:
        is_unlocked = False
        servo_lock()
        print('lock')
        return "locked"
    return "User not found", 404

@app.route("/unlock", methods=['GET'])
def unlock_route():
    global is_unlocked  
    token = request.args['token']
    print(token)  
    user = User.query.get(token)
    if user:
        is_unlocked = True
        servo_unlock()
        print('unlock')
        return "unlocked"
    return "User not found", 404

@app.route("/add_user", methods=['POST'])
def add_user():
    if request.form['password'] == "Hoge123": #任意のパスワードを設定
        name = request.form['name']
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"token": new_user.token}), 201
    return "Unauthorized", 401

@app.route("/del_user", methods=['DELETE'])
def del_user():
    token = request.args['token']
    session = Session()  
    del_data = User.query.get(token)
    if del_data:
        db.session.delete(del_data)
        db.session.commit()
        db.session.close()
        return "User deleted", 200
    return "User not found", 404

@app.route("/users", methods=['GET'])
def get_users():
    token = request.args['token']
    if not token:
        return "Unauthorized", 401
    user = User.query.get(token)
    if not user:
        return "Unauthorized", 401
    users = User.query.all()
    users_list = [{"token": user.token, "name": user.name} for user in users]
    return jsonify(users_list)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=7200)
