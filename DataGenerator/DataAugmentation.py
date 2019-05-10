from PIL import Image,ImageEnhance
import torch
import torchvision.transforms as transforms
import random
import glob
import numpy as np
import pandas as pd


##dataaugmentationを行う.輝度変更。コントラスト変更。上下左右回転。

def main():
    #ファイルオープン.（注）ファイル内にオリジナルのみにする.同名のcsvも開く

    filePic = glob.glob('./Training_Data/*.png')
    fileCsv = glob.glob('./Training_Data/*.csv')
    for i,j in zip(filePic,fileCsv):
        name = i
        file_start = name.rindex('/')
        file_end = name.rindex('.')
        name = name[file_start + 1:file_end]#ファイル名だけ取得
        originalPic = Image.open(i)
        originalCsv = pd.read_csv(j)
        #コントラスト変更
        contrast = ImageEnhance.Contrast(originalPic)
        contrastPic = contrast.enhance(random.uniform(0.3,1.5))
        contrastCsv = originalCsv
        name = name[0:2]
        contrastCsv.to_csv('./Training_Data/' + name + '1' + '.csv')
        contrastPic.save('./Training_Data/' + name + '1' + '.png')
        #明度変更
        brightness = ImageEnhance.Brightness(originalPic)
        brightnessPic = brightness.enhance(random.uniform(0.3,1.5))
        brightnessCsv = originalCsv
        brightnessCsv.to_csv('./Training_Data/' + name + '2' + '.csv')
        brightnessPic.save('./Training_Data/' + name + '2' + '.png')
        #回転変更
        rotatePic = originalPic.

if __name__ == '__main__':
    main()