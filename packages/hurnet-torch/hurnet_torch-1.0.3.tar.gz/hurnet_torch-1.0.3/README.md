HurNetTorch is a neural network algorithm with the [HurNet](https://github.com/sapiens-technology/HurNet) architecture that extends the originals capabilities of direct division calculations for beyond processing with CPU, adapting the computational processes through the PyTorch module for devices with GPU, TPU or MPS.

# HurNetTorch

This code was designed, architected, and developed mathematically and algorithmically by Ben-Hur Varriano for Sapiens Technology®️ and aims to modularize the construction of artificial neural networks through a revolutionary architecture called [HurNet](https://github.com/sapiens-technology/HurNet). This architecture replaces the backpropagation process with direct division calculations without gradient descent, making the training and inference of neural networks significantly faster than traditional approaches. This revolutionary concept relies on robust mathematics that drastically reduces the demand for processing and makes [HurNet](https://github.com/sapiens-technology/HurNet) a new paradigm in networks in the field of Artificial Intelligence.

If you prefer, click [here](https://colab.research.google.com/drive/1apjuHSb5ker6r7bdrqN8AlfjWK7RFMlb?usp=sharing) to run it via [Google Colab](https://colab.research.google.com/drive/1apjuHSb5ker6r7bdrqN8AlfjWK7RFMlb?usp=sharing).

Click [here](https://github.com/sapiens-technology/HurNet/blob/main/HurNet-EN.pdf) to read the full study.

<br>![Separate Data](hurnet_torch_equation.png)<br>

## Installation

Use the package manager [pip](https://pypi.org/project/hurnet_torch/) to install HurNetTorch.

```bash
pip install hurnet_torch
```

## Usage
Basic usage example:
```python
from hurnet_torch import HurNetTorch

hurnet_torch_neural_network = HurNetTorch()
# training samples with a pattern that simulates the logic of the xor operator
inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
outputs = [[0], [1], [1], [0]]
# hurnet architecture is more accurate than others, so it is possible to get the correct answer without any hidden layers
hurnet_torch_neural_network.train(input_layer=inputs, output_layer=outputs)

test_outputs = hurnet_torch_neural_network.predict(input_layer=inputs, decimal_places=0)
print(test_outputs)

```
```bash
[[0], [1], [1], [0]]
```

The HurNetTorch network can abstract linear patterns with 100% accuracy.
```python
from hurnet_torch import HurNetTorch

hurnet_torch_neural_network = HurNetTorch()
# samples for training with a pattern that sums the input vectors to obtain the output vectors
inputs = [[1, 2], [3, 4], [5, 6], [7, 8]]
outputs = [[3], [7], [11], [15]]

hurnet_torch_neural_network.train(input_layer=inputs, output_layer=outputs)

test_inputs = [[2, 3], [4, 5], [6, 7], [8, 9]]

test_outputs = hurnet_torch_neural_network.predict(input_layer=test_inputs, decimal_places=0)
print(test_outputs)

```
```bash
[[5], [9], [13], [17]]
```
You can use any number of elements in the input samples and output samples.
```python
from hurnet_torch import HurNetTorch

hurnet_torch_neural_network = HurNetTorch()
'''
samples for training with a pattern that multiplies the input by two in the first element of each output
and then multiplies the first element of the same output by ten to obtain the second element of this output
'''
inputs = [[1], [2], [3], [4]]
outputs = [[2, 20], [4, 40], [6, 60], [8, 80]]

hurnet_torch_neural_network.train(input_layer=inputs, output_layer=outputs)

test_inputs = [[5], [6], [7], [8]]

test_outputs = hurnet_torch_neural_network.predict(input_layer=test_inputs, decimal_places=0)
print(test_outputs)

```
```bash
[[10, 100], [12, 120], [14, 140], [16, 160]]
```
The network accepts lists with any dimensionality, see a one-dimensional example.
```python
from hurnet_torch import HurNetTorch

hurnet_torch_neural_network = HurNetTorch()
# samples for training with a pattern that calculates twice as many input elements
inputs = [1, 2, 3, 4, 5]
outputs = [2, 4, 6, 8, 10]

hurnet_torch_neural_network.train(input_layer=inputs, output_layer=outputs)

test_inputs = [6, 7, 8, 9]

test_outputs = hurnet_torch_neural_network.predict(input_layer=test_inputs, decimal_places=0)
print(test_outputs)

```
```bash
[12, 14, 16, 18]
```
You can use scalar values in both inputs and outputs. Here's an example with scalars only in the inputs:
```python
from hurnet_torch import HurNetTorch

hurnet_torch_neural_network = HurNetTorch()
'''
with this input pattern, the network should learn that for each scalar,
a vector must be created with twice the value in the first element and
twice the value multiplied by ten in the second element
'''
inputs = [2, 4, 6, 8]
outputs = [[4, 40], [8, 80], [12, 120], [16, 160]]

hurnet_torch_neural_network.train(input_layer=inputs, output_layer=outputs)

test_inputs = [1, 3, 7, 9]

test_outputs = hurnet_torch_neural_network.predict(input_layer=test_inputs, decimal_places=0)
print(test_outputs)

```
```bash
[[2, 20], [6, 60], [14, 140], [18, 180]]
```
Now see an example with scalar values only in the outputs.
```python
from hurnet_torch import HurNetTorch

hurnet_torch_neural_network = HurNetTorch()
# training samples with a pattern that simulates the logical xor operator
inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
outputs = [0, 1, 1, 0]

hurnet_torch_neural_network.train(input_layer=inputs, output_layer=outputs)

test_inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]

test_outputs = hurnet_torch_neural_network.predict(input_layer=test_inputs, decimal_places=0)
print(test_outputs)

```
```bash
[0, 1, 1, 0]
```
Note that there is no limit to the dimensionality of the inputs and outputs. You can work with tensors of any shape aspect ratio.
```python
from hurnet_torch import HurNetTorch

hurnet_torch_neural_network = HurNetTorch()
# example of the xor operator adapted for high dimensionality
inputs = [[[0], [0]], [[0], [1]], [[1], [0]], [[1], [1]]]
outputs = [[[0]], [[1]], [[1]], [[0]]]

hurnet_torch_neural_network.train(input_layer=inputs, output_layer=outputs)

test_inputs = [[[0], [0]], [[0], [1]], [[1], [0]], [[1], [1]]]

test_outputs = hurnet_torch_neural_network.predict(input_layer=test_inputs, decimal_places=0)
print(test_outputs)

```
```bash
[[[0]], [[1]], [[1]], [[0]]]
```
Note that there is no limit to the shape's aspect ratio.
```python
from hurnet_torch import HurNetTorch

hurnet_torch_neural_network = HurNetTorch()
# example of the xor operator adapted to even higher dimensionality
inputs = [[[[[0]], [[0]]]], [[[[0]], [[1]]]], [[[[1]], [[0]]]], [[[[1]], [[1]]]]]
outputs = [[[[0]]], [[[1]]], [[[1]]], [[[0]]]]

hurnet_torch_neural_network.train(input_layer=inputs, output_layer=outputs)

test_inputs = [[[[[0]], [[0]]]], [[[[0]], [[1]]]], [[[[1]], [[0]]]], [[[[1]], [[1]]]]]

test_outputs = hurnet_torch_neural_network.predict(input_layer=test_inputs, decimal_places=0)
print(test_outputs)

```
```bash
[[[[0]]], [[[1]]], [[[1]]], [[[0]]]]
```
With the "decimal_places" parameter, you can control the maximum number of decimal places in the prediction numbers.
```python
from hurnet_torch import HurNetTorch

hurnet_torch_neural_network = HurNetTorch()

inputs = [[1.54321, 2.12345], [3.54321, 4.12345]]
outputs = [[3.54321], [7.54321]]

hurnet_torch_neural_network.train(input_layer=inputs, output_layer=outputs)

test_inputs = [[2.54321, 3.12345]]
# when "decimal_places" is not set, it defaults to None, for all decimal places
print(hurnet_torch_neural_network.predict(input_layer=test_inputs)) # with all decimal places
print(hurnet_torch_neural_network.predict(input_layer=test_inputs, decimal_places=4)) # with 4 decimal places
print(hurnet_torch_neural_network.predict(input_layer=test_inputs, decimal_places=3)) # with 3 decimal places
print(hurnet_torch_neural_network.predict(input_layer=test_inputs, decimal_places=2)) # with 2 decimal places
print(hurnet_torch_neural_network.predict(input_layer=test_inputs, decimal_places=1)) # with 1 decimal place
print(hurnet_torch_neural_network.predict(input_layer=test_inputs, decimal_places=0)) # with no decimal places

```
```bash
[[5.47587347]]
[[5.4759]]
[[5.476]]
[[5.48]]
[[5.5]]
[[5]]
```
Check out an example with the two prediction parameters.
```python
from hurnet_torch import HurNetTorch

hurnet_torch_neural_network = HurNetTorch()

inputs = [[1, 2], [3, 4]]
outputs = [[3], [7]]

hurnet_torch_neural_network.train(input_layer=inputs, output_layer=outputs)

test_inputs = [[2, 3]]

test_outputs = hurnet_torch_neural_network.predict(test_inputs, 0)
print(test_outputs)

```
```bash
[[5]]
```
Use the "addHiddenLayer" function to add hidden layers to the network and increase the abstraction capacity of non-linear patterns.
```python
from hurnet_torch import HurNetTorch

hurnet_torch_neural_network = HurNetTorch()

inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
outputs = [[0], [1], [1], [0]]
"""
the module accepts the following activation functions both in the layer and in training:
('linear', 'sigmoid', 'tanh', 'relu', 'leaky_relu', 'leakyrelu', 'softmax', 'softplus', 'elu', 'silu', 'swish', 'gelu', 'selu', 'mish', 'hard_sigmoid', 'hardsigmoid')
"""
# you can add as many layers as you want
hurnet_torch_neural_network.addHiddenLayer( # returns True if the layer is added successfully, or False otherwise
	num_neurons=2, # integer for the number of neurons in the layer (default 1)
	activation_function='sigmoid' # string value with the name of the activation function applied to the layer weights calculation (default 'linear')
)

hurnet_torch_neural_network.train(input_layer=inputs, output_layer=outputs)

test_inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]

test_outputs = hurnet_torch_neural_network.predict(test_inputs)
print(test_outputs)

```
```bash
[[0.0], [1.0], [1.0], [0.0]]
```
You can apply an activation function on top of the result of the last added layer, using the "activation_function" parameter of the training function.
```python
from hurnet_torch import HurNetTorch

hurnet_torch_neural_network = HurNetTorch()

inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
outputs = [[0], [1], [1], [0]]

hurnet_torch_neural_network.addHiddenLayer(num_neurons=2, activation_function='sigmoid')
hurnet_torch_neural_network.train(input_layer=inputs, output_layer=outputs, activation_function='relu')

test_inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]

test_outputs = hurnet_torch_neural_network.predict(test_inputs)
print(test_outputs)

```
```bash
[[0.0], [1.13415909], [0.77803898], [0.0]]
```
It is also possible to add multiple hidden layers. There is no limit to the number of hidden layers you can add.
```python
from hurnet_torch import HurNetTorch

hurnet_torch_neural_network = HurNetTorch()

inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
outputs = [[0], [1], [1], [0]]
# use in the neurons, the same amount of elements contained in the input samples
hurnet_torch_neural_network.addHiddenLayer(num_neurons=2, activation_function='relu')
hurnet_torch_neural_network.addHiddenLayer(num_neurons=2, activation_function='tanh')
hurnet_torch_neural_network.addHiddenLayer(num_neurons=2, activation_function='silu')

hurnet_torch_neural_network.train(input_layer=inputs, output_layer=outputs)

test_inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]

test_outputs = hurnet_torch_neural_network.predict(test_inputs)
print(test_outputs)

```
```bash
[[0.0], [1.0], [1.0], [0.0]]
```
With the "bias" parameter you can add an arbitrary value to the network weights.
```python
from hurnet_torch import HurNetTorch

hurnet_torch_neural_network = HurNetTorch()

inputs = [[1], [2], [3], [4]]
outputs = [[2], [4], [6], [8]]
# if no value is assigned to "bias" the network will use the default value of 0.0
hurnet_torch_neural_network.train(input_layer=inputs, output_layer=outputs, bias=0.5)

test_inputs = [[5], [6], [7], [8]]

test_outputs = hurnet_torch_neural_network.predict(test_inputs)
print(test_outputs)

```
```bash
[[12.5], [15.0], [17.5], [20.0]]
```
With the "learning_rate" parameter, you can multiply the network weights by an arbitrary value.
```python
from hurnet_torch import HurNetTorch

hurnet_torch_neural_network = HurNetTorch()

inputs = [[1], [2], [3], [4]]
outputs = [[2], [4], [6], [8]]
# if no value is assigned to "learning_rate" the network will use the default value of 1.0
hurnet_torch_neural_network.train(input_layer=inputs, output_layer=outputs, learning_rate=1.1)

test_inputs = [[5], [6], [7], [8]]

test_outputs = hurnet_torch_neural_network.predict(test_inputs)
print(test_outputs)

```
```bash
[[11.0], [13.20000076], [15.40000057], [17.60000038]]
```
With the "quantization" parameter, you can quantize the network weights so that they are rounded to a certain number of decimal places.
```python
from hurnet_torch import HurNetTorch

hurnet_torch_neural_network = HurNetTorch()

inputs = [[1], [2], [3], [4]]
outputs = [[2], [4], [6], [8]]
# the default value of the "quantization" parameter is None, so that no rounding is applied
hurnet_torch_neural_network.train(input_layer=inputs, output_layer=outputs, quantization=2)

test_inputs = [[5], [6], [7], [8]]

test_outputs = hurnet_torch_neural_network.predict(test_inputs)
print(test_outputs)

```
```bash
[[10.0], [12.0], [14.0], [16.0]]
```
With the "method" parameter, you can choose between two different types of calculations for adjusting weights. With the "division" value, the weights will be calculated based on the division of the outputs by the inputs. With the "pseudo-inverse" value, the weights will be calculated based on the pseudo-inverse.
```python
from hurnet_torch import HurNetTorch

hurnet_torch_neural_network = HurNetTorch()
# samples for training with a pattern that calculates the sum of the entries in the first element and multiplies that sum by ten in the second element
inputs = [[1, 2], [3, 4], [5, 6], [7, 8]]
outputs = [[3, 30], [7, 70], [11, 110], [15, 150]]
# the default value of the "method" parameter is "division", for the division calculation
hurnet_torch_neural_network.train(input_layer=inputs, output_layer=outputs, method='pseudo-inverse')

test_inputs = [[2, 3], [4, 5]]

test_outputs = hurnet_torch_neural_network.predict(test_inputs, decimal_places=0)
print(test_outputs)

```
```bash
[[5, 50], [9, 90]]
```
With the "progress" parameter, you can display the training progress bar with True, or disable the display of the bar with False.
```python
from hurnet_torch import HurNetTorch

hurnet_torch_neural_network = HurNetTorch()

inputs = [[1, 2], [3, 4], [5, 6], [7, 8]]
outputs = [[3, 30], [7, 70], [11, 110], [15, 150]]
# the default value of the "progress" parameter is False, to keep the progress bar disabled
hurnet_torch_neural_network.train(input_layer=inputs, output_layer=outputs, progress=True)

test_inputs = [[2, 3], [4, 5], [6, 7]]

test_outputs = hurnet_torch_neural_network.predict(test_inputs, decimal_places=0)
print(test_outputs)

```
```bash
Training model: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4/4 [00:00<00:00, 173.10it/s]
[[5, 50], [9, 90], [13, 130]]
```
With the "saveModel" function it is possible to save the trained model to load it later from any location.
```python
from hurnet_torch import HurNetTorch

hurnet_torch_neural_network = HurNetTorch()

inputs = [[1, 2], [3, 4], [5, 6], [7, 8]]
outputs = [[3, 30], [7, 70], [11, 110], [15, 150]]

hurnet_torch_neural_network.train(input_layer=inputs, output_layer=outputs)

hurnet_torch_neural_network.saveModel( # returns True if saved successfully, or False otherwise
	model_path='./my_model.hurnettorch', # string with the save path
	progress=True # True to enable the progress bar, or False to keep the progress bar disabled (default False)
)

```
```bash
Saving model: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1.25k/1.25k [00:00<00:00, 4.04MB/s]
```
With the "loadModel" function it is possible to load a pre-trained model from a specific location.
```python
from hurnet_torch import HurNetTorch

hurnet_torch_neural_network = HurNetTorch()

hurnet_torch_neural_network.loadModel( # returns True if loaded successfully, or False otherwise
	model_path='./my_model.hurnettorch', # string with the path of the model to be loaded
	progress=True # True to enable the progress bar, or False to keep the progress bar disabled (default False)
)

test_inputs = [[2, 3], [4, 5], [6, 7]]

test_outputs = hurnet_torch_neural_network.predict(test_inputs, decimal_places=0)
print(test_outputs)

```
```bash
Loading model: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1.25k/1.25k [00:00<00:00, 20.4MB/s]
[[5, 50], [9, 90], [13, 130]]
```
If no path is given to the "model_path" parameter of the "saveModel" function, the default value "./model.hurnettorch" will be used.
```python
from hurnet_torch import HurNetTorch

hurnet_torch_neural_network = HurNetTorch()

inputs = [[1, 2], [3, 4], [5, 6], [7, 8]]
outputs = [[3, 30], [7, 70], [11, 110], [15, 150]]

hurnet_torch_neural_network.train(input_layer=inputs, output_layer=outputs)

hurnet_torch_neural_network.saveModel()

```
```bash

```
If no path is given to the "model_path" parameter of the "loadModel" function, the default value "./model.hurnettorch" will be used.
```python
from hurnet_torch import HurNetTorch

hurnet_torch_neural_network = HurNetTorch()

hurnet_torch_neural_network.loadModel()

test_inputs = [[2, 3], [4, 5], [6, 7]]

test_outputs = hurnet_torch_neural_network.predict(test_inputs, decimal_places=0)
print(test_outputs)

```
```bash
[[5, 50], [9, 90], [13, 130]]
```
The "toAdjustInnerLength" function normalizes an input tensor by making all of its innermost vectors have the same number of numeric elements.
```python
from hurnet_torch import HurNetTorch

hurnet_torch_neural_network = HurNetTorch()
# the tensor must have the same number of numeric elements in all vectors
test_inputs = [[1, 2, 3, 4], [4, 3, 2, 1]]
# the default value of "numeric_length" is None, to not modify the number of internal numeric elements
print(hurnet_torch_neural_network.toAdjustInnerLength(input_tensor=test_inputs, numeric_length=7))
print(hurnet_torch_neural_network.toAdjustInnerLength(input_tensor=test_inputs, numeric_length=3))
print(hurnet_torch_neural_network.toAdjustInnerLength(input_tensor=test_inputs, numeric_length=None))

```
```bash
[[1.0, 2.0, 3.0, 4.0, 0.0, 0.0, 0.0], [4.0, 3.0, 2.0, 1.0, 0.0, 0.0, 0.0]]
[[1.0, 2.0, 3.0], [4.0, 3.0, 2.0]]
[[1, 2, 3, 4], [4, 3, 2, 1]]
```
With the "getParameters" function you get a dictionary with all the model configuration parameters.
```python
from hurnet_torch import HurNetTorch

hurnet_torch_neural_network = HurNetTorch()

inputs = [[1, 2], [3, 4], [5, 6], [7, 8]]
outputs = [[3, 30], [7, 70], [11, 110], [15, 150]]

hurnet_torch_neural_network.addHiddenLayer(2, 'sigmoid')
hurnet_torch_neural_network.train(inputs, outputs)

result_dictionary = hurnet_torch_neural_network.getParameters()
print(result_dictionary)

```
```bash
{'one_dimensional_input': 0, 'one_dimensional_output': 0, 'method': 'division', 'weights_vector': [], 'activation_function': 'linear', 'hidden_layers': [[2, 'sigmoid']], 'hidden_weights': [[[0.8834270238876343, 1.5426652431488037], [0.6478235125541687, 0.4084811210632324]]], 'hidden_biases': [[-2.074511766433716, 0.16853241622447968]], 'weights_list': [[2.0658180713653564, 20.658180236816406], [3.575137138366699, 35.751373291015625], [5.505502700805664, 55.055023193359375], [7.500348091125488, 75.00347900390625]], 'weights_matrix': [], 'output_dimensions': [2], 'vector_length': 1}
```
With the "setParameters" function you can update the model's configuration parameters.
```python
from hurnet_torch import HurNetTorch

hurnet_torch_neural_network = HurNetTorch()

inputs = [[1, 2], [3, 4], [5, 6], [7, 8]]
outputs = [[3, 30], [7, 70], [11, 110], [15, 150]]

hurnet_torch_neural_network.train(inputs, outputs)

result_dictionary = hurnet_torch_neural_network.getParameters()
hurnet_torch_neural_network.setParameters(state=result_dictionary)

test_inputs = [[2, 3], [4, 5], [6, 7]]

test_outputs = hurnet_torch_neural_network.predict(test_inputs, decimal_places=0)
print(test_outputs)

```
```bash
[[5, 50], [9, 90], [13, 130]]
```
With the "device" parameter of the class constructor, you can choose the network execution device.
```python
from hurnet_torch import HurNetTorch
# the "device" parameter receives a string with the name of the execution device, or None so that the best device is chosen automatically
# if the selected device does not exist on the current machine, the algorithm will search for the best available device
hurnet_torch_neural_network = HurNetTorch(device=None) # runs on the best available device
inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
outputs = [[0], [1], [1], [0]]
hurnet_torch_neural_network.train(input_layer=inputs, output_layer=outputs)
test_inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
test_outputs = hurnet_torch_neural_network.predict(input_layer=test_inputs, decimal_places=0)
print(test_outputs)

hurnet_torch_neural_network = HurNetTorch(device='gpu') # runs on gpu
inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
outputs = [[0], [1], [1], [0]]
hurnet_torch_neural_network.train(input_layer=inputs, output_layer=outputs)
test_inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
test_outputs = hurnet_torch_neural_network.predict(input_layer=test_inputs, decimal_places=0)
print(test_outputs)

hurnet_torch_neural_network = HurNetTorch(device='cuda') # runs on gpu
inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
outputs = [[0], [1], [1], [0]]
hurnet_torch_neural_network.train(input_layer=inputs, output_layer=outputs)
test_inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
test_outputs = hurnet_torch_neural_network.predict(input_layer=test_inputs, decimal_places=0)
print(test_outputs)

hurnet_torch_neural_network = HurNetTorch(device='tpu') # runs on tpu
inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
outputs = [[0], [1], [1], [0]]
hurnet_torch_neural_network.train(input_layer=inputs, output_layer=outputs)
test_inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
test_outputs = hurnet_torch_neural_network.predict(input_layer=test_inputs, decimal_places=0)
print(test_outputs)

hurnet_torch_neural_network = HurNetTorch(device='xla') # runs on tpu
inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
outputs = [[0], [1], [1], [0]]
hurnet_torch_neural_network.train(input_layer=inputs, output_layer=outputs)
test_inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
test_outputs = hurnet_torch_neural_network.predict(input_layer=test_inputs, decimal_places=0)
print(test_outputs)

hurnet_torch_neural_network = HurNetTorch(device='mps') # runs on mps
inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
outputs = [[0], [1], [1], [0]]
hurnet_torch_neural_network.train(input_layer=inputs, output_layer=outputs)
test_inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
test_outputs = hurnet_torch_neural_network.predict(input_layer=test_inputs, decimal_places=0)
print(test_outputs)

hurnet_torch_neural_network = HurNetTorch(device='cpu') # runs on cpu
inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
outputs = [[0], [1], [1], [0]]
hurnet_torch_neural_network.train(input_layer=inputs, output_layer=outputs)
test_inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
test_outputs = hurnet_torch_neural_network.predict(input_layer=test_inputs, decimal_places=0)
print(test_outputs)

```
```bash
[[0], [1], [1], [0]]
[[0], [1], [1], [0]]
[[0], [1], [1], [0]]
[[0], [1], [1], [0]]
[[0], [1], [1], [0]]
[[0], [1], [1], [0]]
[[0], [1], [1], [0]]
```
See below an example with logical operators.
```python
from hurnet_torch import HurNetTorch
inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
# outputs for the logical operator "and"
# is only true (1) when both inputs are equal to true (1)
hurnet_torch_neural_network = HurNetTorch()
outputs = [[0], [0], [0], [1]]
hurnet_torch_neural_network.train(input_layer=inputs, output_layer=outputs)
test_outputs = hurnet_torch_neural_network.predict(input_layer=inputs, decimal_places=0)
print(test_outputs)
# outputs for the logical operator "or"
# will be true (1) when at least one of the inputs is equal to true (1)
hurnet_torch_neural_network = HurNetTorch()
outputs = [[0], [1], [1], [1]]
hurnet_torch_neural_network.train(input_layer=inputs, output_layer=outputs)
test_outputs = hurnet_torch_neural_network.predict(input_layer=inputs, decimal_places=0)
print(test_outputs)
# outputs for the logical operator "not"
# true (1) becomes false (0) and false (0) becomes true (1)
hurnet_torch_neural_network = HurNetTorch()
outputs = [[1, 1], [1, 0], [0, 1], [0, 0]]
hurnet_torch_neural_network.addHiddenLayer(num_neurons=2, activation_function='sigmoid')
hurnet_torch_neural_network.addHiddenLayer(num_neurons=2, activation_function='relu')
hurnet_torch_neural_network.train(input_layer=inputs, output_layer=outputs)
test_outputs = hurnet_torch_neural_network.predict(input_layer=inputs, decimal_places=0)
print(test_outputs)
# outputs for the logical operator "xor"
# is true (1) only when the two inputs are different
hurnet_torch_neural_network = HurNetTorch()
outputs = [[0], [1], [1], [0]]
hurnet_torch_neural_network.train(input_layer=inputs, output_layer=outputs)
test_outputs = hurnet_torch_neural_network.predict(input_layer=inputs, decimal_places=0)
print(test_outputs)

```
```bash
[[0], [0], [0], [1]]
[[0], [1], [1], [1]]
[[1, 1], [1, 0], [0, 1], [0, 0]]
[[0], [1], [1], [0]]
```
Below is an example without using hidden layers and using hidden layers on the same data samples.
```python
# without hidden layers the network cannot learn enough to generalize non-linear patterns with different orderings
from hurnet_torch import HurNetTorch

hurnet_torch_neural_network = HurNetTorch()
inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
outputs = [[0], [1], [1], [0]]
hurnet_torch_neural_network.train(input_layer=inputs, output_layer=outputs)
# test with the inputs in a different order than the one used in training
test_inputs = [[1, 0], [0, 1], [1, 1], [0, 0]]
test_outputs = hurnet_torch_neural_network.predict(input_layer=test_inputs, decimal_places=0)
print(test_outputs)

# by adding hidden layers, the network improves pattern abstraction and can generalize to any ordering
hurnet_torch_neural_network = HurNetTorch()
inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
outputs = [[0], [1], [1], [0]]
hurnet_torch_neural_network.addHiddenLayer(num_neurons=2, activation_function='sigmoid')
hurnet_torch_neural_network.addHiddenLayer(num_neurons=2, activation_function='relu')
hurnet_torch_neural_network.train(input_layer=inputs, output_layer=outputs)
# test with the inputs in a different order than the one used in training
test_inputs = [[1, 0], [0, 1], [1, 1], [0, 0]]
test_outputs = hurnet_torch_neural_network.predict(input_layer=test_inputs, decimal_places=0)
print(test_outputs)

```
```bash
[[0], [1], [2], [0]]
[[0], [1], [1], [0]]
```
Check below a comparative example between the training and inference time spent running the HurNetTorch the network algorithm and the PyTorch the network algorithm commonly used in building language models.
```bash
pip install hurnet torch hurnet_torch
```
```python
# test run on a macbook pro m3 max with 48gb vram
# !pip install hurnet
from hurnet import measure_execution_time, tensor_similarity_percentage
"""
training pattern
first output element: sums the first two input elements
second output element: multiplies the sum of the first two input elements by ten
third output element: subtracts one from the third input element
"""
# samples for training
input_layer = [[1, 2, 3], [3, 4, 5], [5, 6, 7]]
output_layer = [[3, 30, 2], [7, 70, 4], [11, 110, 6]]
# samples for prediction/test
input_layer_for_testing = [[2, 3, 4], [4, 5, 6]]
expected_output = [[5, 50, 3], [9, 90, 5]]
# !pip install torch
import torch
import torch.nn as nn
import torch.optim as optim
torch.manual_seed(42)
inputs = torch.tensor(input_layer, dtype=torch.float32)
outputs = torch.tensor(output_layer, dtype=torch.float32)
class NeuralNet(nn.Module):
    def __init__(self):
        super(NeuralNet, self).__init__()
        self.fc1 = nn.Linear(3, 10)
        self.fc2 = nn.Linear(10, 10)
        self.fc3 = nn.Linear(10, 3)
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x
model = NeuralNet()
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)
test_inputs = []
# !pip install hurnet_torch
from hurnet_torch import HurNetTorch
hurnet_torch_neural_network = HurNetTorch(device='cpu')
def test_with_pytorch_TRAIN():
    print('######################### ALGORITHM: PYTORCH (TRAIN) #########################')
    # artificial neural network training
    epochs = 9000 # minimum value found to obtain the best result
    for epoch in range(epochs):
        optimizer.zero_grad()
        predictions = model(inputs)
        loss = criterion(predictions, outputs)
        loss.backward()
        optimizer.step()
    global test_inputs
    test_inputs = torch.tensor(input_layer_for_testing, dtype=torch.float32)
def test_with_pytorch_INFERENCE():
	print('####################### ALGORITHM: PYTORCH (INFERENCE) #######################')
	# artificial neural network inference
	test_outputs = model(test_inputs).detach().numpy().astype(int).tolist()
	similarity = tensor_similarity_percentage(obtained_output=test_outputs, expected_output=expected_output)
	print(test_outputs)
	print(f'similarity between the result and the expectation: {similarity:.10f}.')

# test with the hurnet_torch algorithm, note that it is not necessary to apply deep learning
def test_with_hurnet_torch_TRAIN():
	print('###################### ALGORITHM: HURNET-TORCH (TRAIN)  ######################')
	# artificial neural network training
	hurnet_torch_neural_network.train(input_layer=input_layer, output_layer=output_layer)
	# artificial neural network inference
def test_with_hurnet_torch_INFERENCE():
	print('#################### ALGORITHM: HURNET-TORCH (INFERENCE)  ####################')
	test_outputs = hurnet_torch_neural_network.predict(input_layer=input_layer_for_testing, decimal_places=0)
	similarity = tensor_similarity_percentage(obtained_output=test_outputs, expected_output=expected_output)
	print(test_outputs)
	print(f'similarity between the result and the expectation: {similarity:.10f}.')

# calculation for measurement of training and inference results
pytorch_time_train = measure_execution_time(function=test_with_pytorch_TRAIN, display_message=True)
hurnet_torch_time_train = measure_execution_time(function=test_with_hurnet_torch_TRAIN, display_message=True)
difference_train = int(round(max((hurnet_torch_time_train, pytorch_time_train))/min((hurnet_torch_time_train, pytorch_time_train))))
description = f'''
Note that the HurNetTorch network is {difference_train} times faster than the PyTorch network ({pytorch_time_train:.10f} divided by {hurnet_torch_time_train:.10f}).
Also remember that this time difference can increase dramatically as more complexity is added to the network.
'''
print(description)
pytorch_time_inference = measure_execution_time(function=test_with_pytorch_INFERENCE, display_message=True)
hurnet_torch_time_inference = measure_execution_time(function=test_with_hurnet_torch_INFERENCE, display_message=True)
difference_inference = int(round(round(max((hurnet_torch_time_inference, pytorch_time_inference))/min((hurnet_torch_time_inference, pytorch_time_inference)), 2)-1, 2)*100)
description = f'''
Note that the HurNetTorch network is {difference_inference}% faster than the PyTorch network ({pytorch_time_inference:.10f} divided by {hurnet_torch_time_inference:.10f}).
Also remember that this time difference can increase dramatically as more complexity is added to the network.
'''
print(description)

```
```bash
######################### ALGORITHM: PYTORCH (TRAIN) #########################
Execution time: 1.0847776653 seconds.
###################### ALGORITHM: HURNET-TORCH (TRAIN)  ######################
Execution time: 0.0001490004 seconds.

Note that the HurNetTorch network is 7280 times faster than the PyTorch network (1.0847776653 divided by 0.0001490004).
Also remember that this time difference can increase dramatically as more complexity is added to the network.

####################### ALGORITHM: PYTORCH (INFERENCE) #######################
[[5, 50, 2], [9, 90, 4]]
similarity between the result and the expectation: 0.9111111111.
Execution time: 0.0001232093 seconds.
#################### ALGORITHM: HURNET-TORCH (INFERENCE)  ####################
[[4, 45, 3], [9, 88, 5]]
similarity between the result and the expectation: 0.9462962963.
Execution time: 0.0000950415 seconds.

Note that the HurNetTorch network is 30% faster than the PyTorch network (0.0001232093 divided by 0.0000950415).
Also remember that this time difference can increase dramatically as more complexity is added to the network.

```
In one of the tests with the MPS hardware of the Macbook M3 Max with 48 GB of VRAM, we were able to obtain a result of up to 5612 times more speed with the HurNetTorch architecture.<br>

![Separate Data](separate_data.png)<br>

In one of the tests with the standard Google Colab CPU environment, we were able to achieve a result of up to **14161** times more speed with the HurNetTorch architecture.
```bash
######################### ALGORITHM: PYTORCH (TRAIN) #########################
Execution time: 11.1138258950 seconds.
###################### ALGORITHM: HURNET-TORCH (TRAIN)  ######################
Execution time: 0.0007848080 seconds.

Note that the HurNetTorch network is 14161 times faster than the PyTorch network (11.1138258950 divided by 0.0007848080).
Also remember that this time difference can increase dramatically as more complexity is added to the network.

####################### ALGORITHM: PYTORCH (INFERENCE) #######################
[[4, 49, 2], [8, 89, 4]]
similarity between the result and the expectation: 0.8540740741.
Execution time: 0.0006746120 seconds.
#################### ALGORITHM: HURNET-TORCH (INFERENCE)  ####################
[[4, 45, 3], [9, 88, 5]]
similarity between the result and the expectation: 0.9462962963.
Execution time: 0.0004365520 seconds.

Note that the HurNetTorch network is 55% faster than the PyTorch network (0.0006746120 divided by 0.0004365520).
Also remember that this time difference can increase dramatically as more complexity is added to the network.

```
![Separate Data](google_colab.png)<br>
![Separate Data](similarity_google_colab.png)<br>

```python
# test run on a macbook pro m3 max with 48gb vram
from hurnet import measure_execution_time, tensor_similarity_percentage
"""
training pattern
first output element: sums the first two input elements
second output element: multiplies the sum of the first two input elements by ten
third output element: subtracts one from the third input element
"""
# samples for training
input_layer = [[1, 2, 3], [3, 4, 5], [5, 6, 7]]
output_layer = [[3, 30, 2], [7, 70, 4], [11, 110, 6]]
# samples for prediction/test
input_layer_for_testing = [[2, 3, 4], [4, 5, 6]]
expected_output = [[5, 50, 3], [9, 90, 5]]

def test_with_pytorch(): # !pip install torch
    print('###################### ALGORITHM: PYTORCH (TRAIN and INFERENCE) ######################')
    import torch
    import torch.nn as nn
    import torch.optim as optim
    torch.manual_seed(42)
    inputs = torch.tensor(input_layer, dtype=torch.float32)
    outputs = torch.tensor(output_layer, dtype=torch.float32)
    class NeuralNet(nn.Module):
        def __init__(self):
            super(NeuralNet, self).__init__()
            self.fc1 = nn.Linear(3, 10)
            self.fc2 = nn.Linear(10, 10)
            self.fc3 = nn.Linear(10, 3)
        def forward(self, x):
            x = torch.relu(self.fc1(x))
            x = torch.relu(self.fc2(x))
            x = self.fc3(x)
            return x
    model = NeuralNet()
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    # artificial neural network training
    epochs = 9000 # minimum value found to obtain the best result
    for epoch in range(epochs):
        optimizer.zero_grad()
        predictions = model(inputs)
        loss = criterion(predictions, outputs)
        loss.backward()
        optimizer.step()
    test_inputs = torch.tensor(input_layer_for_testing, dtype=torch.float32)
    # artificial neural network inference
    test_outputs = model(test_inputs).detach().numpy().astype(int).tolist()
    similarity = tensor_similarity_percentage(obtained_output=test_outputs, expected_output=expected_output)
    print(test_outputs)
    print(f'similarity between the result and the expectation: {similarity:.10f}.')

# test with the hurnet_torch algorithm, note that it is not necessary to apply deep learning
def test_with_hurnet_torch(): # !pip install hurnet_torch
    print('###################### ALGORITHM: HURNET-TORCH (TRAIN and INFERENCE)  ######################')
    from hurnet_torch import HurNetTorch
    hurnet_torch_neural_network = HurNetTorch(device='cpu')
    # artificial neural network training
    hurnet_torch_neural_network.train(input_layer=input_layer, output_layer=output_layer)
    # artificial neural network inference
    test_outputs = hurnet_torch_neural_network.predict(input_layer=input_layer_for_testing, decimal_places=0)
    similarity = tensor_similarity_percentage(obtained_output=test_outputs, expected_output=expected_output)
    print(test_outputs)
    print(f'similarity between the result and the expectation: {similarity:.10f}.')

# calculation for measurement of training and inference results
pytorch_time = measure_execution_time(function=test_with_pytorch, display_message=True)
hurnet_torch_time = measure_execution_time(function=test_with_hurnet_torch, display_message=True)
difference = int(round(max((hurnet_torch_time, pytorch_time))/min((hurnet_torch_time, pytorch_time))))
description = f'''
Note that the HurNetTorch network is {difference} times faster than the PyTorch network ({pytorch_time:.10f} divided by {hurnet_torch_time:.10f}).
Also remember that this time difference can increase dramatically as more complexity is added to the network.
'''
print(description)

```
```bash
###################### ALGORITHM: PYTORCH (TRAIN and INFERENCE) ######################
[[5, 50, 2], [9, 90, 4]]
similarity between the result and the expectation: 0.9111111111.
Execution time: 1.8048646664 seconds.
###################### ALGORITHM: HURNET-TORCH (TRAIN and INFERENCE)  ######################
[[4, 45, 3], [9, 88, 5]]
similarity between the result and the expectation: 0.9462962963.
Execution time: 0.0014207494 seconds.

Note that the HurNetTorch network is 1270 times faster than the PyTorch network (1.8048646664 divided by 0.0014207494).
Also remember that this time difference can increase dramatically as more complexity is added to the network.

```
![Separate Data](data_together.png)<br>

# HurNetTorch
## Methods
### Construtor: HurNetTorch
Parameters
| Name                | Description                                                                                                | Type              | Default Value     |
|---------------------|------------------------------------------------------------------------------------------------------------|-------------------|-------------------|
| device              | device name for training and inference                                                                     | str               | None              |

### addHiddenLayer (function return type: bool): Returns True if the hidden layer is added successfully, or False otherwise.
Parameters
| Name                | Description                                                                                                | Type              | Default Value     |
|---------------------|------------------------------------------------------------------------------------------------------------|-------------------|-------------------|
| num_neurons         | number of neurons for the layer being added                                                                | int               | 1                 |
| activation_function | string with the name of the activation function to be used for linear or non-linear data abstraction       | str               | 'linear'          |

### train (function return type: bool): Returns True if training is successful or False otherwise.
Parameters
| Name                | Description                                                                                                | Type              | Default Value     |
|---------------------|------------------------------------------------------------------------------------------------------------|-------------------|-------------------|
| input_layer         | tensor with input samples                                                                                  | list              | []                |
| output_layer        | tensor with output samples                                                                                 | list              | []                |
| activation_function | string with the name of the activation function applied to the result of the last layer                    | str               | 'linear'          |
| bias                | positive or negative floating number used to add bias to the network                                       | float             | 0.0               |
| learning_rate       | updates the network weights by multiplying its value by the weights                                        | float             | 1.0               |
| quantization        | integer with the number of decimal places for the weights                                                  | int               | None              |
| method              | 'division' to calculate weights with division, or 'pseudo-inverse' to calculate with pseudo-inverse        | str               | 'division'        |
| progress            | True to enable the progress bar, or False to disable it                                                    | bool              | False             |

### saveModel (function return type: bool): Returns True if the training save is successful or False otherwise.
Parameters
| Name                | Description                                                                                                | Type              | Default Value     |
|---------------------|------------------------------------------------------------------------------------------------------------|-------------------|-------------------|
| model_path          | path and name of the file to be generated, for the saved training model                                    | str               | ''                |
| progress            | True to enable the progress bar, or False to disable it                                                    | bool              | False             |

### loadModel (function return type: bool): Returns True if the training load is successful or False otherwise.
Parameters
| Name                | Description                                                                                                | Type              | Default Value     |
|---------------------|------------------------------------------------------------------------------------------------------------|-------------------|-------------------|
| model_path          | path and name of the file to be loaded, for the pre-trained model to be used                               | str               | ''                |
| progress            | True to enable the progress bar, or False to disable it                                                    | bool              | False             |

### predict (function return type: list): Returns a multidimensional tensor with the numerical results of the inference.
Parameters
| Name                | Description                                                                                                | Type              | Default Value     |
|---------------------|------------------------------------------------------------------------------------------------------------|-------------------|-------------------|
| input_layer         | input tensor with samples for prediction                                                                   | list              | []                |
| decimal_places      | integer with the number of decimal places for the elements of the prediction output tensor                 | int               | None              |

### toAdjustInnerLength (function return type: list): Returns a list by updating the number of numeric elements.
Parameters
| Name                | Description                                                                                                | Type              | Default Value     |
|---------------------|------------------------------------------------------------------------------------------------------------|-------------------|-------------------|
| input_tensor        | native python list or pytorch tensor that will have the number of numeric elements normalized              | list/torch.Tensor | []                |
| numeric_length      | fixed amount of numeric elements in the innermost vectors                                                  | int               | None              |

### getParameters (function return type: dict): Returns a dictionary with the internal parameters that configure the model.

### setParameters (function return type: bool): Returns True if the model's internal parameters are updated, or False otherwise.
Parameters
| Name                | Description                                                                                                | Type              | Default Value     |
|---------------------|------------------------------------------------------------------------------------------------------------|-------------------|-------------------|
| state               | dictionary with the name of the parameters to be updated in keys and the update value in values            | dict              | {}                |


You can also use the "HurNetTransformer" class to calculate the initial weights of a Transformer network.
```python
from hurnet_torch import HurNetTransformer
from torch import tensor

x = tensor([[0, 0], [0, 1], [1, 0], [1, 1]])
y = tensor([[0], [1], [1], [0]])

hurnet_transformer = HurNetTransformer( # initialization of the main class
    input_dim=x.shape, # input tensor ratio
    output_dim=y.shape, # output tensor ratio
    activation_function='linear', # activation function for inference (will be applied to the prediction results)
    interaction=True, # enables or disables interaction calculation (increases or decreases the complexity of the network)
    bias=0.0, # arbitrary number for the network bias if the training function bias is not defined
    device='cpu' # execution device
) # if the device is not defined, the best available device will be selected automatically

hurnet_transformer.train_layer( # artificial neural network training
    x=x, # tensor with the input samples
    y=y, # tensor with the output samples
    activation_function='linear', # activation function applied to the last layer (will be applied to the results of the hidden layers)
    bias=0.01, # if this bias value is not set, the constructor bias will be used
    learning_rate=1.0, # arbitrary number that will be multiplied by the network weights so that they are updated
    quantization=2, # number of decimal places in rounding of weights
    method='division', # method used to replace backpropagation in the calculation of weight adjustment
    hidden_layers=[(2, 'sigmoid'), (2, 'tanh')] # list of hidden layers added to the network architecture
) # preferably use training with division when the x and y tensors are very large, for small or medium tensors use the pseudo-inverse

print(hurnet_transformer.weights) # displays the weights found in the adjustment
print(hurnet_transformer.weights_data) # displays the rescaled weights for the prediction
y = hurnet_transformer.forward(x=x) # performs the network inference
print(y.to(int).tolist()) # displays the prediction result

```
```bash
Parameter containing:
tensor([[-0.8340, -0.6419,  1.4841, -0.9246],
        [-1.0029,  0.1420, -0.7358, -0.1473],
        [ 0.0913, -0.0835, -0.3827,  1.0952],
        [ 0.2724,  1.7108, -1.0630,  1.5896],
        [ 0.8601, -0.8724,  0.7019,  0.2578],
        [-0.5030, -1.0133, -0.3386, -2.2299],
        [-0.0862, -1.3560,  0.4212,  0.5422],
        [ 0.1288, -0.1054,  0.1540, -1.0210],
        [ 0.9842,  0.1249, -0.3333, -0.0226],
        [ 0.8316, -0.7483,  0.9197, -0.5796]], requires_grad=True)
tensor([[-0.8340],
        [-0.6419],
        [ 1.4841],
        [-0.9246]])
[[0], [1], [1], [0]]
```

# HurNetTransformer
## Methods
### Construtor: HurNetTransformer
Parameters
| Name                | Description                                                                                                | Type              | Default Value     |
|---------------------|------------------------------------------------------------------------------------------------------------|-------------------|-------------------|
| input_dim           | shape of input samples                                                                                     | tuple             | (1,)              |
| output_dim          | shape of output samples                                                                                    | tuple             | (1,)              |
| activation_function | string with the name of the activation function applied to the inference result                            | str               | 'linear'          |
| interaction         | True to increase the number of weights in the network, or False to keep the default number of weights      | bool              | True              |
| bias                | floating number used to add bias to the network (used when train_layer bias is not set)                    | float             | 0.0               |
| device              | device name for training and inference                                                                     | str               | None              |

### train_layer (function return type: bool): Returns True if training is successful or False otherwise.
Parameters
| Name                | Description                                                                                                | Type              | Default Value     |
|---------------------|------------------------------------------------------------------------------------------------------------|-------------------|-------------------|
| x                   | tensor with input samples                                                                                  | torch.Tensor      | tensor([])        |
| y                   | tensor with output samples                                                                                 | torch.Tensor      | tensor([])        |
| activation_function | string with the name of the activation function applied to the result of the last layer                    | str               | 'linear'          |
| bias                | positive or negative floating number used to add bias to the network                                       | float             | None              |
| learning_rate       | updates the network weights by multiplying its value by the weights                                        | float             | None              |
| quantization        | integer with the number of decimal places for the weights                                                  | int               | None              |
| method              | 'division' to calculate weights with division, or 'pseudo-inverse' to calculate with pseudo-inverse        | str               | 'pseudo-inverse'  |
| hidden_layers       | list of tuples with hidden layers [(int with number of neurons, str with name of activation function)]     | list              | None              |

### forward (function return type: torch.Tensor): Returns a PyTorch tensor with the inference result.
Parameters
| Name                | Description                                                                                                | Type              | Default Value     |
|---------------------|------------------------------------------------------------------------------------------------------------|-------------------|-------------------|
| x                   | input tensor with samples for prediction                                                                   | torch.Tensor      | tensor([])        |


With the "TransformerHurNet" class you can obtain the configuration attributes of the "HurNetTransformer" architecture.
```python
from hurnet_torch import TransformerHurNet
from torch import tensor

x = tensor([[0, 0], [0, 1], [1, 0], [1, 1]])

hurnet_transformer = TransformerHurNet(
    embedding_dim=2, # number of numeric elements per vector
    block_size=8, # maximum number of elements processed at a time
    number_heads=1, # number of heads/attention mechanisms capturing patterns at the same time
    number_layers=1, # number of hidden layers in the network, the higher this number, the greater the amount of abstracted patterns and the heavier the network will be
    dropout=0.01, # percentage (between 0 and 1) of neurons turned off at each step so that the network tries to guess the missing neurons and learns instead of memorizing
    vocab_size=4, # total number of unique (non-repeating) elements that the network can process
    device='cpu', # device used in running the network (if none is defined, the class will choose the most suitable one automatically)
    outer=None # used only to maintain compatibility with older versions of the class
)

y = hurnet_transformer.forward(input_tensor=x)
print(y) # displays the output tensor

print(hurnet_transformer.positional_encoding) # displays the tensor with the encoding positions
print(hurnet_transformer.dropout) # displays the attribute that stores the dropout value
print(hurnet_transformer.embedding) # displays the ratio of the input tensor
print(hurnet_transformer.multi_head_attention) # displays the decoder with attention mechanisms for gpt models
print(hurnet_transformer.hurnet_layer) # displays the layer built with the HurNetTransformer architecture (instantiated object)

```
```bash
tensor([[[-4.1224e+00, -1.4080e+00,  4.9366e+00, -1.0510e+00],
         [-4.1224e+00, -1.4080e+00,  4.9366e+00, -1.0510e+00]],

        [[-4.1224e+00, -1.4080e+00,  4.9366e+00, -1.0510e+00],
         [-2.1274e+00, -2.2113e+00, -2.4930e-03,  4.1934e+00]],

        [[-2.1274e+00, -2.2113e+00, -2.4931e-03,  4.1934e+00],
         [-4.1224e+00, -1.4080e+00,  4.9366e+00, -1.0510e+00]],

        [[-2.1274e+00, -2.2113e+00, -2.4931e-03,  4.1934e+00],
         [-2.1274e+00, -2.2113e+00, -2.4933e-03,  4.1934e+00]]],
       grad_fn=<ViewBackward0>)
Parameter containing:
tensor([[[0., 0.],
         [0., 0.],
         [0., 0.],
         [0., 0.],
         [0., 0.],
         [0., 0.],
         [0., 0.],
         [0., 0.]]], requires_grad=True)
Dropout(p=0.01, inplace=False)
Embedding(4, 2)
TransformerDecoder(
  (layers): ModuleList(
    (0): TransformerDecoderLayer(
      (self_attn): MultiheadAttention(
        (out_proj): NonDynamicallyQuantizableLinear(in_features=2, out_features=2, bias=True)
      )
      (multihead_attn): MultiheadAttention(
        (out_proj): NonDynamicallyQuantizableLinear(in_features=2, out_features=2, bias=True)
      )
      (linear1): Linear(in_features=2, out_features=2048, bias=True)
      (dropout): Dropout(p=0.01, inplace=False)
      (linear2): Linear(in_features=2048, out_features=2, bias=True)
      (norm1): LayerNorm((2,), eps=1e-05, elementwise_affine=True)
      (norm2): LayerNorm((2,), eps=1e-05, elementwise_affine=True)
      (norm3): LayerNorm((2,), eps=1e-05, elementwise_affine=True)
      (dropout1): Dropout(p=0.01, inplace=False)
      (dropout2): Dropout(p=0.01, inplace=False)
      (dropout3): Dropout(p=0.01, inplace=False)
    )
  )
)
HurNetTransformer()
```

# TransformerHurNet
## Methods
### Construtor: TransformerHurNet
Parameters
| Name                | Description                                                                                                | Type              | Default Value     |
|---------------------|------------------------------------------------------------------------------------------------------------|-------------------|-------------------|
| embedding_dim       | amount of elements per token vector                                                                        | int               | 0                 |
| block_size          | maximum number of tokens for the context window size                                                       | int               | 0                 |
| number_heads        | number of attention mechanisms                                                                             | int               | 0                 |
| number_layers       | number of hidden layers in the transformer network                                                         | int               | 0                 |
| dropout             | percentage (between 0 and 1) of neurons turned off at each step                                            | float             | None              |
| vocab_size          | integer number with the vocabulary size                                                                    | int               | 0                 |
| device              | device name to run on                                                                                      | str               | None              |
| outer               | has no real functionality; just to maintain compatibility                                                  | NoneType          | None              |

### forward (function return type: torch.Tensor): Returns a PyTorch tensor with the inference result.
Parameters
| Name                | Description                                                                                                | Type              | Default Value     |
|---------------------|------------------------------------------------------------------------------------------------------------|-------------------|-------------------|
| input_tensor        | input tensor with samples for prediction                                                                   | torch.Tensor      | tensor([])        |

## Contributing

We do not accept contributions that may result in changing the original code.

Make sure you are using the appropriate version.

## License

This is proprietary software and its alteration and/or distribution without the developer's authorization is not permitted.
