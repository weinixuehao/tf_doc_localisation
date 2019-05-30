import numpy as np
import tensorflow as tf
import cv2
from PIL import Image, ImageDraw

def _load_graph(frozen_graph_filename):
    """
    """
    with tf.gfile.GFile(frozen_graph_filename, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    with tf.Graph().as_default() as graph:
        tf.import_graph_def(graph_def, name="")    
    return graph

# Load TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_path="frozen_model.tflite")
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Test model on random input data.
input_shape = input_details[0]['shape']
input_data = np.array(Image.open("test_samples_255x340/receipt_247.jpg").resize((input_shape[2], input_shape[1])), dtype=np.float32)
input_data = np.expand_dims(input_data, 0)
# input_data = np.array(np.random.random_sample(input_shape), dtype=np.float32)
interpreter.set_tensor(input_details[0]['index'], input_data)

interpreter.invoke()
output_data = interpreter.get_tensor(output_details[0]['index'])
cv2.imshow("tflite", output_data[0])
print(output_data)


freeze_file_name = "frozen_model.pb"
graph = _load_graph(freeze_file_name)
sess = tf.Session(graph=graph)
inputs = graph.get_tensor_by_name('input:0')
activation_map = graph.get_tensor_by_name("heats_map_regression/pred_keypoints/BiasAdd:0")
_activation_map = sess.run([activation_map], feed_dict={inputs: input_data})
asdf = _activation_map[0][0]
cv2.imshow("pb", asdf)
print(_activation_map)

while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # print "I'm done"
        break