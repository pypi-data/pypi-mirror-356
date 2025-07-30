import numpy as np
import json
from NeuralNetworkMLP.Layer import Layer
from NeuralNetworkMLP.Plot import errorPlotOverEpochs

TANH = "tanh"
RELU = "relu"
SIGMOID = "sigmoid"
SOFTMAX = "softmax"

class NeuralNetwork:
    """
    A neural network class that builds a multilayer perceptron using Layer objects.
    
    Example:
        >>> nn = NeuralNetwork(
        ...     inputLayerNeurons=2,
        ...     hiddenLayersNeurons=[3],
        ...     outputLayerNeurons=1,
        ...     activationFunctions=["relu", "sigmoid"]
        ... )
    """
    def __init__(self, inputLayerNeurons=None, hiddenLayersNeurons=None, outputLayerNeurons=None, 
                 activationFunctions=None, modelFile=None):
        """
        Initialize a NeuralNetwork instance either from parameters or from a saved model file.

        Args:
            inputLayerNeurons (int, optional): Number of neurons in the input layer.
            hiddenLayersNeurons (list, optional): List of neuron counts for each hidden layer.
            outputLayerNeurons (int, optional): Number of neurons in the output layer.
            activationFunctions (list, optional): List of activation functions for each layer.
                Its length must equal len(hiddenLayersNeurons) + 1.
            modelFile (str, optional): Path to a JSON file from which to load a saved model.

        Example:
            >>> nn = NeuralNetwork(2, [3], 1, ["relu", "sigmoid"])
        """
        if modelFile is not None:
            self.loadModel(modelFile)
        else:
            if (inputLayerNeurons is None or hiddenLayersNeurons is None or 
                outputLayerNeurons is None or activationFunctions is None):
                raise ValueError("All layer parameters and activation functions must be provided if not loading a model.")
            
            expectedActivations = len(hiddenLayersNeurons) + 1
            if len(activationFunctions) != expectedActivations:
                raise ValueError(f"Expected {expectedActivations} activation functions but got {len(activationFunctions)}.")
            
            self.inputLayerNeurons = inputLayerNeurons
            self.hiddenLayersNeurons = hiddenLayersNeurons
            self.outputLayerNeurons = outputLayerNeurons
            self.activationFunctions = activationFunctions

            self.epochs = 500
            self.batch_size = 32
            self.learningRate = 0.0001
            self.threshold = 1e-6

            self.__initializeLayers()

    def setEpochs(self, epochs):
        """
        Set the number of training epochs.

        Args:
            epochs (int): The total number of epochs to run during training.

        Example:
            >>> nn.setEpochs(1000)
        """
        self.epochs = epochs

    def setBatchSize(self, batchSize):
        """
        Set the batch size for training.

        Args:
            batchSize (int): The number of samples per training batch.

        Example:
            >>> nn.setBatchSize(64)
        """
        self.batchSize = batchSize

    def setLearningRate(self, learningRate):
        """
        Set the learning rate for the training process.

        Args:
            learningRate (float): The step size used when updating the network's weights.

        Example:
            >>> nn.setLearningRate(0.001)
        """
        self.learningRate = learningRate

    def setThreshold(self, threshold):
        """
        Set the convergence threshold for early stopping during training.

        Args:
            threshold (float): If the training loss falls below this value, training can be halted.

        Example:
            >>> nn.setThreshold(1e-3)
        """
        self.threshold = threshold

    def __initializeLayers(self):
        """
        Construct the layers using the specified architecture.

        Example:
            >>> nn._initializeLayers()
        """
        self.layers = []
        prevNeurons = self.inputLayerNeurons

        for i, neurons in enumerate(self.hiddenLayersNeurons):
            activation = self.activationFunctions[i]
            self.layers.append(Layer(prevNeurons, neurons, activation))
            prevNeurons = neurons

        activation = self.activationFunctions[-1]
        self.layers.append(Layer(prevNeurons, self.outputLayerNeurons, activation))

    def feedForward(self, inputs):
        """
        Perform a feed-forward pass through the network.

        Args:
            inputs (np.array): Input data of shape (n_samples, inputLayerNeurons).

        Returns:
            tuple: (activations, preActivations)
                - activations: List of outputs per layer (including the input).
                - preActivations: List of linear combinations (z values) before activation.

        Example:
            >>> import numpy as np
            >>> inputs = np.array([[0.5, 0.8]])
            >>> activations, preActivations = nn.feedForward(inputs)
        """
        activations = [inputs]
        preActivations = []
        currentOutput = inputs

        for layer in self.layers:
            currentOutput = layer.forward(currentOutput)
            preActivations.append(layer.preActivation)
            activations.append(currentOutput)

        return activations, preActivations

    def backPropagation(self, activations, preActivations, expectedOutput):
        """
        Perform backpropagation to update the network's weights and biases.

        Args:
            activations (list of np.array): Activations from each layer (including input).
            preActivations (list of np.array): Linear combinations (z values) before activation.
            expectedOutput (np.array): Expected output values.

        Example:
            >>> # Suppose activations and preActivations were obtained via feedForward
            >>> nn.backPropagation(activations, preActivations, expectedOutput)
        """
        outputError = activations[-1] - expectedOutput
        lastActivationDerivative = self.layers[-1].activationDerivative(preActivations[-1])
        
        if lastActivationDerivative.ndim == 3:
            delta = np.einsum('ij,ijk->ik', outputError, lastActivationDerivative)
        else:
            delta = outputError * lastActivationDerivative
        deltas = [delta]

        for i in reversed(range(len(self.layers) - 1)):
            layer = self.layers[i]
            nextLayer = self.layers[i + 1]
            delta = deltas[0].dot(nextLayer.weights.T) * layer.activationDerivative(preActivations[i])
            deltas.insert(0, delta)

        for i, layer in enumerate(self.layers):
            layer.weights -= self.learningRate * activations[i].T.dot(deltas[i])
            layer.biases -= self.learningRate * np.sum(deltas[i], axis=0, keepdims=True)

    def train(self, trainingData, trainingLabels, useThreshold=False, plotErrorsVsEpochs=False):
        """
        Train the network using mini-batch gradient descent and backpropagation.

        Args:
            trainingData (np.array): Training input data.
            trainingLabels (np.array): Corresponding expected outputs.
            useThreshold (bool, optional): Stop training early if error falls below threshold.
            plotErrorsVsEpochs (bool, optional): plot a line chart of errors vs epochs.

        Example:
            >>> import numpy as np
            >>> # Example for an XOR problem
            >>> trainingData = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
            >>> trainingLabels = np.array([[0], [1], [1], [0]])
            >>> nn.train(trainingData, trainingLabels)
        """
        print("Start training the neural network.")
        allErrors = []
        numberSamples = trainingData.shape[0]
        for epoch in range(self.epochs):
            indices = np.arange(numberSamples)
            np.random.shuffle(indices)
            trainingDataShuffled = trainingData[indices]
            trainingLabelsShuffled = trainingLabels[indices]

            totalEpochLoss = 0.0
            numberBatches = 0

            for batchStart in range(0, numberSamples, self.batch_size):
                batchEnd = batchStart + self.batch_size
                batchData = trainingDataShuffled[batchStart:batchEnd]
                batchLabels = trainingLabelsShuffled[batchStart:batchEnd]

                activations, preActivations = self.feedForward(batchData)
                predictions = activations[-1]
                batchLoss = np.mean((predictions - batchLabels) ** 2)
                totalEpochLoss += batchLoss
                numberBatches += 1

                self.backPropagation(activations, preActivations, batchLabels)

            averageLoss = totalEpochLoss / numberBatches
            print(f"Epoch {epoch+1}/{self.epochs} - Error: {averageLoss:.6f}")
            
            allErrors.append(averageLoss)

            if useThreshold and averageLoss < self.threshold:
                print(f"Average error {averageLoss:.6f} is below threshold {self.threshold}. Stopping training.")
                break
        
        if (plotErrorsVsEpochs):
            errorPlotOverEpochs(allErrors)
        print("Training completed.")

    def evaluation(self, testingData, testingLabels):
        predictions = []
        for i in range(testingData.shape[0]):
            sample = testingData[i].reshape(1, -1)
            activations, _ = self.feedForward(sample)
            output = activations[-1]

            if self.outputLayerNeurons == 1:
                predictedLabel = 1 if output[0, 0] > 0.5 else 0
            else:
                predictedLabel = np.argmax(output, axis=1)[0]

            predictions.append(predictedLabel)

        predictions = np.array(predictions)

        if testingLabels.ndim > 1 and testingLabels.shape[1] > 1:
            expectedLabels = np.argmax(testingLabels, axis=1)
        else:
            expectedLabels = testingLabels.flatten()

        accuracy = np.mean(predictions == expectedLabels) * 100
        print(f"\nEvaluation completed with accuracy: {accuracy:.2f}%")

    def predict(self, inputData):
        """
        Generate a prediction for the given input data.

        Args:
            inputData (np.array): Input data for prediction.

        Returns:
            tuple: (activations, preActivations) from the feed-forward pass.

        Example:
            >>> import numpy as np
            >>> sample = np.array([[0.5, 0.8]])
            >>> activations, preActivations = nn.predict(sample)
        """
        return self.feedForward(inputData)

    def saveModel(self, filename="NeuralNetworkModel.json"):
        """
        Save the model architecture and parameters to a JSON file.

        Args:
            filename (str): File name to save the model.

        Example:
            >>> nn.saveModel("model.json")
        """
        print("\nSaving the model...")
        modelData = {
            "input_size": self.inputLayerNeurons,
            "hidden_size": self.hiddenLayersNeurons,
            "output_size": self.outputLayerNeurons,
            "activation_functions": self.activationFunctions,
            "weights": [layer.weights.tolist() for layer in self.layers],
            "biases": [layer.biases.tolist() for layer in self.layers]
        }
        with open(filename, "w") as file:
            json.dump(modelData, file)
        print(f"Model saved to \"{filename}\".")

    def loadModel(self, modelFile="NeuralNetworkModel.json"):
        """
        Load a model from a JSON file and rebuild the network.

        Args:
            modelFile (str): Path to the JSON file containing the model.

        Example:
            >>> nn.loadModel("model.json")
        """
        print(f"\nLoading model from \"{modelFile}\"...")
        
        with open(modelFile, "r") as file:
            modelData = json.load(file)
        self.inputLayerNeurons = modelData["input_size"]
        self.hiddenLayersNeurons = modelData["hidden_size"]
        self.outputLayerNeurons = modelData["output_size"]
        self.activationFunctions = modelData["activation_functions"]

        self.layers = []
        layerSizes = self.hiddenLayersNeurons + [self.outputLayerNeurons]
        prevNeurons = self.inputLayerNeurons

        for i, neurons in enumerate(layerSizes):
            activation = self.activationFunctions[i]
            layer = Layer(prevNeurons, neurons, activation)
            layer.weights = np.array(modelData["weights"][i])
            layer.biases = np.array(modelData["biases"][i])
            self.layers.append(layer)
            prevNeurons = neurons

        print("Model loaded.")
