import pandas
import numpy
from boto3.dynamodb.conditions import Key
from matplotlib import pyplot
from statsmodels.tsa.statespace.sarimax import SARIMAX
import io
import boto3
import matplotlib.image as mpimg
# Calculate MAPE (mean absolute percentage error)
# @param1   actual value
# @param2   predicted value
# @return   mean absolute percentage error between actual and predicted
def mape(actual, predicted):
    return numpy.mean(numpy.abs((actual - predicted) / actual)) * 100

#Configure source of data and length of forecast
forecast_length = 7
source_file = 'clean_spanish_data.txt'

#Read in data
data = pandas.read_csv(source_file, usecols = [0])
data.columns = ["Views"]
data = data['Views']

#Split into training and test sets
train_size = int(len(data) * 0.94)
#Spanish set has less samples

test_size = len(data) - train_size
train, test = data[0:train_size], data[train_size:len(data)]

#Initialize empty arrays to store the predictions errors
errors = []
predictions = []
#Number of days into future to forecast at a time

#Train the model and make predictions
for i in range(len(test) - forecast_length + 1):
    print(i)
    #Configure the model - SARIMA(1,0,1)x(1,1,1)7
    model = SARIMAX(train, order=(1, 0, 1), seasonal_order=(1, 1, 1, 7), enforce_stationarity=False,
                    enforce_invertibility=False, trend='n')
    #Train the model
    model_fit = model.fit(disp=False, maxiter=100)

    #Make 1 prediction of the specified forecast length
    forecast = model_fit.predict(start = len(train), end = len(train) + (forecast_length-1), dynamic = True)

    #Print error and add it to out array of errors
    error = mape(forecast, test[i:i+forecast_length])
    print(error)
    errors.append(error)
    # Add the forecast to array of forecasts
    predictions.append(list(forecast))
    #Add the period we just predicted to the training set for the next period
    new_train = test[i:i+1]
    train = numpy.append(train, new_train)

#Print the average error
print("Average Error:", sum(errors)/len(errors))

testy = []
for index, value in test.items():
    testy.append(value)

#get predictions in a plottable form
predictions = pandas.DataFrame(predictions).values

pp = []
for i in range(len(predictions[0])-1):
    pp.append(predictions[0][i])
for i in range(len(predictions)):
    pp.append(predictions[i][-1])


model = SARIMAX(data, order=(1, 0, 1), seasonal_order=(1, 1, 1, 7), enforce_stationarity=False,
                    enforce_invertibility=False, trend='n')
model_fit = model.fit(disp=False, maxiter=100)
derp = model_fit.predict(start = len(data), end = len(data) + (forecast_length-1), dynamic = True)
derp = list(derp)
d = []

for i in range(len(testy)-1):
    d.append(numpy.nan)

d.append(testy[-1])

for i in range(len(derp)):
    d.append(derp[i])

d = pandas.DataFrame(d).values


pyplot.plot(predictions, color='blue')
pyplot.plot(testy, color='red')
pyplot.plot(pp, color = 'blue')
pyplot.plot(d, color='green')
img_data = io.BytesIO()
pyplot.savefig(img_data, format='png')
img_data.seek(0)

s3 = boto3.client('s3')
s3.upload_fileobj(img_data, 'sjsu-cmpe172-scry', 'test.png')
pyplot.show()

resource = boto3.resource('s3')
bucket = resource.Bucket('sjsu-cmpe172-scry')

image_object = bucket.Object('test.png')
image = mpimg.imread(io.BytesIO(image_object.get()['Body'].read()), 'png')

pyplot.figure(0)
pyplot.imshow(image)
pyplot.show()