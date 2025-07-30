import numpy as np
from NeuralNetworkMLP.Activations import reluActivation, reluDerivative, sigmoidActivation, sigmoidDerivative, tanhActivation, tanhDerivative, softmaxActivation, softmaxDerivative

class Layer:
    def __init__(self, inputSize, outputSize, activationType, weights=None, biases=None):
        """
        Initialize a layer.

        Args:
            inputSize (int): Number of inputs to this layer.
            outputSize (int): Number of neurons in this layer.
            activationType (str): Type of activation function ("relu", "sigmoid", or "tanh").
            weights (np.array, optional): Pre-initialized weight matrix of shape (inputSize, outputSize).
            biases (np.array, optional): Pre-initialized bias vector of shape (1, outputSize).

        Raises:
            ValueError: If only one of weights or biases is provided.
        """
        self.inputSize = inputSize
        self.outputSize = outputSize
        self.activationType = activationType.lower()

        if weights is None and biases is None:
            self.weights = np.random.rand(inputSize, outputSize) - 0.5
            self.biases = np.random.rand(1, outputSize) - 0.5
        elif weights is not None and biases is not None:
            self.weights = weights
            self.biases = biases
        else:
            raise ValueError("Either both weights and biases must be provided, or both must be None.")

    def activate(self, inputData):
        """
        Apply the activation function to the input x using the external activations module.

        Args:
            x (np.array): Input data.
        
        Returns:
            np.array: Activated output.
        """
        if self.activationType == "relu":
            return reluActivation(inputData)
        elif self.activationType == "sigmoid":
            return sigmoidActivation(inputData)
        elif self.activationType == "tanh":
            return tanhActivation(inputData)
        elif self.activationType == "softmax":
            return softmaxActivation(inputData)
        else:
            raise ValueError(f"Unsupported activation type: {self.activationType}")

    def activationDerivative(self, preActivatedData):
        """
        Compute the derivative of the activation function for the input x using the external module.

        Args:
            x (np.array): Input data (typically the pre-activation values).
        
        Returns:
            np.array: The derivative of the activation function.
        """
        if self.activationType == "relu":
            return reluDerivative(preActivatedData)
        elif self.activationType == "sigmoid":
            return sigmoidDerivative(preActivatedData)
        elif self.activationType == "tanh":
            return tanhDerivative(preActivatedData)
        elif self.activationType == "softmax":
            return softmaxDerivative(preActivatedData)
        else:
            raise ValueError(f"Unsupported activation type: {self.activationType}")

    def forward(self, inputs):
        """
        Perform a forward pass through the layer.

        Args:
            inputs (np.array): Input data of shape (n_samples, inputSize).
        
        Returns:
            np.array: Output after applying the layer's linear transformation and activation,
                      of shape (n_samples, outputSize).
        """
        self.inputs = inputs
        self.preActivation = np.dot(inputs, self.weights) + self.biases
        self.outputs = self.activate(self.preActivation)
        return self.outputs
