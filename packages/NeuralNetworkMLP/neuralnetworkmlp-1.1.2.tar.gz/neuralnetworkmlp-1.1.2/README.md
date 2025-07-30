# MLP Neural Network

MLP Neural Network is a lightweight Python library for building and training Multi-Layer Perceptron (MLP) models. This repository provides a simple yet powerful framework for experimenting with neural networks, along with an example program and dataset to help you get started quickly.

## Features

* Simple API: Quickly build and train neural network models with a few lines of code.
* Customizable Architecture: Easily configure the number of layers, neurons per layer, activation functions,  learning rates, epochs, batch size and threshold.
* Example Program: The included "test.py" script demonstrates how to integrate and use the library in a real-world scenario.
* Sample Dataset: Comes with an iris.csv file containing the famous Iris dataset, ideal for testing and learning.

## Getting Started

### Requirements

* Python 3.x is required.
* NumPy library is required.
* Pandas library is required.
* Matplotlib library is required.
* Json (built-in) library is required.

Install NumPy python library by using the below.
```
pip install numpy
pip install pandas
pip install matplotlib
```

## Installation

Clone the repository to your local machine:
```
git clone https://github.com/ThePhantom2307/MLP-Neural-Network.git
cd MLP-Neural-Network
```

Or you can use the built-in function pip
```
pip install NeuralNetworkMLP
```

## Running the Example
The repository includes an example script (test.py) that shows how to use the library. The script loads the provided iris.csv dataset, builds an MLP model, trains it, and evaluates its performance. To run the example, simply execute:

```python
python test.py
```
## Usage
You can incorporate the MLP Neural Network library into your own projects. Below is a short example to illustrate how to use the library:

```python
import NeuralNetworkMLP as nn
import numpy as np

# Load or create the datasets
xTrain = np.array([[0, 1],
                   [1, 0],
                   [1, 1],
                   [0, 0]])

yTrain = np.array([[1], [1], [0], [0]])

xTest = np.array([[1, 0]])

# Define your network architecture: for example, input layer of size 2, one hidden layer with 10 neurons, and output layer of size 1.
neuralNetwork = nn.NeuralNetwork(
    inputLayerNeurons=2,
    hiddenLayersNeurons=[10],
    outputLayerNeurons=1,
    activationFunctions=[nn.RELU, nn.SIGMOID]
)

# Train the model on your training data
neuralNetwork.train(xTrain, yTrain)

# Predict on new data
predictions = neuralNetwork.predict(xTest)

# Save the model
neuralNetwork.saveModel("NeuralNetworkModel.json")

# Load the model
neuralNetwork.loadModel("NeuralNetworkModel.json")
```
For more detailed usage, refer to the "test.py" file, which provides a complete example.

## Contributing
Contributions, suggestions, and bug reports are welcome! If you’d like to contribute, please fork the repository and create a pull request. Alternatively, feel free to open an issue to discuss improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
