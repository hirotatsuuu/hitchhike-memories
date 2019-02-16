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

    if (size > 100000):
        scaled = cv2.resize(img, dsize=(int(img.shape[1] / 8), int(img.shape[0] / 8)))
        print('{} -> {}'.format(img.shape, scaled.shape))
        cv2.imwrite(f.stem + '-thumb.jpg', scaled)
    else:
        scaled = cv2.resize(img, dsize=(int(img.shape[1] / 4), int(img.shape[0] / 4)))
        print('{} -> {}'.format(img.shape, scaled.shape))
        cv2.imwrite(f.stem + '-thumb.jpg', scaled)
