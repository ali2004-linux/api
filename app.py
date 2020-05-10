from flask import Flask,request,abort,jsonify
from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Integer,String
from werkzeug.security import check_password_hash,generate_password_hash

# config for app

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ali:@localhost/ali'
app.config["SECRET_KEY"] = "-/-+alianshirkhoda+@#*&@@#-*@12??<DKdmlfOERTH4oltfg"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "-/-+this_is_a_secret_+keyRTH4oltfg"
db.create_all()

# model for database

class User(db.Model):
    __tablename__ = "user"
    id = Column(Integer,primary_key=True,unique=True)
    username = Column(String(100),nullable=False,unique=True)
    password = Column(String(200),nullable=False)
    name = Column(String(180),nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check(self, password):
        return check_password_hash(self.password, password)
db.create_all()
#=======================================================
@app.route("/",methods=['POST','GET'])
def index():
    return abort(404)

@app.route("/l/v1/log/<token>",methods=["POST","GET"])
def log(token):
    if request.method == 'POST':
        if not str(token) == "ali2004h*+":
            return abort(404)
        else:
            if request.json:
                use = request.json[('username')]
                passw = request.json[('password')]
                name = request.json[('name')]
                if use and passw and name:
                    user = User.query.filter(User.username == use, User.name == name).first()
                    user_test = User.query.filter(User.username == use).first()
                    name_test = User.query.filter(User.name == name).first()
                    if not user_test:
                        return jsonify(message="Username NotFound!"),400
                    elif not name_test:
                        return json(message="Name NotFound"),400
                    elif not user.check(passw):
                        return jsonify(message="Password NotFound"),400
                    return jsonify(message=f"Login Successed! Welcome {use}"),200
                else:
                    return jsonify(message="i can't Fields Empty"),400
            else:
                use = request.form[('username')]
                passw = request.form[('password')]
                name = request.form [('name')]
                if use and passw and name:
                    user = User.query.filter(User.username == use, User.name == name).first()
                    user_test = User.query.filter(User.username == use).first()
                    name_test = User.query.filter(User.name == name).first()
                    if not user_test:
                        return jsonify(message="Username Not Found!"),400
                    elif not name_test:
                        return jsonify(message="Name NotFound!"),400
                    elif not user.check(passw):
                        return jsonify(message="password not"),400
                    return jsonify(message=f"Login Successed! Welcome {use}"),200
                else:
                    return jsonify(message="i can't Fields Empty"),400
    elif request.method == 'GET':
        return abort(404)
    else:
        return abort(404)

@app.route("/r/v1/reg/<token>",methods=["POST","GET"])
def ri(token):
    if request.method == 'POST':
        if not str(token) == "ali2004h*+-":
            return abort(404)
        else:
            if request.is_json:
                use = request.json[("username")]
                passw = request.json[("password")]
                name = request.json[("name")]
                if use and passw and name:
                    passw_ = generate_password_hash(passw)
                    new_user = User(username=use,password=passw_,name=name)
                    try:
                        db.session.add(new_user)
                        db.session.commit()
                        return jsonify(message="Register Successfuly :)",username=f"{use}"),200
                    except IntegrityError:
                        db.session.rollback()
                        return jsonify(message="UserName is Alerdy"),400
                else:
                    return jsonify(message="i can't Fields Empty"),400
            else:
                use = request.form[("username")]
                passw = request.form[("password")]
                name = request.form[("name")]
                if use and passw and name:
                    passw_ = generate_password_hash(passw)
                    new_user = User(username=use,password=passw_,name=name)
                    try:
                        db.session.add(new_user)
                        db.session.commit()
                        return jsonify(message="register Successfuly",username=f"{use}"),200
                    except IntegrityError:
                        db.session.rollback()
                        return jsonify(message="User is Alerdy"),400
                else:
                    return jsonify(message="i can't Fields Empty"),400
    elif request.method == 'GET':
        return abort(404)
    else:
        return abort(404)


if __name__ == '__main__':
    app.run("0.0.0.0",5000)

