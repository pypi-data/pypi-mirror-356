import numpy as np

def softmaxActivation(data):
    """
    Compute the softmax function in a numerically stable way.
    Expects z to be a 2D array (batch_size x num_classes).
    """
    exps = np.exp(data - np.max(data, axis=1, keepdims=True))
    return exps / np.sum(exps, axis=1, keepdims=True)

def softmaxDerivative(data):
    """
    Compute the full Jacobian matrix for softmax for each sample.
    Returns a 3D array of shape (batch_size, num_classes, num_classes)
    where each slice [i, :, :] is the Jacobian for sample i.
    """
    softmax = softmaxActivation(data)
    batch_size, num_classes = softmax.shape
    jacobian = np.zeros((batch_size, num_classes, num_classes))
    
    for i in range(batch_size):
        for j in range(num_classes):
            for k in range(num_classes):
                if j == k:
                    jacobian[i, j, k] = softmax[i, j] * (1 - softmax[i, j])
                else:
                    jacobian[i, j, k] = -softmax[i, j] * softmax[i, k]
    
    return jacobian

def sigmoidActivation(data):
    """
    Apply the sigmoid activation function.

    Args:
        data (np.array): Input data.

    Returns:
        np.array: The result of applying the sigmoid function.
    """
    data = np.clip(data, -500, 500)
    return 1 / (1 + np.exp(-data))

def sigmoidDerivative(data):
    """
    Compute the derivative of the sigmoid function.

    Args:
        data (np.array): Pre-activation values.

    Returns:
        np.array: The derivative of the sigmoid function.
    """
    s = sigmoidActivation(data)
    return s * (1 - s)

def reluActivation(data):
    """
    Apply the ReLU activation function.

    Args:
        data (np.array): Input data.

    Returns:
        np.array: The result of applying the ReLU function.
    """
    return np.maximum(0, data)

def reluDerivative(data):
    """
    Compute the derivative of the ReLU function.

    Args:
        data (np.array): Pre-activation values.

    Returns:
        np.array: The derivative of the ReLU function.
    """
    return (data > 0).astype(float)

def tanhActivation(data):
    """
    Apply the tanh activation function.

    Args:
        data (np.array): Input data.

    Returns:
        np.array: The result of applying the tanh function.
    """
    return np.tanh(data)

def tanhDerivative(data):
    """
    Compute the derivative of the tanh function.

    Args:
        data (np.array): Pre-activation values.

    Returns:
        np.array: The derivative of the tanh function.
    """
    return 1 - np.tanh(data) ** 2