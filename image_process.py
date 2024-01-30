import math

import cv2


def resize_img(img, scale_rate):
    new_width = int(img.shape[1] * scale_rate)
    new_height = int(img.shape[0] * scale_rate)
    resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    return resized_img


def cal_scale_rate(origin_bytes, expected_bytes):
    return math.sqrt(expected_bytes / origin_bytes)
