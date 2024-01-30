from flask import Flask, request, send_file
from image_process import cal_scale_rate
from util import cal_bytes
import numpy as np
import cv2
from service import get_io_obj

app = Flask(__name__)


@app.route('/test')
def test():
    return 'Hello World'


@app.route('/process', methods=['POST'])
def process():
    global img_io
    size = float(request.args.get('size'))
    unit = request.args.get('unit')
    mode = request.args.get('mode')

    # convert string of image data to uint8
    nparr = np.fromstring(request.data, np.uint8)
    # decode image
    img_src = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    origin_bytes = request.content_length
    expected_bytes = cal_bytes(size, unit)

    # 参数校验
    if mode == 'compress' and origin_bytes <= expected_bytes:
        return 'Already compressed'
    if mode == 'expand' and origin_bytes >= expected_bytes:
        return 'Already expanded'

    retry_cnt = 5
    scale_rate = cal_scale_rate(origin_bytes, expected_bytes)
    while retry_cnt > 0:
        img_io = get_io_obj(img_src, scale_rate)
        actual_bytes = img_io.tell()
        if mode == 'compress':
            if actual_bytes >= expected_bytes:
                scale_rate = scale_rate * 0.8
            else:
                break
        if mode == 'expand':
            if actual_bytes <= expected_bytes:
                scale_rate = scale_rate * 1.2
            else:
                break
        retry_cnt = retry_cnt - 1

    if retry_cnt == 0:
        return 'Server error'

    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')


if __name__ == '__main__':
    app.run()
