import pandas
import numpy
from matplotlib import pyplot
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.statespace.sarimax import SARIMAX
import statsmodels.api as sm

# Calculate MAPE (mean absolute percentage error)
# @param1   actual value
# @param2   predicted value
# @return   mean absolute percentage error between actual and predicted
def mape(actual, predicted):
    return numpy.mean(numpy.abs((actual - predicted) / actual)) * 100

#Dickey Fuller test to test if series is stationary
def test_stationary(timeseries):
    print('Results of Dickey-Fuller Test:')
    stationary_test = adfuller(timeseries, autolag='AIC')
    output = pandas.Series(stationary_test[0:4], index=['Test Statistic', 'P-Value', 'Number of Lags', 'Number of Observations'])
    for key, value in stationary_test[4].items():
        output['Critical Value (%s)' % key] = value
    print(output)

#Configure source of data and length of forecast
forecast_length = 1
source_file = 'clean_spanish_data.txt'

#Read in data
data = pandas.read_csv(source_file, usecols = [0])
data.columns = ["Views"]
data = data['Views']

#OPTIONAL, used for seeing how many differences needed
#Test if the data is stationary
#test_stationary(data)

#OPTIONAL, used to find optimal models with auto-correlation, partial autocorrelation
#Check the autocorrelation and partial autocorrelations to determine parameters
#fig = pyplot.figure()
#ax1 = fig.add_subplot(211)
#fig = sm.graphics.tsa.plot_acf(data.iloc[8:], lags=30, ax=ax1)
#ax2 = fig.add_subplot(212)
#fig = sm.graphics.tsa.plot_pacf(data[8:], lags=30, ax=ax2)
#pyplot.show()

#Split into training and test sets
train_size = 650
#Spanish set has less samples
if source_file.__contains__("spanish"):
    train_size = 575
test_size = len(data) - train_size
train, test = data[0:train_size], data[train_size:len(data)]

#Initialize empty arrays to store the predictions errors
errors = []
predictions = []
#Number of days into future to forecast at a time

#Train the model and make predictions
for i in range(len(test) - forecast_length):
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

#get predictions in a plottable form
predictions = pandas.DataFrame(predictions).values

#Plot actual vs predicted
pyplot.plot(test.reset_index(), color = 'red')
pyplot.plot(predictions, color='blue')
pyplot.show()