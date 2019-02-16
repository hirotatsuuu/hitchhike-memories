# -*- coding: utf-8 -*-
import cv2
import os
from pathlib import Path

images_path = '.'
for f in Path(images_path).rglob('*.jpg'):
    print(f.name)

    img = cv2.imread(f.name)
    print('original size:', img.shape, img.shape[0])
    size = os.path.getsize(f.name)
    print('size: ', size)

    if (size > 1000000):
        scaled = cv2.resize(img, dsize=(int(img.shape[1] / 16), int(img.shape[0] / 16)))
    elif (size > 700000):
        scaled = cv2.resize(img, dsize=(int(img.shape[1] / 14), int(img.shape[0] / 14)))
    elif (size > 500000):
        scaled = cv2.resize(img, dsize=(int(img.shape[1] / 12), int(img.shape[0] / 12)))
    elif (size > 300000):
        scaled = cv2.resize(img, dsize=(int(img.shape[1] / 8), int(img.shape[0] / 12)))
    elif (size > 100000):
        scaled = cv2.resize(img, dsize=(int(img.shape[1] / 6), int(img.shape[0] / 6)))
    else:
        scaled = cv2.resize(img, dsize=(int(img.shape[1] / 4), int(img.shape[0] / 4)))
    print('{} -> {}'.format(img.shape, scaled.shape))
    cv2.imwrite(f.stem + '-thumb.jpg', scaled)