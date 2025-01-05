import os
import shutil
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


month = str(datetime.now().month)
source_parent = "imgs"
cuts_parent = "results/교통비"
source_path = f"{source_parent}/교통비.jpg"
cuts_path = f"{cuts_parent}/{month}월_{{}}_{{}}.png"
result_path = "results/pdfs"

shutil.rmtree(cuts_parent, ignore_errors=True)    # 잘라낸 jpgs 지우기

Path(source_parent).mkdir(parents=True, exist_ok=True)  # 원본 jpg 경로
Path(cuts_parent).mkdir(parents=True, exist_ok=True)    # 잘라낸 jpg 파일들 경로
Path(result_path).mkdir(parents=True, exist_ok=True)    # pdf 결과 경로


# 이미지 파일 불러오기
img_arr = np.fromfile(source_path, np.uint8)
image = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
print(image[:2,:,:])
print(image.shape)
# raise Exception
height = image.shape[0]
interval = 1200
width = image.shape[1]
resize_width = 800

for h in range(0, height, interval):
    s_height = h
    e_height = h + interval
    cropped_image = image[s_height:e_height, 0:width]
    cropped_image = cv2.resize(cropped_image, dsize=(resize_width, interval))
    ret, encoded_img = cv2.imencode(".png", cropped_image)
    print(h, ret)
    if ret:
        with open(cuts_path.format(s_height, e_height), "wb") as f:
            encoded_img.tofile(f)
            
            
images = [cuts_parent + '/' + f for f in os.listdir(cuts_parent)]
images.sort(key=lambda x: int(x.split("_")[1]))     # 가운데 숫자로 정렬
images = [Image.open(image) for image in images]    # 이미지 오픈

images[0].save(
	f"{result_path}/교통비내역.pdf", "PDF", resolution=100.0, save_all=True, append_images=images[1:]
)