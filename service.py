from image_process import resize_img
from PIL import Image
import io
import cv2


def get_io_obj(img, scale_rate):
    img_dst = resize_img(img, scale_rate)
    # convert to Image
    img_dst = Image.fromarray(cv2.cvtColor(img_dst, cv2.COLOR_BGR2RGB))
    img_io = io.BytesIO()
    img_dst.save(img_io, 'PNG')
    return img_io
