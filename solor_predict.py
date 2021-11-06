from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Bidirectional

from scipy.ndimage import gaussian_filter1d
from scipy.signal import medfilt

from numpy.random import seed
seed(1)
import tensorflow as tf
tf.random.set_seed(1)

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from numpy import array

font = {
    'family': 'Arial',
    'weight': 'normal',
    'size': 10
}
plt.rc('font', **font)

n_timestamp = 10
train_hours = 15000
test_hours = 500
n_eps = 25
filter_on = 0

#
# Select model type
# 1: Single cell
# 2: Stacked
# 3: Bidirectional
#
model_type = 2

url = "F://Excel//solar-hourly.csv"
dataset = pd.read_csv(url)
if filter_on == 1:
    dataset['energy'] = medfilt(dataset['energy'], 3)
    dataset['energy'] = gaussian_filter1d(dataset['energy'], 1.2)

train_set = dataset[0: train_hours].reset_index(drop=True)
test_set = dataset[train_hours: train_hours + test_hours].reset_index(drop=True)
training_set = train_set.iloc[:, 4: 5].values
testing_set = test_set.iloc[:, 4: 5].values

# normalize data
sc = MinMaxScaler(feature_range=(0, 1))
training_set_scaled = sc.fit_transform(training_set)
testing_set_scaled = sc.fit_transform(testing_set)

# split data
def data_split(seq, n_timestamp):
    x = []
    y = []
    for i in range(len(seq)):
        end_id = i + n_timestamp
        if end_id >= len(seq):
            break
        seq_x, seq_y = seq[i: end_id], seq[end_id]
        x.append(seq_x)
        y.append(seq_y)
    return array(x), array(y)

x_train, y_train = data_split(training_set_scaled, n_timestamp)
x_train = x_train.reshape(x_train.shape[0], x_train.shape[1], 1)
x_test, y_test = data_split(testing_set_scaled, n_timestamp)
x_test = x_test.reshape(x_test.shape[0], x_test.shape[1], 1)

if model_type == 1:
    model = Sequential()
    model.add(LSTM(units=50, activation='reulu', input_shape=(x_train.shape[1], 1)))
    model.add(Dense(units=1))
elif model_type == 2:
    model = Sequential()
    model.add(LSTM(50, activation='relu', return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(LSTM(50, activation='relu'))
    model.add(Dense(1))
elif model_type == 3:
    model = Sequential()
    model.add(Bidirectional(LSTM(50, activation='relu', return_sequences=True, input_shape=(x_train.shape[1], 1))))
    model.add(Dense(1))

# start training
model.compile(optimizer='adam', loss='mean_squared_error')
history = model.fit(x_train, y_train, epochs=n_eps, batch_size=32)
loss = history.history['loss']
eps = range(len(loss))

# get predicted data
y_predicted = model.predict(x_test)

# de-normalize the data'
y_predicted_descaled = sc.inverse_transform(y_predicted)
y_train_descaled = sc.inverse_transform(y_train)
y_test_descaled = sc.inverse_transform(y_test)
y_pred = y_predicted.ravel()
y_pred = [round(yx, 2) for yx in y_pred]
y_tested = y_test.ravel()

# show results
plt.figure(figsize=(8, 7))

plt.subplot(3, 1, 1)
plt.plot(dataset['energy'], color='black', linewidth=1, label='True value')
plt.ylabel('energy')
plt.xlabel('hour')
plt.title('All data')

plt.subplot(3, 2, 3)
plt.plot(y_test_descaled, color='black', linewidth=1, label='True value')
plt.plot(y_predicted_descaled, color='red', linewidth=1, label='Predicted')
plt.legend(frameon=False)
plt.ylabel('energy')
plt.xlabel('hour')
plt.title('Predicted data for n hours')

plt.subplot(3, 2, 4)
plt.plot(y_test_descaled[0: 75], color='black', linewidth=1, label='True value')
plt.plot(y_predicted_descaled[0: 75], color='red', linewidth=1, label='Predicted')
plt.legend(frameon=False)
plt.ylabel('energy')
plt.xlabel('hour')
plt.title('Predicted data for first 75 hours')

plt.subplot(3, 3, 7)
plt.plot(eps, loss, color='black')
plt.ylabel('Loss (MSE)')
plt.xlabel('Epoch')
plt.title('Training curve')

plt.subplot(3, 3, 8)
plt.plot(y_test_descaled - y_predicted_descaled, color='black')
plt.ylabel("Residual")
plt.xlabel("hour")
plt.title("Residual plot")

plt.subplot(3, 3, 9)
plt.scatter(y_predicted_descaled, y_test_descaled, s=2, color='black')
plt.ylabel('Y true')
plt.xlabel('Y predicted')
plt.title('Scatter plot')

plt.subplots_adjust(hspace = 0.5, wspace=0.3)
plt.show()

mse = mean_squared_error(y_test_descaled, y_predicted_descaled)
r2 = r2_score(y_test_descaled, y_predicted_descaled)
print("mse=" + str(round(mse, 2)))
print("r2=" + str(round(r2, 2)))