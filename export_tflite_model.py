import tensorflow as tf
import numpy as np 

outputNodeNames = ["heats_map_regression/pred_keypoints/BiasAdd"]
input_checkpoint = "data/train_dir/model.ckpt-33318"
graph_def_file = "224X224_frozen_model.pb"
input_name = "input"

with tf.Session(graph=tf.Graph()) as sess:
    inputImg = tf.placeholder(dtype=tf.float32, shape=(1, 224, 224, 3), name=input_name)
    saver = tf.train.import_meta_graph(input_checkpoint + '.meta', input_map={'IteratorGetNext:0':  inputImg}, clear_devices=True)
    saver.restore(sess, input_checkpoint)
    graph = tf.get_default_graph() # 获得默认的图
    graph_def = graph.as_graph_def()
    # tf.import_graph_def(graph_def, input_map={"IteratorGetNext:0": inputImg})
    # print(tf.get_default_graph().as_graph_def() == graph_def)
    # outputNodes = outputNodeNames.split(",")
    output_graph_def = tf.graph_util.convert_variables_to_constants(sess, graph_def, outputNodeNames)

    # Finally we serialize and dump the output graph to the filesystem
    with tf.gfile.GFile(graph_def_file, "wb") as f:
        f.write(output_graph_def.SerializeToString())

    input_arrays = [input_name]
    # converter = tf.lite.TFLiteConverter.from_frozen_graph(
    #         graph_def_file, input_arrays, outputNodeNames)
    # tflite_model = converter.convert()
    # open("255X340_frozen_model.tflite", "wb").write(tflite_model)

    converter = tf.contrib.lite.TocoConverter.from_frozen_graph(
    graph_def_file, input_arrays, outputNodeNames)
    tflite_model = converter.convert()
    open("224X224_frozen_model.tflite", "wb").write(tflite_model)
