from PIL import Image,ImageDraw,ImageEnhance,ImageMath
import glob


files = glob.glob('../data/JPEGImages/*.jpg')
f_pixel = open('../data/ImageSets/pixel.txt','a')
for i in files:
    pic = Image.open(i)
    for x in range(pic.size[0]):
        for y in range(pic.size[1]):
            r,g,b = pic.getpixel((x,y))
            if (not (type(x) is  int) or not(type(y) is int) or not(type(r) is int) or not(type(g) is int) or not(type(b) is int)):
                print("エラー")
            f_pixel.write(str(x) + ',' + str(y) + ':' + str(r) + ',' + str(g) + ',' + str(b) + ' ')
        f_pixel.write('\n')

f_pixel.close()