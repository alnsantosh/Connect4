from keras.utils import plot_model
import keras
import pydot, graphviz
import os
from keras import layers

def get_input_position(x,y):
	return 4*(x*7+y),4*(x*7+y+1)

def layer1filter(inputTensor,x,y,dir):
	concat_step=[]
	for step in range(4):
		if dir=="v":
			start_position,end_position=get_input_position(x+step,y)
		elif dir=="h":
			start_position,end_position=get_input_position(x,y+step)
		elif dir=="pd":
			start_position,end_position=get_input_position(x+step,y+step)
		elif dir=="nd":
			start_position,end_position=get_input_position(x+step,y-step)
		concat_step.append(inputTensor[:,start_position:end_position])
	lamdaLayer=keras.layers.concatenate(concat_step)
	#print(lamdaLayer)
	return lamdaLayer


def get_model():
	os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
	inputTensor =keras.layers.Input(shape=(168,))
	layer1Lambda =[]
	for i in range(3):
		for j in range(7):
			layer1Lambda.append(keras.layers.Lambda(layer1filter, arguments={"x":i,"y":j,"dir":"v"}, output_shape=((16,)))(inputTensor))

	for j in range(6):
		for i in range(4):
			layer1Lambda.append(keras.layers.Lambda(layer1filter, arguments={"x":i,"y":j,"dir":"h"}, output_shape=((16,)))(inputTensor))

	for i in range(3):
		for j in range(4):
			layer1Lambda.append(keras.layers.Lambda(layer1filter, arguments={"x":i,"y":j,"dir":"pd"}, output_shape=((16,)))(inputTensor))

	for i in range(3):
		for j in range(3,7):
			layer1Lambda.append(keras.layers.Lambda(layer1filter, arguments={"x":i,"y":j,"dir":"nd"}, output_shape=((16,)))(inputTensor))

	layer1DenseConnection=[]
	for l in range(len(layer1Lambda)):
		layer1Lambda[l]=keras.layers.Dense(1)(layer1Lambda[l])
	layer1Output=keras.layers.concatenate(layer1Lambda)
	denselayer2 =keras.layers.Dense(138)(layer1Output)
	outputlayer = keras.layers.Dense(42)(denselayer2)
	model=keras.models.Model(inputs=inputTensor,outputs=outputlayer)
	model.summary()
	return model
	#plot_model(model, to_file='model.png')
