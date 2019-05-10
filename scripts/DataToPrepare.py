import torch
import torchvision.transforms as transforms
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np


class Data_transforms():
    #imageはPILimageで渡す
    def __init__(self,image):
        self.image = image
