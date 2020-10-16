# IMPORTS######################################################################################
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
import re
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, \
    jwt_refresh_token_required, create_refresh_token, get_raw_jwt
###############################################################################################

# APP CONFIG####################################################################################
app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://admin:Cascade5995$$$@cmpe172.cxubifgi6ctr.us-west-1.rds.amazonaws.com:3306/bank'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "SJSU/CMPE172/Scry"
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]

jwt = JWTManager(app)
db = SQLAlchemy(app)
CORS(app)
################################################################################################


# DB CONFIG#####################################################################################


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24))
    email = db.Column(db.String(64))
    pwd = db.Column(db.String(64))

    # Constructor
    def __init__(self, username, email, pwd):
        self.username = username
        self.email = email
        self.pwd = pwd


class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship('User', foreign_keys=uid)
    title = db.Column(db.String(256))
    content = db.Column(db.String(2048))


##########################################################


# METHODS##############
def getUsers():
    users = User.query.all()
    return [{"id": i.id, "username": i.username, "email": i.email, "password": i.pwd} for i in users]


def getUser(uid):
    users = User.query.all()
    user = list(filter(lambda x: x.id == uid, users))[0]
    return {"id": user.id, "username": user.username, "email": user.email, "password": user.pwd}


def addUser(username, email, pwd):
    if username and pwd and email:
        try:
            user = User(username, email, pwd)
            db.session.add(user)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
    else:
        return False


def removeUser(uid):
    try:
        user = User.query.get(uid)
        db.session.delete(user)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False



def getTweets():
    tweets = Tweet.query.all()
    return [{"id": i.id, "title": i.title, "content": i.content, "user": getUser(i.uid)} for i in tweets]


def getUserTweets(uid):
    tweets = Tweet.query.all()
    return [{"id": item.id, "userid": item.user_id, "title": item.title, "content": item.content} for item in
            filter(lambda i: i.user_id == uid, tweets)]


def addTweet(title, content, uid):
    if title and content and uid:
        try:
            user = list(filter(lambda i: i.id == uid, User.query.all()))[0]
            twt = Tweet(title=title, content=content, user=user)
            db.session.add(twt)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
    else:
        return False


def delTweet(tid):
    try:
        tweet = Tweet.query.get(tid)
        db.session.delete(tweet)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

class InvalidToken(db.Model):
    __tablename__ = "invalid_tokens"
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(2048))

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_invalid(cls, jti):
        q = cls.query.filter_by(jti=jti).first()
        return bool(q)


@jwt.token_in_blacklist_loader
def check_if_blacklisted_token(decrypted):
    jti = decrypted["jti"]
    return InvalidToken.is_invalid(jti)
###############################################################

# ROUTES####################################
@app.route("/api/login", methods=["POST"])
def login():
    try:
        email = request.json["email"]
        password = request.json["pwd"]
        if email and password:
            user = list(filter(lambda x: x["email"] == email and x["password"] == password, getUsers()))
            if len(user) == 1:
                token = create_access_token(identity=user[0]["id"])
                refresh_token = create_refresh_token(identity=user[0]["id"])
                return jsonify({"token": token, "refreshToken": refresh_token})
            else:
                return jsonify({"error": "Invalid credentials"})
        else:
            return jsonify({"error": "Invalid form"})
    except Exception as e:
        print(e)
        return jsonify({"error": "Invalid form"})


@app.route("/api/register", methods=["POST"])
def register():
    # db.create_all()
    try:
        email = request.json["email"]
        email = email.lower()
        password = request.json["pwd"]
        username = request.json["username"]
        # Check to see if user already exists
        users = getUsers()
        if (len(list(filter(lambda x: x["email"] == email, users))) == 1):
            return jsonify({"error": "Invalid form1"})
        # Email validation check
        if not re.match(r"[\w\._]{5,}@\w{3,}.\w{2,4}", email):
            return jsonify({"error": "Invalid form2"})
        addUser(username, email, password)
        return jsonify({"success": True})
    except:
        return jsonify({"error": "Invalid form3"})


@app.route("/api/checkiftokenexpire", methods=["POST"])
@jwt_required
def check_if_token_expire():
    print(get_jwt_identity())
    return jsonify({"success": True})


@app.route("/api/refreshtoken", methods=["POST"])
@jwt_refresh_token_required
def refresh():
    identity = get_jwt_identity()
    token = create_access_token(identity=identity)
    return jsonify({"token": token})


@app.route("/api/logout/access", methods=["POST"])
@jwt_required
def access_logout():
    jti = get_raw_jwt()["jti"]
    try:
        invalid_token = InvalidToken(jti=jti)
        invalid_token.save()
        return jsonify({"success": True})
    except Exception as e:
        print(e)
        return {"error": e}


@app.route("/api/logout/refresh", methods=["POST"])
@jwt_required
def refresh_logout():
    jti = get_raw_jwt()["jti"]
    try:
        invalid_token = InvalidToken(jti=jti)
        invalid_token.save()
        return jsonify({"success": True})
    except Exception as e:
        print(e)
        return {"error": e}

@app.route("/api/tweets")
@jwt_required
def get_tweets():
    return jsonify(getTweets())


@app.route("/api/addtweet", methods=["POST"])
@jwt_required
def add_tweet():
    # db.create_all()
    try:
        title = request.json["title"]
        content = request.json["content"]
        uid = get_jwt_identity() # The line that changed
        addTweet(title, content, uid)
        return jsonify({"success": "true"})
    except Exception as e:
        print(e)
        return jsonify({"error": "Invalid form"})


@app.route("/api/deletetweet", methods=["DELETE"])
@jwt_required
def delete_tweet():
    try:
        tid = request.json["tid"]
        delTweet(tid)
        return jsonify({"success": "true"})
    except:
        return jsonify({"error": "Invalid form"})


####################################


# APP###########################
if __name__ == "__main__":
    app.run(debug=True)
################################
