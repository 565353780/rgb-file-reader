#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from tqdm import tqdm

from rgb_file_reader.Method.image import getImage, saveImage

class RGBReader(object):
    def __init__(self,
                 rgb_file_path=None,
                 image_width=None,
                 image_height=None,
                 image_channel=None):
        self.rgb_file_path = rgb_file_path
        self.image_width = image_width
        self.image_height = image_height
        self.image_channel = image_channel

        self.data = None
        self.image_size = None
        self.image_num = None

        if self.rgb_file_path is not None:
            self.loadRGBFile(self.rgb_file_path)
        return

    def reset(self):
        self.data = None

    def loadRGBData(self):
        if self.rgb_file_path is None:
            print("[ERROR][RGBReader::loadRGBData]")
            print("\t rgb_file_path is None!")
            return False
        if not os.path.exists(self.rgb_file_path):
            print("[ERROR][RGBReader::loadRGBData]")
            print("\t rgb_file not exist!")
            return False

        with open(self.rgb_file_path, "rb") as f:
            self.data = f.read()

        if None in [self.image_width,
                    self.image_height,
                    self.image_channel]:
            print("[ERROR][RGBReader::loadRGBData]")
            print("\t image size not valid!")
            return False

        self.image_size = \
            self.image_width * \
            self.image_height * \
            self.image_channel

        self.image_num = int(len(self.data) / self.image_size)
        return True

    def loadRGBFile(self, rgb_file_path):
        self.rgb_file_path = rgb_file_path

        if not self.loadRGBData():
            print("[ERROR][RGBReader::loadRGBFile]")
            print("\t loadRGBData failed!")
            return False
        return True

    def getImage(self, image_idx):
        if image_idx >= self.image_num:
            print("[ERROR][RGBReader::getImage]")
            print("\t image_idx out of range!")
            return None
        image = getImage(self.data, self.image_size, image_idx)
        return image

    def saveImage(self, image_idx, save_folder_path):
        if image_idx >= self.image_num:
            print("[ERROR][RGBReader::saveImage]")
            print("\t image_idx out of range!")
            return False

        if not saveImage(self.data,
                         self.image_size,
                         image_idx,
                         save_folder_path):
            print("[ERROR][RGBReader::saveImage]")
            print("\t saveImage failed!")
            return False
        return True

    def saveAllImage(self, save_folder_path, print_progress=False):
        for_data = range(self.image_num)
        if print_progress:
            for_data = tqdm(for_data)
        for i in for_data:
            if not self.saveImage(i, save_folder_path):
                print("[ERROR][RGBReader::saveAllImage]")
                print("\t saveImage failed!")
                return False
        return True

def demo():
    rgb_file_path = "/home/chli/water/正常速度输液视频.rgb"
    image_width = 2048
    image_height = 1440
    image_channel = 3
    save_folder_path = "/home/chli/chLi/WaterDrop/20220905_zbar_cap/"

    rgb_reader = RGBReader(rgb_file_path,
                           image_width,
                           image_height,
                           image_channel)

    rgb_reader.saveAllImage(save_folder_path, True)
    return True

