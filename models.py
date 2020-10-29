from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship('User', foreign_keys=uid)
    datasetid = db.Column(db.Integer)
    length = db.Column(db.Integer)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship('User', foreign_keys=uid)
    productName = db.Column(db.String(256))
    description = db.Column(db.String(2048))
    s3key = db.Column(db.String(256))
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
    try:
        user = User(username, email, pwd)
        db.session.add(user)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
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


def getUserRequest(uid):
    requests = Request.query.filter_by(uid= uid).order_by(Request.id.desc()).all()
    request = list(requests)[0]
    return {"id": request.id, "uid": request.uid, "user": getUser(request.uid), "DatasetID":request.datasetid, "length":request.length}


def getData():
    datasets = Data.query.all()
    return[{"id": i.id, "uid": i.uid, "user": getUser(i.uid), "ProductName": i.productName, "Description": i.description, "S3Key":i.s3key} for i in datasets]

def getTweets():
    tweets = Tweet.query.all()
    return [{"id": i.id, "title": i.title, "content": i.content, "user": getUser(i.uid)} for i in tweets]


def getUserTweets(uid):
    tweets = Tweet.query.all()
    return [{"id": item.id, "userid": item.user_id, "title": item.title, "content": item.content} for item in
            filter(lambda i: i.user_id == uid, tweets)]


def addTweet(title, content, uid):
    try:
        user = list(filter(lambda i: i.id == uid, User.query.all()))[0]
        twt = Tweet(title=title, content=content, user=user)
        db.session.add(twt)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def addData(productName, description, s3key, uid):
    try:
        user = list(filter(lambda i: i.id == uid, User.query.all()))[0]
        dataset = Data(user=user, productName=productName, description=description, s3key=s3key,)
        db.session.add(dataset)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def addRequest(uid, did, length):
    try:
        user = list(filter(lambda i: i.id == uid, User.query.all()))[0]
        request = Request(user=user, datasetid=did, length=length)
        db.session.add(request)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False


def delTweet(tid):
    try:
        tweet = Tweet.query.get(tid)
        print("del tweet")
        db.session.delete(tweet)
        db.session.commit()
        print("comitted")
        return True
    except Exception as e:
        print(e)
        return False

def delData(did):
    try:
        data = Data.query.get(did)
        db.session.delete(data)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def getDataset(did):
    data = Data.query.get(did)
    return{"id": data.id, "uid": data.uid, "user": getUser(data.uid), "ProductName": data.productName, "Description": data.description, "S3Key":data.s3key}


def delRequest(rid):
    try:
        request = Request.query.get(rid)
        db.session.delete(request)
        db.session.commit()
        print("Successfully deleted request")
        return True
    except Exception as e:
        print("delete request failed")
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
