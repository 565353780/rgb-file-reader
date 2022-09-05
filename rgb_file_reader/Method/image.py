#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np

from rgb_file_reader.Method.path import createFilePath, renameFile, removeIfExist

def getImage(data, image_size, image_idx):
    image_data = data[image_idx * image_size : (image_idx + 1) * image_size]
    int_data = [int(x) for x in image_data]
    image = np.array(int_data).reshape((1440, 2048, 3)).astype(np.uint8)
    return image

def saveImage(data, image_size, image_idx, save_folder_path):
    save_image_file_path = save_folder_path + str(image_idx) + ".png"
    if os.path.exists(save_image_file_path):
        return True

    createFilePath(save_image_file_path)

    image = getImage(data, image_size, image_idx)

    tmp_image_file_path = save_folder_path + str(image_idx) + "_tmp.png"
    removeIfExist(tmp_image_file_path)
    cv2.imwrite(tmp_image_file_path, image)

    renameFile(tmp_image_file_path, save_image_file_path)
    return True

