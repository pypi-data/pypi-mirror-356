"""

Activation Functions on CPU
===========================
This module contains activation functions that run on the CPU.


Module functions:
-----------------
- 'sigmoid': Sigmoid,
- 'mod_circular': modular_circular_activation,
- 'tanh_circular': tanh_circular_activation,
- 'leaky_relu': leaky_relu,
- 'relu': Relu,
- 'gelu': gelu,
- 'tanh': tanh,
- 'sinakt': sinakt,
- 'p_squared': p_squared,
- 'sglu': lambda x: sglu(x, alpha=1.0),
- 'dlrelu': dlrelu,
- 'sin_plus': sin_plus,
- 'acos': lambda x: acos(x, alpha=1.0, beta=0.0),
- 'isra': isra,
- 'waveakt': waveakt,
- 'arctan': arctan,
- 'bent_identity': bent_identity,
- 'softsign': softsign,
- 'pwl': pwl,
- 'sine': sine,
- 'tanh_square': tanh_square,
- 'linear':,
- 'sine_square': sine_square,
- 'logarithmic': logarithmic,
- 'sine_offset': lambda x: sine_offset(x, 1.0),
- 'spiral': spiral_activation,
- 'circular': circular_activation
- Softmax()
"""

import numpy as np
from scipy.special import expit, softmax
import warnings

# ACTIVATION FUNCTIONS -----

def all_activations():

    activations_list = ['linear', 'sigmoid', 'relu', 'tanh', 'circular', 'spiral', 'sin_plus', 'mod_circular', 'tanh_circular', 'leaky_relu', 'gelu', 'sinakt', 'p_squared', 'sglu', 'dlrelu', 'acos', 'isra', 'waveakt', 'arctan', 'bent_identity', 'softsign', 'pwl', 'sine', 'tanh_square', 'sine_square', 'logarithmic', 'sine_offset']
    return activations_list

def spiral_activation(x):

    r = np.sqrt(np.sum(x**2))
    
    theta = np.arctan2(x[1:], x[:-1])

    spiral_x = r * np.cos(theta + r)
    spiral_y = r * np.sin(theta + r)
    

    spiral_output = np.concatenate(([spiral_x[0]], spiral_y))
    
    return spiral_output


def Softmax(
    x  # num: Input data to be transformed using softmax function.
):
    """
    Applies the softmax function to the input data.

    Args:
        (num): Input data to be transformed using softmax function.

    Returns:
       (num): Transformed data after applying softmax function.
    """

    return softmax(x)


def Sigmoid(
    x  # num: Input data to be transformed using sigmoid function.
):
    """
    Applies the sigmoid function to the input data.

    Args:
        (num): Input data to be transformed using sigmoid function.

    Returns:
        (num): Transformed data after applying sigmoid function.
    """
    return expit(x)


def Relu(
    x  # num: Input data to be transformed using ReLU function.
):
    """
    Applies the Rectified Linear Unit (ReLU) function to the input data.

    Args:
        (num): Input data to be transformed using ReLU function.

    Returns:
        (num): Transformed data after applying ReLU function.
    """

    return np.maximum(0, x)

def tanh(x):
    return np.tanh(x)

def sin_plus(x):
    return (np.sin(x) + 1) / 2

def modular_circular_activation(x, period=2*np.pi):
    return np.mod(x, period) / period

def tanh_circular_activation(x):
    return (np.tanh(x) + 1) / 2

def leaky_relu(x, alpha=0.01):
    return np.where(x > 0, x, alpha * x)

def gelu(x):
    return 0.5 * x * (1 + np.tanh(np.sqrt(2 / np.pi) * (x + 0.044715 * np.power(x, 3))))

def sinakt(x):
    return np.sin(x) + np.cos(x)

def p_squared(x, alpha=1.0, beta=0.0):
    return alpha * x**2 + beta * x

def sglu(x, alpha=1.0):
    return softmax(alpha * x) * x

# 4. Double Leaky ReLU (DLReLU)
def dlrelu(x):
    return np.maximum(0.01 * x, x) + np.minimum(0.01 * x, 0.1 * x)

# 6. Adaptive Cosine Activation (ACos)
def acos(x, alpha=1.0, beta=0.0):
    return np.cos(alpha * x + beta)

# 10. Inverse Square Root Activation (ISRA)
def isra(x):
    return x / np.sqrt(np.abs(x) + 1)

def waveakt(x, alpha=1.0, beta=2.0, gamma=3.0):
    return np.sin(alpha * x) * np.cos(beta * x) * np.sin(gamma * x)

def arctan(x):
    return np.arctan(x)

def bent_identity(x):
    return (np.sqrt(x**2 + 1) - 1) / 2 + x

def circular_activation(x, scale=2.0, frequency=1.0, shift=0.0):    
    
    n_features = x.shape[0]
    
    circular_output = np.zeros_like(x)
    
    for i in range(n_features):
        
        r = np.sqrt(np.sum(x**2))
        theta = 2 * np.pi * (i / n_features) + shift
        
        circular_x = r * np.cos(theta + frequency * r) * scale
        circular_y = r * np.sin(theta + frequency * r) * scale
        
        if i % 2 == 0:
            circular_output[i] = circular_x
        else:
            circular_output[i] = circular_y
    
    return circular_output

def softsign(x):
    return x / (1 + np.abs(x))

def pwl(x, alpha=0.5, beta=1.5):
    return np.where(x <= 0, alpha * x, beta * x)

def sine(x, alpha=1.0):
    return np.sin(alpha * x)

def tanh_square(x):
    return np.tanh(x)**2

def sine_square(x):
    return np.sin(x)**2

def logarithmic(x):
    return np.log(x**2 + 1)

def sine_offset(x, beta=0.0):
    return np.sin(x + beta)


def apply_activation(Input, activation_list):
    """
    Applies activation functions for inputs
    
    Args:
        Input (numpy.ndarray):
        activation_list (list):
    """
    origin_input = np.copy(Input)
    
    activation_functions = {
        'sigmoid': Sigmoid,
        'mod_circular': modular_circular_activation,
        'tanh_circular': tanh_circular_activation,
        'leaky_relu': leaky_relu,
        'relu': Relu,
        'gelu': gelu,
        'tanh': tanh,
        'sinakt': sinakt,
        'p_squared': p_squared,
        'sglu': lambda x: sglu(x, alpha=1.0),
        'dlrelu': dlrelu,
        'sin_plus': sin_plus,
        'acos': lambda x: acos(x, alpha=1.0, beta=0.0),
        'isra': isra,
        'waveakt': waveakt,
        'arctan': arctan,
        'bent_identity': bent_identity,
        'softsign': softsign,
        'pwl': pwl,
        'sine': sine,
        'tanh_square': tanh_square,
        'linear': lambda x: x,
        'sine_square': sine_square,
        'logarithmic': logarithmic,
        'sine_offset': lambda x: sine_offset(x, 1.0),
        'spiral': spiral_activation,
        'circular': circular_activation
    }
    
    try:

        valid_mask = np.array([act in activation_functions for act in activation_list])
        valid_activations = np.array(activation_list)[valid_mask]

        activation_outputs = np.array([activation_functions[act](origin_input) for act in valid_activations])

        return np.sum(activation_outputs, axis=0)
        
    except Exception as e:
        warnings.warn(f"Error in activation processing: {str(e)}", RuntimeWarning)
        return Input