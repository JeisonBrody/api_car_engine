import os
import torch
import torch.nn as nn
import torchvision
import onnxruntime
import cv2
from tqdm import tqdm
import numpy as np


def inference(onnx_path, imgs_dir, img_fname):
    session = onnxruntime.InferenceSession(onnx_path, providers=['CPUExecutionProvider'])
    print(onnxruntime.get_available_providers())
    print(onnxruntime.get_device())

    mark_file = '/Users/macbook/PycharmProjects/dip/archive/misc/make_names.csv'
    model_file = '/Users/macbook/PycharmProjects/dip/archive/misc/model_names.csv'

    with open(mark_file, 'r') as file:
        mark_list = file.read().splitlines()
    with open(model_file, 'r') as file:
        model_list = file.read().splitlines()

    IN_IMAGE_W, IN_IMAGE_H = 224, 224

    img = cv2.imread(os.path.join(imgs_dir, img_fname), cv2.IMREAD_COLOR)
    resized = cv2.resize(img, (IN_IMAGE_W, IN_IMAGE_H), interpolation=cv2.INTER_LINEAR)
    img_in = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    img_in = np.transpose(img_in, (2, 0, 1)).astype(np.float32)
    img_in = np.expand_dims(img_in, axis=0)
    img_in /= 255.0

    # Computing
    input_name = session.get_inputs()[0].name

    mark_outputs, model_outputs = session.run(None, {input_name: img_in})
    mark_conf, mark_prediction = np.max(mark_outputs), np.argmax(mark_outputs)
    model_conf, model_prediction = np.max(model_outputs), np.argmax(model_outputs)

    print(f'{img_fname} | Mark: {mark_list[mark_prediction]} | Model: {model_list[model_prediction]}')
    return f"{mark_list[mark_prediction]} {(model_list[model_prediction])}"


def recognition(fname):
    onnx_path = "/Users/macbook/PycharmProjects/dip/archive/weights/exp2/compcar_model.onnx"
    images_dir = "/Users/macbook/PycharmProjects/dip/archive/photo"
    car = inference(onnx_path, images_dir, fname)
    return car


if __name__ == '__main__':
    onnx_path = "/Users/macbook/Desktop/Диплом/neural_net_dip/archive/weights/exp2/compcar_model.onnx"
    imgs_fname = ""
    images_dir = "/Users/macbook/PycharmProjects/dip/archive/photo"

    # inference(onnx_path, images_dir, imgs_fname)
