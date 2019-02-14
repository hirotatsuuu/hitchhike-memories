#coding:utf-8

import os # os操作
import shutil # ファイルコピー
from PIL import Image # 画像情報を取得
import PIL.ExifTags as ExifTags
import reverse_geocoder as rg
import string
from pathlib import Path
import glob

# 最新プラス1の値を取得
def get_leatest_num ():
    images_path = '../static/images/'
    list = []

    for f in Path(images_path).rglob('*.jpg'):
        list.append(f.stem)
    list.sort()
    return int(list[-1][-5:]) + 1

def new_post ():
    num = 0
    images_path = '../static/images/'
    photos_path = './hitchhike/'
    old_photos_path = './old/'

    # 写真の数の取得
    photo_num = len(glob.glob(photos_path + '*'))

    leatest_num = get_leatest_num()

    # 写真のリネーム
    photo_name_num = leatest_num
    for f in Path(photos_path).rglob('*'):
        f.rename(photos_path + '{}-{:0=5}'.format('hitchhike', photo_name_num) + '.jpg')
        photo_name_num += 1

    while num < photo_num:
        # ファイル名の格納
        name = '{}-{:0=5}'.format('hitchhike', leatest_num)

        # 記事ディレクトリの作成
        content_path = '../content/' + name
        os.makedirs(content_path)

        for f in Path(photos_path).rglob('*'):
            if (f.stem == name):
                # exifの取得
                im = Image.open(photos_path + f.name)

                exif = {
                    ExifTags.TAGS[k]: v
                    for k, v in im._getexif().items()
                    if k in ExifTags.TAGS
                }

                # 日付情報の取得
                if ('DateTimeOriginal' in exif):
                    date = exif["DateTimeOriginal"]

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

                # 記事内の文章の作成
                contents = [
                    '+++\n',
                    'albumthumb = "/images/' + name + '.jpg"\n',
                    'title = "' + title + '"\n',
                    'date = "' + date + '"\n',
                    'weight = ' + str(leatest_num) + '\n',
                    '+++\n'
                ]

                # _index.mdの作成及び内容の書き込み
                f = open(content_path + '/_index.md', 'w', encoding='utf-8')
                f.writelines(contents)
                f.close()

                # 写真のコピー
                shutil.copy(photos_path + name + '.jpg', images_path)

                # 写真の移動
                shutil.move(photos_path + name + '.jpg', old_photos_path)

                # exif情報の削除
                with Image.open(images_path + name + '.jpg') as src:
                    data = src.getdata()
                    mode = src.mode
                    size = src.size

                with Image.new(mode, size) as dst:
                    dst.putdata(data)
                    dst.save(images_path + name + '.jpg')

        num+=1
        leatest_num+=1

new_post()