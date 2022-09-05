#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np
from tqdm import tqdm

def removeIfExist(file_path):
    while os.path.exists(file_path):
        try:
            os.remove(file_path)
        except:
            continue
    return True

def renameFile(file_path, target_file_path):
    if not os.path.exists(file_path):
        print("[ERROR][rgb_reader::renameFile]")
        print("\t file not exist!")
        return False

    while os.path.exists(file_path):
        try:
            os.rename(file_path, target_file_path)
        except:
            continue
    return True

def getImage(data, image_size, image_idx):
    image_data = data[image_idx * image_size : (image_idx + 1) * image_size]
    int_data = [int(x) for x in image_data]
    image = np.array(int_data).reshape((1440, 2048, 3)).astype(np.uint8)
    return image

def saveImage(data, image_size, image_idx, save_folder_path):
    save_image_file_path = save_folder_path + str(image_idx) + ".png"
    if os.path.exists(save_image_file_path):
        return True

    image = getImage(data, image_size, image_idx)

    tmp_image_file_path = save_folder_path + str(image_idx) + "_tmp.png"
    removeIfExist(tmp_image_file_path)
    cv2.imwrite(tmp_image_file_path, image)

    renameFile(tmp_image_file_path, save_image_file_path)
    return True

if __name__ == "__main__":
    rgb_file_path = "./正常速度输液视频.rgb"
    image_width = 2048
    image_height = 1440
    image_channel = 3
    save_folder_path = "/home/chli/chLi/WaterDrop/20220905_zbar_cap/"

    with open(rgb_file_path, "rb") as f:
        data = f.read()

    os.makedirs(save_folder_path, exist_ok=True)

    image_size = image_width * image_height * image_channel
    image_num = int(len(data) / image_size)

    print("start save images...")
    for i in tqdm(range(image_num)):
        saveImage(data, image_size, i, save_folder_path)

