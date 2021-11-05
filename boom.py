# imports
import sys

import numpy as np
import pandas
import pandas as pd
from sklearn import preprocessing, __all__, model_selection


class Layer:
    def __init__(self):
        self.input = None
        self.output = None

    # computes the output Y of a layer for a given input X
    def forward_pass(self, input):
        raise NotImplementedError

    # computes dE/dX for a given dE/dY (and update parameters if any)
    def backward_pass(self, output_error, learning_rate):
        raise NotImplementedError


# inherit from base class Layer
class FCLayer(Layer):
    # input_size = number of input neurons
    # output_size = number of output neurons
    def __init__(self, input_size, output_size):
        self.weights = np.random.rand(input_size, output_size) - 0.5
        self.bias = np.random.rand(1, output_size) - 0.5

    # returns output for a given input
    def forward_pass(self, input_data):
        self.input = input_data
        self.output = np.dot(self.input, self.weights) + self.bias
        return self.output

    # computes dE/dW, dE/dB for a given output_error=dE/dY. Returns input_error=dE/dX.
    def backward_pass(self, output_error, learning_rate):
        input_error = np.dot(output_error, self.weights.T)
        weights_error = np.dot(self.input.T, output_error)
        # dBias = output_error

        # update parameters
        self.weights -= learning_rate * weights_error
        self.bias -= learning_rate * output_error
        return input_error


class ActivationLayer(Layer):
    def __init__(self, activation, activation_prime):
        self.activation = activation
        self.activation_prime = activation_prime

    # returns the activated input
    def forward_pass(self, input_data):
        self.input = input_data
        self.output = self.activation(self.input)
        return self.output

    # Returns input_error=dE/dX for a given output_error=dE/dY.
    # learning_rate is not used because there is no "learnable" parameters.
    def backward_pass(self, output_error, learning_rate):
        return self.activation_prime(self.input) * output_error


# activation function and its derivative

def sigmoid(x):
    return 1.0 / (1 + np.exp(-x))


def sigmoid_derivative(x):
    return x * (1.0 - x)


def tanh(x):
    return np.tanh(x)


def tanh_derivative(x):
    return 1 - np.tanh(x) ** 2


# loss function and its derivative
def mean_square_error(y_true, y_pred):
    return np.mean(np.power(y_true - y_pred, 2))


def mean_square_error_derivative(y_true, y_pred):
    return 2 * (y_pred - y_true) / y_true.size


# loss function and its derivative
def mean_absolute_error(y_true, y_pred):
    return np.mean(y_true - y_pred)


def mean_absolute_error_derivative(y_true, y_pred):
    if y_pred > y_true:
        result = 1
    else:
        result = -1
    return result


class Network:
    def __init__(self):
        self.layers = []
        self.loss = None
        self.loss_derivative = None

    # add layer to network
    def add(self, layer):
        self.layers.append(layer)

    # set loss to use
    def use(self, loss, loss_derivative):
        self.loss = loss
        self.loss_derivative = loss_derivative

    # predict output for given input
    def predict(self, input_data):
        # sample dimension first
        samples = len(input_data)
        result = []

        # run network over all samples
        for i in range(samples):
            # forward propagation
            output = input_data[i]
            for layer in self.layers:
                output = layer.forward_pass(output)
            result.append(output)

        return result

    # train the network
    def fit(self, X_train, y_train, epochs, learning_rate):
        # sample dimension first
        samples = len(X_train)

        # training loop
        for i in range(epochs):
            err = 0
            for j in range(samples):
                # forward propagation
                output = X_train[j]
                for layer in self.layers:
                    output = layer.forward_pass(output)
                # compute loss (for display purpose only)
                err += self.loss(y_train[j], output)

                # backward propagation
                error = self.loss_derivative(y_train[j], output)
                for layer in reversed(self.layers):
                    error = layer.backward_pass(error, learning_rate)

            # calculate average error on all samples
            err /= samples
            print("zoom")
            print('epoch %d/%d   error=%f' % (i + 1, epochs, err))


if __name__ == "__main__":

    if len(sys.argv) != 5:
        sys.exit(
            "Please give the required amount of arguments - <Dataset path>, <Activation function like sigmoid, "
            "tanh>, <No. of iterations>, <Learning Rate>")
    else:
        train = sys.argv[1]
        activation_cli = sys.argv[2]
        epoch = int(sys.argv[3])
        learn_rate = float(sys.argv[4])
        activation_functions = ["sigmoid", "relu", "tanh"]
        if activation_cli not in activation_functions:
            sys.exit("Activation function not found !")

    # training data
    print('Loading data from file ...')  # Now let's load the data
    dataset = pandas.read_csv(train)
    print('done \n')

    # Input Normalization
    normalized_data = preprocessing.normalize(dataset, axis=0)
    dt = pd.DataFrame(normalized_data)
    dt_length = len(dt.columns)

    X = dt.drop([dt_length - 1], axis=1)
    y = dt[dt_length - 1]

    # Split data into training and testing datasets

    test_pct = 0.20  # reserve 20% of the data points for testing performance
    seed = 42  # setting the seed allows for repeatability
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=test_pct, random_state=seed)
    print(X_train.shape, y_train.shape)
    print(X_test.shape, y_test.shape)

    X_train, X_test, y_train, y_test = X_train.to_numpy(), X_test.to_numpy(), y_train.to_numpy(), y_test.to_numpy()
    X_train = np.reshape(X_train, (X_train.shape[0], 1, dt_length - 1))
    y_train = np.reshape(y_train, (y_train.shape[0], 1, 1))
    X_test = np.reshape(X_test, (X_test.shape[0], 1, dt_length - 1))
    y_test = np.reshape(y_test, (y_test.shape[0], 1, 1))

    # network
    net = Network()
    net.add(FCLayer(11, 3))
    if activation_cli in ("sigmoid", "Sigmoid", "SIGMOID"):
        net.add(ActivationLayer(sigmoid, sigmoid_derivative))
    elif activation_cli in ("tanh", "Tanh", "TANH"):
        net.add(ActivationLayer(tanh, tanh_derivative))

    net.add(FCLayer(3, 1))
    if activation_cli in ("sigmoid", "Sigmoid", "SIGMOID"):
        net.add(ActivationLayer(sigmoid, sigmoid_derivative))
    elif activation_cli in ("tanh", "Tanh", "TANH"):
        net.add(ActivationLayer(tanh, tanh_derivative))

    # train
    net.use(mean_square_error, mean_square_error_derivative)
    net.fit(X_train, y_train, epochs=epoch, learning_rate=learn_rate)

    # test
    out = net.predict(X_test)
    print(out)
