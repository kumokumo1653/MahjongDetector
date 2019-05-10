from PIL import Image,ImageDraw
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
times = 3
for j in range(times):
    # xmlファイルを生成
    xml = ET.Element('Annotations')
    folder = ET.SubElement(xml, 'folder')
    folder.text = 'data'
    fileName = ET.SubElement(xml, 'fileName')
    size = ET.SubElement(xml, 'size')
    width = ET.SubElement(size, 'width')
    width.text = str(backgroud.width)
    height = ET.SubElement(size, 'height')
    height.text = str(backgroud.height)
    depth = ET.SubElement(size, 'depth')
    depth.text = '3'
    rate = random.uniform(0.5,3)
    bg = backgroud.copy()
    x,y=random.randrange(0,100),random.randrange(100,400)
    i=0
    data = []
    while x<430:
        pai = random.choice(Pai)
        pai_image = pai[0]
        pai_image = pai_image.resize((int(30*rate),int(40*rate)))
        if i is not 0:
            x, y = int(x + pai_image.width / 2), int(random.uniform(y - 5, y + 5))
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

        theta = math.radians(-30)
        dimension = ((bg.width * math.sin(-theta) + bg.height * math.cos(-theta)))/2
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
    fileName.text = str(j)+'00.png'
    theta = math.degrees(theta)*-1
    bg = bg.rotate(theta,expand=True,resample=Image.BICUBIC)
    print(bg.size)
    draw = ImageDraw.Draw(bg)
    for i in data:
        #print(i)
        draw.rectangle((i[0],i[1],i[2],i[3]),outline=(256,256,256))

    num = str(j)
    num = num.zfill(6)
    bg.save('../data/Imagedata/'+num+'.jpg')
    annotation = md.parseString(ET.tostring(xml,'utf-8'))
    file = open('../data/Annotations/'+num+'.xml','w')
    annotation.writexml(file, encoding='utf-8', newl='\n', indent='', addindent='  ')
