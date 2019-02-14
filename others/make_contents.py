#coding:utf-8

import os # os操作
import shutil # ファイルコピー
from PIL import Image # 画像情報を取得
import PIL.ExifTags as ExifTags
import reverse_geocoder as rg
import random
import string

# 関数の定義
def make_contents():
    print('start make contents!')

    num = 0
    old_time = "0000-00-00"

    imagesPath = '../static/images/'
    os.makedirs(imagesPath)
    while num < 146:
        name = '{}-{:0=5}'.format('hitchhike', num) # nameの作成
        dirpath = '../content/' + name
        picpath = '../content/' + name + '/' + name + '.jpg'
        pic = '/Users/hirotatsu/work/dev/hitchhike-memories/others/hitchhike/' + name +'.jpg'

        os.makedirs(dirpath) # ディレクトリの作成

        shutil.copy(pic, imagesPath) #ファイルコピー

        # EXIF情報を得る
        im = Image.open(pic)

        exif = {
            ExifTags.TAGS[k]: v
            for k, v in im._getexif().items()
            if k in ExifTags.TAGS
        }

        # 日付の取得
        def get_time (exif):
            if ('DateTimeOriginal' in exif):
                time = exif["DateTimeOriginal"]
                old_time = time
                return time.replace(':', '-')[:10]
            return ''

        time = get_time (exif)
        if time == '':
            time = old_time

        # GPS情報の取得
        def get_gps (exif):
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
                return area['cc'], area['admin1'] + ' ' + area['name']
            return '', ''

        country, location = get_gps (exif)

        # mdxに書き込む情報
        contents = [
            '+++\n',
            'albumthumb = "/images/' + name + '.jpg"\n',
            'title = "' + location + ' , ' + country + '"\n',
            'date = "' + time + '"\n',
            '+++\n'
        ]

        # ファイルを作成して書き込む
        f = open(dirpath + '/_index.md', 'w', encoding='utf-8')
        f.writelines(contents)
        f.close()

        # numに1をプラスする
        num+=1

    print('end make contents!')

# 関数の実行
make_contents()