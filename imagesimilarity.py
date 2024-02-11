# -*- coding: utf-8 -*-
"""imageSimilarity.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JE89BqbnM9V_Tonq5GbjW5kxMYO1f92E
"""

import torch
from torch import nn

"""#Model

##Sub Models
"""

class ConvLayer(nn.Module):
  def __init__(self, input, output, kernal, stride=1):
    super(ConvLayer, self).__init__()
    self.sequential=nn.Sequential(
      nn.Conv2d(input, output, kernal, stride),
      nn.ReLU(),
    )

  def forward(self, input):
    return self.sequential(input)

class LinearLayer(nn.Module):
  def __init__(self, input, output):
    super(LinearLayer, self).__init__()
    self.sequential=nn.Sequential(
      nn.Linear(input, output),
      nn.ReLU(),
    )
  def forward(self, input):
    return self.sequential(input)

"""##Main Model"""

class SiameseModel(nn.Module):
  def __init__(self):
    super(SiameseModel, self).__init__()

    self.sequential=nn.Sequential(
      ConvLayer(3, 64, 11),

      nn.LocalResponseNorm(5,alpha=0.0001,beta=0.75,k=2),

      nn.MaxPool2d(2),

      ConvLayer(64, 64, 5),


      nn.LocalResponseNorm(5,alpha=0.0001,beta=0.75,k=2),

      nn.MaxPool2d(2),

      nn.Dropout(.3),

      ConvLayer(64, 64, 3),

      ConvLayer(64, 64, 3),

      nn.MaxPool2d(2),

      nn.Dropout(.3),

      nn.Flatten(),

      LinearLayer(3481, 1024),
      nn.Dropout(.3),


      LinearLayer(1024, 2)

    )
  def forward(self, image):
    return self.sequential(image)

model=SiameseModel()
image=torch.rand(3,512,512)
model(image).shape