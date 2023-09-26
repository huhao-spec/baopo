import json
import os

import torch
from PIL import Image
from torchvision import transforms

from model_mobile_net import efficientnet_b0 as create_model


def yuce(root):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    data_transform = transforms.Compose(
        [transforms.Resize(224),
         transforms.CenterCrop(224),
         transforms.ToTensor(),
         transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])

    # load image
    img_path = root
    img = Image.open(img_path)
    # [N, C, H, W]
    img = data_transform(img)
    # expand batch dimension
    img = torch.unsqueeze(img, dim=0)

    # read class_indict
    json_path = 'class_indices.json'
    with open(json_path, "r") as f:
        class_indict = json.load(f)

    # create model
    model = create_model(num_classes=3).to(device)

    # load model weights
    model_weight_path = "D:/undergrate_project/rongyexijing/weights/0.997.pth"
    model.load_state_dict(torch.load(model_weight_path, map_location=device))
    model.eval()
    with torch.no_grad():
        # predict class
        output = torch.squeeze(model(img.to(device))).cpu()
        predict = torch.softmax(output, dim=0)
        predict_cla = torch.argmax(predict).numpy()
    print_res = "class: {}".format(class_indict[str(predict_cla)])
    print(print_res)
    return print_res
