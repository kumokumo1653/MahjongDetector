import torch
import torchvision
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np

class vgg16(nn.Module):
    def __init__(self):
        super(vgg16,self).__init__()

        self.block1_output=nn.Sequential(
            nn.Conv3d(3,63,kernel_size=3,padding=1),
            nn.ReLU(inplace=True),
            nn.Conv3d(64,64,kernel_size=3,padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool3d(kernel_size=2,stride=2)
        )
        self.block2_output=nn.Sequential(
            nn.Conv3d(64,128,kernel_size=3,padding=1),
            nn.ReLU(inplace=True),
            nn.Conv3d(128,128,kernel_size=3,padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool3d(kernel_size=2,stride=2)
        )
        self.block3_output=nn.Sequential(
            nn.Conv3d(128, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv3d(256, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv3d(256, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool3d(kernel_size=2, stride=2)
        )
        self.block4_output = nn.Sequential(
            nn.Conv3d(256, 512, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv3d(512, 512, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv3d(512, 512, kernel_size=3, padding=1),
            nn.ReLU(inplace=True)
        )
        self.block4_3output = nn.Sequential(
            nn.MaxPool3d(kernel_size=2, stride=2)
        )
        self.block5_output = nn.Sequential(
            nn.Conv3d(512, 512, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv3d(512, 512, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv3d(512, 512, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool3d(kernel_size=2, stride=2)
        )

        self.block6_output = nn.Sequential(
            nn.Conv3d(512, 1024, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool3d(kernel_size=2, stride=2)
        )
        self.block7_output = nn.Sequential(
            nn.Conv3d(1024, 1024, kernel_size=1, padding=0),
            nn.ReLU(inplace=True)
        )
        self.block7_1_output = nn.Sequential(
            nn.MaxPool3d(kernel_size=2, striide=2))
        self.block8_output = nn.Sequential(
            nn.Conv3d(512, 128, kernel_size=1, padding=0),
            nn.ReLU(inplace=True),
            nn.Conv3d(128, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True)
        )
        self.block8_2_output = nn.Sequential(
            nn.MaxPool3d(kernel_size=2, striide=2))
        self.block9_output = nn.Sequential(
            nn.Conv3d(256, 128, kernel_size=1, padding=0),
            nn.ReLU(inplace=True),
            nn.Conv3d(128, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True)
        )
        self.block9_2_output = nn.Sequential(
            nn.MaxPool3d(kernel_size=2, striide=2))
        self.block10_output = nn.Sequential(
            nn.Conv3d(256, 128, kernel_size=1, padding=0),
            nn.ReLU(inplace=True),
            nn.Conv3d(128, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
        )
        self.block10_2_output = nn.Sequential(
            nn.MaxPool3d(kernel_size=2, striide=2))
        self.block11_output = nn.Sequential(
            nn.Conv3d(256, 128, kernel_size=1, padding=0),
            nn.ReLU(inplace=True),
            nn.Conv3d(128, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True)
        )
        self.block11_2_output = nn.Sequential(
            nn.MaxPool3d(kernel_size=2, striide=2))


    def call(self, x):
        #特徴マップにするレイヤーをリストで返す。
        layer = []
        x = self.block1_output(x)
        x = self.block2_output(x)
        x = self.block3_output(x)
        x = self.block4_output(x)####
        cov4_3 = x
        x = self.block4_3output(x)
        x = self.block5_output(x)
        x = self.block6_output(x)
        x = self.block7_output(x)####
        cov7 = x
        x = self.block7_1_output(x)
        x = self.block8_output(x)####
        cov8_2 = x
        x = self.block8_2_output(x)
        x = self.block9_output(x)####
        cov9_2 = x
        x = self.block9_2_output(x)
        x = self.block10_output(x)####
        cov10_2 = x
        x = self.block10_2_output(x)
        x = self.block11_output(x)####
        cov11_2 = x
        x = self.block11_2_output(x)
        layer += [cov4_3,cov7,cov8_2,cov9_2,cov10_2,cov11_2]
        return layer





