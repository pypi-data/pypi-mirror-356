import numpy as np
import pandas as pd
from random import randint

def loadDataFromTextFile(filePath, numberOfData=-1, inputSize=2, labelSize=1):
    """
    Load a dataset from a CSV text file and split it into input features and labels.

    This function reads a CSV file (without headers) from the specified file path using pandas.
    It can optionally limit the number of rows read from the file. The data is then split into two
    parts: one for input features and one for labels, based on the provided column sizes.

    Args:
        filePath (str): The path to the CSV file containing the dataset.
        numberOfData (int, optional): The maximum number of data rows to load. If set to -1 (default),
            all rows are loaded.
        inputSize (int, optional): The number of columns representing input features. Defaults to 2.
        labelSize (int, optional): The number of columns representing labels. Defaults to 1.

    Returns:
        tuple: A tuple containing two numpy arrays:
            - np.ndarray: The array of input features.
            - np.ndarray: The array of labels.

    Example:
        >>> inputs, labels = loadDataFromTextFile("data.csv", numberOfData=100, inputSize=3, labelSize=1)
        >>> print(inputs.shape, labels.shape)
    """
    print(f"\nLoading dataset from file \"{filePath}\"")
    data = pd.read_csv(filePath, header=None)

    if numberOfData != -1:
        data = data.iloc[:numberOfData]

    data = data.values

    inputData = data[:, :inputSize]
    labels = data[:, inputSize:inputSize + labelSize]
    
    print("Dataset loaded.")
    return np.array(inputData), np.array(labels)


def generateExampleDataset(numberOfData):
    """
    Generate an example XOR dataset.

    This function creates a dataset for the XOR logic gate by generating a specified number of
    random binary pairs. For each pair, the XOR (exclusive OR) operation is computed to produce a label.
    The dataset is returned as two lists: one containing the input pairs and the other containing the
    corresponding XOR results.

    Args:
        numberOfData (int): The number of data samples to generate.

    Returns:
        tuple: A tuple containing two elements:
            - inputData (list of list of int): A list where each element is a list of two binary integers,
              representing the input pair (e.g., [0, 1]).
            - labels (list of int): A list of integers (0 or 1) representing the XOR result for each input pair.

    Example:
        >>> inputs, labels = generateExampleDataset(4)
        >>> print(inputs)
        [[0, 1], [1, 0], [0, 0], [1, 1]]
        >>> print(labels)
        [1, 1, 0, 0]
    """
    inputData = []
    labels = []

    for _ in range(numberOfData):
        xRandom = randint(0, 1)
        yRandom = randint(0, 1)

        randomData = [xRandom, yRandom]
        result = xRandom ^ yRandom
        
        inputData.append(randomData)
        labels.append(result)

    return inputData, labels
