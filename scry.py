from models import User, Tweet, InvalidToken,getUser, getUsers, addUser, removeUser, getTweets, getUserTweets, addTweet, delTweet, getRequest, Request, Data, addData, getData, delData, addRequest, delRequest, getUserRequest
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
import re
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, \
    jwt_refresh_token_required, create_refresh_token, get_raw_jwt
from models import db


app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://admin:Cascade5995$$$@cmpe172.cxubifgi6ctr.us-west-1.rds.amazonaws.com:3306/bank'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "SJSU/CMPE172/Scry"
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
db.app = app
db.init_app(app)
jwt = JWTManager(app)
CORS(app)


@jwt.token_in_blacklist_loader
def check_if_blacklisted_token(decrypted):
    jti = decrypted["jti"]
    return InvalidToken.is_invalid(jti)


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
    print(getUsers())
    try:
        email = request.json["email"]
        email = email.lower()
        password = request.json["pwd"]
        username = request.json["username"]
        if not (email and password and username):
            return jsonify({"error": "Must please fill out all fields"})
        # Check to see if user already exists
        users = getUsers()
        if (len(list(filter(lambda x: x["email"] == email, users))) == 1):
            return jsonify({"error": "That username is already in use"})
        # Email validation check
        if not re.match(r"[\w\._]{5,}@\w{3,}.\w{2,4}", email):
            return jsonify({"error": "Invalid e-mail address"})
        addUser(username, email, password)
        return jsonify({"success": True})
    except Exception as e:
        print(e)
        return jsonify({"error": "Invalid form"})


@app.route("/api/forecast")
@jwt_required
def forecast():
    print("HELL0")
    uid = get_jwt_identity()
    print("uid:")
    print(uid)
    req = getRequest()
    print(req)
    return jsonify({"success": True})


@app.route("/api/checkiftokenexpire", methods=["POST"])
@jwt_required
def check_if_token_expire():
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
#@jwt_required
def get_tweets():
    return jsonify(getTweets())


@app.route("/api/addtweet", methods=["POST"])
@jwt_required
def add_tweet():
    # db.create_all()
    try:
        title = request.json["title"]
        content = request.json["content"]
        if not (title and content):
            return jsonify({"error": "All fields are mandatory"})
        uid = get_jwt_identity()
        addTweet(title, content, uid)
        return jsonify({"success": "true"})
    except Exception as e:
        print(e)
        return jsonify({"error": "Invalid form"})


@app.route("/api/deletetweet/<tid>", methods=["DELETE"])
@jwt_required
def delete_tweet(tid):
    try:
        print(tid)
        delTweet(tid)
        return jsonify({"success": "true"})
    except:
        return jsonify({"error": "Invalid form"})


@app.route("/api/getcurrentuser")
@jwt_required
def get_current_user():
    uid = get_jwt_identity()
    return jsonify(getUser(uid))


@app.route("/api/changepassword", methods=["POST"])
@jwt_required
def change_password():
    try:
        user = User.query.get(get_jwt_identity())
        if not (request.json["password"] and request.json["npassword"]):
            return jsonify({"error": "Invalid form"})
        if not user.pwd == request.json["password"]:
            return jsonify({"error": "Wrong password"})
        user.pwd = request.json["npassword"]
        db.session.add(user)
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        print(e)
        return jsonify({"error": "Invalid form"})


@app.route("/api/deleteaccount", methods=["DELETE"])
@jwt_required
def delete_account():
    try:
        user = User.query.get(get_jwt_identity())
        tweets = Tweet.query.all()
        for tweet in tweets:
            if tweet.user.username == user.username:
                delTweet(tweet.id)
        removeUser(user.id)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)})
####################################


# APP###########################
if __name__ == "__main__":
    app.run(debug=True)
################################
