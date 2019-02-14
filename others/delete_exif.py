from PIL import Image

def delete_exif():
    print('start delete exif!')
    imagesPath = '../static/images/'

    num = 0

    while num < 146:

        name = '{}-{:0=5}'.format('hitchhike', num + 1)
        path = imagesPath + name + '.jpg'

        print(path)

        with Image.open(path) as src:
            data = src.getdata()
            mode = src.mode
            size = src.size

        with Image.new(mode, size) as dst:
            dst.putdata(data)
            dst.save(path)

        num+=1

    print('end delete exif!')

delete_exif()