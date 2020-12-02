from models import User, InvalidToken, getUser, getUsers, addUser, removeUser, \
    Data, addData, getData, delData, \
    getDataset
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
import re
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, \
    jwt_refresh_token_required, create_refresh_token, get_raw_jwt
from models import db
import io
import boto3
from boto3.dynamodb.conditions import Key
import pandas
import numpy
import pymysql
from matplotlib import pyplot
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib
matplotlib.use("Agg")

app = Flask(__name__, static_folder="build", static_url_path="/")
app.config[
    "SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://admin:Cascade5995$$$@cmpe172.cxubifgi6ctr.us-west-1.rds.amazonaws.com:3306/bank'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "SJSU/CMPE172/Scry"
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
app.config['DEBUG'] = True
db.app = app
db.init_app(app)
jwt = JWTManager(app)
CORS(app)


def mape(actual, predicted):
    return numpy.mean(numpy.abs((actual - predicted) / actual)) * 100


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
    did = int(request.args['id'])
    print(did)
    forecast_length = int(request.args['length'])
    uid = get_jwt_identity()
    dataset = getDataset(did)
    key = dataset["S3Key"]

    s3_client = boto3.client('s3', aws_access_key_id="AKIAJ5ZHSDMMRPXMYRJQ",
                             aws_secret_access_key="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")

    response = s3_client.get_object(Bucket="sjsu-cmpe172-scry", Key=key)
    file = response["Body"].read()
    data = pandas.read_csv(io.BytesIO(file), usecols=[0])

    username = getUser(uid)["username"]
    productname = getDataset(did)["ProductName"]
    graphkey = username + productname + ".png"

    data.columns = ["Views"]
    data = data['Views']

    # Split into training and test sets
    train_size = int(len(data) * 0.94)
    test_size = len(data) - train_size
    train, test = data[0:train_size], data[train_size:len(data)]

    # Initialize empty arrays to store the predictions errors
    errors = []
    predictions = []
    # Train the model and make predictions
    for i in range(len(test) - forecast_length + 1):
        print(i)
        # Configure the model - SARIMA(1,0,1)x(1,1,1)7
        model = SARIMAX(train, order=(1, 0, 1), seasonal_order=(1, 1, 1, 7), enforce_stationarity=False,
                        enforce_invertibility=False, trend='n')
        # Train the model
        model_fit = model.fit(disp=False, maxiter=100)

        # Make 1 prediction of the specified forecast length
        forecast = model_fit.predict(start=len(train), end=len(train) + (forecast_length - 1), dynamic=True)

        # Print error and add it to out array of errors
        error = mape(forecast, test[i:i + forecast_length])
        print(error)
        errors.append(error)
        # Add the forecast to array of forecasts
        predictions.append(list(forecast))
        # Add the period we just predicted to the training set for the next period
        new_train = test[i:i + 1]
        train = numpy.append(train, new_train)

    # Print the average error
    print("Average Error:", sum(errors) / len(errors))

    testy = []
    for index, value in test.items():
        testy.append(value)

    # get predictions in a plottable form
    predictions = pandas.DataFrame(predictions).values

    pp = []
    for i in range(len(predictions) - 1):
        pp.append(predictions[i][0])
    for i in range(len(predictions[0])):
        pp.append(predictions[-1][i])

    model = SARIMAX(data, order=(1, 0, 1), seasonal_order=(1, 1, 1, 7), enforce_stationarity=False,
                    enforce_invertibility=False, trend='n')
    model_fit = model.fit(disp=False, maxiter=100)
    derp = model_fit.predict(start=len(data), end=len(data) + (forecast_length - 1), dynamic=True)
    derp = list(derp)
    d = []

    for i in range(len(testy) - 1):
        d.append(numpy.nan)

    d.append(testy[-1])

    for i in range(len(derp)):
        d.append(derp[i])

    d = pandas.DataFrame(d).values

    print("Prediction done! creating plot")

    pyplot.plot(testy, color='red', label='Actual History')
    pyplot.plot(pp, color='blue', label='Validation')
    pyplot.plot(d, color='green', label="Forecast")
    pyplot.legend(loc="upper left")
    img_data = io.BytesIO()
    pyplot.savefig(img_data, format='png')
    img_data.seek(0)
    s3_client.upload_fileobj(img_data, 'sjsu-cmpe172-scry', graphkey)
    #use string dataset+user.png as a convention
    response2 = s3_client.generate_presigned_url('get_object',
                                                 Params={'Bucket': 'sjsu-cmpe172-scry',
                                                         'Key': graphkey},
                                                 ExpiresIn=7200)
    pyplot.clf()
    fdict = {}
    fdict["success"] = response2
    fdict["Average Percentage Error"] = round(sum(errors) / len(errors), 2)
    stringy = "Period "
    vals = []

    for i in range(len(d)):
        if not numpy.isnan(numpy.float64(d[i][0])):
            vals.append(d[i][0])
    for i in range(1, len(vals)):
        fdict[stringy + str(i) + " forecast"] = int(vals[i])

    return jsonify(fdict)


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


@app.route("/api/products")
# @jwt_required
def get_products():
    return jsonify(getData())


@app.route("/api/deleteproduct/<pid>", methods=["DELETE"])
@jwt_required
def delete_product(pid):
    try:
        print(pid)
        delData(pid)
        return jsonify({"success": "true"})
    except:
        return jsonify({"error": "Invalid form"})


@app.route("/api/getcurrentuser")
@jwt_required
def get_current_user():
    uid = get_jwt_identity()
    return jsonify(getUser(uid))


@app.route("/api/addproduct", methods=["POST"])
@jwt_required
def add_product():
    try:
        f = request.files['image']
        dd = request.form["title"]
        ff = request.form['content']
        p = pandas.read_csv(f)
        print(p)
        uid = get_jwt_identity()
        current_user = getUser(uid)
        un = current_user['username']
        key = un + dd + ".txt"

        s3_client = boto3.client('s3', aws_access_key_id="AKIAJ5ZHSDMMRPXMYRJQ",
                                 aws_secret_access_key="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")
        csv_buf = io.StringIO()
        p.to_csv(csv_buf, index=False)
        csv_buf.seek(0)
        s3_client.put_object(Bucket='sjsu-cmpe172-scry', Body=csv_buf.getvalue(), Key=key)

        #s3_client.upload_fileobj(f, 'sjsu-cmpe172-scry', key)
        addData(dd, ff, key, uid)
        return jsonify({"success": "true"})
    except Exception as e:
        print(e)
        return jsonify({"error": "Invalid form"})

@app.route("/<a>")
def react_routes(a):
    return app.send_static_file("index.html")


@app.route("/")
def react_index():
    return app.send_static_file("index.html")


@app.route("/api/deleteaccount", methods=["DELETE"])
@jwt_required
def delete_account():
    try:
        user = User.query.get(get_jwt_identity())
        tweets = Data.query.all()
        for tweet in tweets:
            if tweet.user.username == user.username:
                delData(tweet.id)
        removeUser(user.id)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)})


####################################


# APP###########################
if __name__ == "__main__":
    app.run(host='0.0.0.0')
################################
