'''
code by hh2023-8-20
pip install thop
'''
import torch
from thop import profile

from model_mobile_net import MobileNetV2 as create_model

device = torch.device("cuda")
# input_shape of model,batch_size=1
net = create_model()

input = torch.randn(1, 3, 224, 224)
flops, params = profile(net, inputs=(input,))

print("FLOPs=", str(flops / 1e9) + '{}'.format("G"))
print("params=", str(params / 1e6) + '{}'.format("M"))