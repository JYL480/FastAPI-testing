import torch
import torchvision

from torch import nn
from timeit import default_timer as timer
from PIL import Image

def createModel(num_classes = 3, seed_int = 42):
    # We are using the efficientnet_b2 model!!
    weights = torchvision.models.EfficientNet_B2_Weights.DEFAULT
    transforms = weights.transforms()
    model = torchvision.models.efficientnet_b2(weights=weights)

        # Freeze all layers in base model
    for param in model.parameters():
        param.requires_grad = False
    

    torch.manual_seed(seed_int)
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.3, inplace=True),
        nn.Linear(in_features=1408, out_features=num_classes),
    )
    

    # Will return the model and transforms!!
    return model, transforms

def predictImg(img_path):
    class_names = ["pizza", "steak", "sushi"]
    model, transformation = createModel()
    model.load_state_dict(
    torch.load(
        f="model/09_pretrained_effnetb2_feature_extractor_pizza_steak_sushi_20_percent.pth",
        map_location=torch.device("cpu"),  # load to CPU
    )
)

    # img_tensor = transformation(img).unsqueeze(0)
    start_time = timer()
    # Lol the Image has 4 channels, you have to covert to RGB!!
    img = Image.open(img_path).convert('RGB')
    img_trans = transformation(img).unsqueeze(0)
    # print(img_trans.shape)

    model.eval()
    with torch.inference_mode():
        pred = torch.softmax(model(img_trans), dim=1)
        pred_label = torch.argmax(pred, dim=1)
    pred_time = round(timer() - start_time, 5)
    return class_names[pred_label] ,pred_time
    