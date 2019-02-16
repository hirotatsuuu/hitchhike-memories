#coding:utf-8

import os
import string
import shutil # ファイルの移動やコピーのため
import glob
import cv2 # 画像圧縮のため
from pathlib import Path
from PIL import Image # exif情報の処理のため
import PIL.ExifTags as ExifTags # exif情報の処理のため
import reverse_geocoder as rg # 位置情報処理のため

def new_post ():
    print('Start new_post Function')
    print('*********************************')

    num = 0 # 処理の回数
    images_path = '../static/images/' # 写真を格納する場所
    photos_path = './hitchhike/' # 新しい写真を格納する場所
    old_photos_path = './old/' # 処理が終わった写真を格納する場所

    # 写真の数の取得
    photos_num = len(glob.glob(photos_path + '*'))
    print('photos_num: ', photos_num)

    # 最新プラス1の値を取得
    list = []
    for f in Path(images_path).rglob('hitchhike-[0-9][0-9][0-9][0-9][0-9].jpg'):
        list.append(f.stem)
    list.sort()
    leatest_num = int(list[-1][-5:]) + 1
    print('leatest_num: ', leatest_num)

    # 写真のリネーム
    photo_name_num = leatest_num
    for f in Path(photos_path).rglob('*'):
        f.rename(photos_path + '{}-{:0=5}'.format('hitchhike', photo_name_num) + '.jpg')
        photo_name_num += 1
    print('Fin rename')

    while num < photos_num:
        file_name = '{}-{:0=5}'.format('hitchhike', leatest_num)
        photo_name = photos_path + file_name + '.jpg'
        photo_name_thumb = photos_path + file_name + '-thumb.jpg'

        # 記事ディレクトリの作成
        content_path = '../content/' + file_name
        os.makedirs(content_path)

        for f in Path(photos_path).rglob('*'):
            if (f.stem == file_name):
                # exifの取得
                img = Image.open(photos_path + f.name)
                exif = {
                    ExifTags.TAGS[k]: v
                    for k, v in img._getexif().items()
                    if k in ExifTags.TAGS
                }

                # 日付情報の取得
                if ('DateTimeOriginal' in exif):
                    date = exif["DateTimeOriginal"]
                print('Date: ', date)

                # GPS情報の取得
                if ('GPSInfo' in exif):
                    gps_tags = exif["GPSInfo"]
                    gps = {
                        ExifTags.GPSTAGS.get(t, t): gps_tags[t]
                        for t in gps_tags
                    }
                    def conv_deg(v):
                        d = float(v[0][0]) / float(v[0][1])
                        m = float(v[1][0]) / float(v[1][1])
                        s = float(v[2][0]) / float(v[2][1])
                        return d + (m / 60.0) + (s / 3600.0)
                    lat = conv_deg(gps["GPSLatitude"])
                    lat_ref = gps["GPSLatitudeRef"]
                    if lat_ref != "N": lat = 0 - lat
                    lon = conv_deg(gps["GPSLongitude"])
                    lon_ref = gps["GPSLongitudeRef"]
                    if lon_ref != "E": lon = 0 - lon
                    results = rg.search([(lat, lon)])
                    area = {t: results[0][t] for t in results[0]}
                    title = area['admin1'] + ' ' + area['name'] + ' , ' + area['cc']
                print('Title: ', title)

                # 記事内の文章の作成
                contents = [
                    '+++\n',
                    'thumb = "/images/' + file_name + '-thumb.jpg"\n',
                    'albumthumb = "/images/' + file_name + '.jpg"\n',
                    'title = "' + title + '"\n',
                    'date = "' + date + '"\n',
                    'weight = ' + str(leatest_num) + '\n',
                    '+++\n'
                ]

                # _index.mdの作成及び内容の書き込み
                f = open(content_path + '/_index.md', 'w', encoding='utf-8')
                f.writelines(contents)
                f.close()

                # 写真の圧縮
                img = cv2.imread(photo_name)
                size = os.path.getsize(photo_name)

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
                cv2.imwrite(photo_name_thumb, scaled)

                # 写真のコピー
                shutil.copy(photo_name, images_path)
                shutil.copy(photo_name_thumb, images_path)

                # 写真の移動
                shutil.move(photo_name, old_photos_path)
                shutil.move(photo_name_thumb, old_photos_path)

                # exif情報の削除
                with Image.open(images_path + file_name + '.jpg') as src:
                    data = src.getdata()
                    mode = src.mode
                    size = src.size
                with Image.new(mode, size) as dst:
                    dst.putdata(data)
                    dst.save(images_path + file_name + '.jpg')
                print('Fin: ', file_name)

        num+=1
        leatest_num+=1

    print('*********************************')
    print('End new_post Function')

new_post()