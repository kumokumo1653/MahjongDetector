from PIL import Image,ImageDraw,ImageEnhance,ImageMath
import random
import glob
import numpy as np
import math
#import pandas as pd
import xml.etree.ElementTree as ET
import xml.dom.minidom as md
#背景描画
backgroud = Image.new('RGB',(610,610),(60,180,110))
draw = ImageDraw.Draw(backgroud)


#各牌のテンプレ画像をオープンしてリサイズ。257:349=60:80
Pai = []
name = ""
files = glob.glob('./Picture_Data/*.png')
for i in files:
    name = i
    file_start = name.rindex('/')
    file_end = name.rindex('.')
    name = name[file_start+1:file_end]

    pai = Image.open(i)
    i = name
    pai = pai.resize((60,80))
    Pai.append([pai,i])
#牌を並べる.ランダムに画像を小さくして横に並べる最低7枚。最初の位置を0から100で決定
times = 10000
for j in range(times):
    # xmlファイルを生成
    xml = ET.Element('Annotations')
    folder = ET.SubElement(xml, 'folder')
    folder.text = 'MJdata'
    fileName = ET.SubElement(xml, 'fileName')
    size = ET.SubElement(xml, 'size')
    width = ET.SubElement(size, 'width')
    height = ET.SubElement(size, 'height')
    depth = ET.SubElement(size, 'depth')
    depth.text = '3'
    rate = random.uniform(0.8,3)
    bg = backgroud.copy()
    x,y=random.randrange(0,100),random.randrange(100,400)
    i=0
    data = []
    theta = math.radians(random.uniform(0, 360))
    while x<430:
        pai = random.choice(Pai)
        pai_image = pai[0]
        pai_image = pai_image.resize((int(30*rate),int(40*rate)))
        #hsv変更
        h,s,v = pai_image.convert("HSV").split()
        delta_h = random.randrange(-25,25)
        delta_s = random.randrange(-25,25)
        delta_v = random.randrange(-25,25)
        h,s,v = ImageMath.eval("h + delta_h",h=h,delta_h = delta_h).convert("L"), \
                ImageMath.eval("s + delta_s",s=s,delta_s = delta_s).convert("L"),\
                ImageMath.eval("v + delta_v",v=v,delta_v = delta_v).convert("L")
        pai_image = Image.merge("HSV",(h,s,v)).convert("RGB")
        #コントラスト変更
        enhancer = ImageEnhance.Brightness(pai_image)
        pai_image = enhancer.enhance(random.uniform(0.5,1.5))
        if i is not 0:
            x, y = int(x + pai_image.width / 2 + random.randrange(0,10)), int(random.uniform(y - 5, y + 5))
        bg.paste(pai_image, (x, y))


        xmn = int(x)
        ymn = int(y)
        xur = int(xmn + pai_image.width)
        yur = int(y)
        xdl = int(x)
        ydl = int(ymn + pai_image.height)
        xmx = int(xmn + pai_image.width)
        ymx = int(ymn + pai_image.height)
        points = [[xmn,ymn],[xur,yur],[xdl,ydl],[xmx,ymx]]
        i += 1
        x, y = int(x + pai_image.width / 2), int(random.uniform(y - 5, y + 5))
        object = ET.SubElement(xml,'object')
        name = ET.SubElement(object,'name')
        name.text = str(pai[1])
        difficult = ET.SubElement(object,'difficult')
        difficult.text = '0'
        bndbox = ET.SubElement(object,'bndbox')
        #回転


        dimension = ((bg.width * abs(math.sin(theta)) + bg.height * abs(math.cos(theta))))/2
        ｒotationMatrix = np.matrix([[math.cos(theta), -1*math.sin(theta)],
                                    [math.sin(theta), math.cos(theta)]])
        quadx = []
        quady = []
        for k in points:
            point = np.matrix([[k[0] - bg.width / 2], [k[1] - bg.height / 2]])
            k[0],k[1] = rotationMatrix * point
            k[0] += dimension
            k[1] += dimension
            quadx.append(int(k[0]))
            quady.append(int(k[1]))
        #print(xy)
        xMin = min(quadx)
        yMin = min(quady)
        xMax = max(quadx)
        yMax = max(quady)
        #print(type(xMin))
        data.append([xMin,yMin,xMax,yMax])
        xmin = ET.SubElement(bndbox,'xmin')
        xmin.text = str(xMin)
        ymin = ET.SubElement(bndbox,'ymin')
        ymin.text = str(yMin)
        xmax = ET.SubElement(bndbox,'xmax')
        xmax.text = str(xMax)
        ymax = ET.SubElement(bndbox,'ymax')
        ymax.text = str(yMax)

    theta = math.degrees(-theta)
    bg = bg.rotate(theta,expand=True,resample=Image.BICUBIC)

    draw = ImageDraw.Draw(bg)
    #for i in data:
        #print(i)
     #   draw.rectangle((i[0],i[1],i[2],i[3]),outline=(256,256,256))

    num = str(j)
    num = num.zfill(6)
    fileName.text = num + '.jpg'
    width.text = str(bg.width)
    height.text = str(bg.height)
    bg.save('../data/JPEGImages/'+num+'.jpg')
    annotation = md.parseString(ET.tostring(xml,'utf-8'))
    file = open('../data/Annotations/'+num+'.xml','w')
    annotation.writexml(file, encoding='utf-8', newl='\n', indent='', addindent='  ')

    #debug
    '''f_pixel = open('../data/ImageSets/pixel.txt','a')
    for x in range(bg.size[0]):
        for y in range(bg.size[1]):
            r,g,b = bg.getpixel((x,y))
            if (not (type(x) is  int) or not(type(y) is int) or not(type(r) is int) or not(type(g) is int) or not(type(b) is int)):
                print("エラー")
            f_pixel.write(str(x)+','+str(y)+':'+str(r)+','+str(g)+','+str(b)+' ')
        f_pixel.write('\n')
    '''
#画像セットの作成
'''
trainval　全部
train　　　trainvalの4/5
val       trainvalの1/5
test　　　使わない
'''
f_trainval = open('../data/ImageSets/trainval.txt','w')
f_train = open('../data/ImageSets/train.txt', 'w')
f_val = open('../data/ImageSets/val.txt', 'w')
for i in range(10000):
    if (random.choice([True,True,True,True,False])):
        f_train.write(str(i).zfill(6) + '\n')
    else:
        f_val.write(str(i).zfill(6) + '\n')
    f_trainval.write(str(i).zfill(6) + '\n')


f_trainval.close()
f_train.close()
f_val.close()