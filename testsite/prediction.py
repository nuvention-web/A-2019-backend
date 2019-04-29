import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0, 1'
import numpy as np
from PIL import Image
import torch
import torch.nn as nn
import torch.nn.parallel
import torch.utils.data
from torch.autograd import Variable
import torchvision.transforms as transforms

def predict(tasks, img_paths):
    # Label
    label_dict = {
    "collar_design_labels" : ["Invisible", "Shirt Collar", "Peter Pan", "Puritan Collar", "Rib Collar"],
    "skirt_length_labels" : ["Invisible", "Short Length", "Knee Length", "Midi Length", "Ankle Length", "Floor Length"],
    "coat_length_labels" : ["Invisible", "High Waist Length", "Regular Length", "Long Length", "Micro Length", "Knee Length", "Midi Length", "Ankle&Floor Length"],
    "lapel_design_labels" : ["Invisible", "Notched", "Collarless", "Shawl Collar", "Plus Size Shawl"],
    "neck_design_labels" : ["Invisible", "Turtle Neck", "Ruffle Semi-High Collar", "Low Turtle Neck", "Draped Collar"],
    "neckline_design_labels" : ["Invisible", "Strapless Neck", "Deep V Neckline", "Straight Neck", "V Neckline", "Square Neckline", "Off Shoulder", "Round Neckline", "Sweat Heart Neck", "One Shoulder Neckline"],
    "pant_length_labels" : ["Invisible", "Short Pant", "Mid Length", "3/4 Length", "Cropped Pant", "Full Length"],
    "sleeve_length_labels" : ["Invisible", "Sleeveless", "Cup Sleeves", "Short Sleeves", "Elbow Sleeves", "3/4 Sleeves", "Wrist Length", "Long Sleeves", "Extra Long Sleeves"]
    }

    models = {}
    for task in tasks:
        # Load model
        saved_model = 'checkpoint/' + task + '_model.pkl'
        net = torch.load(saved_model)
        print('net => ')
        print(net)
        if torch.cuda.is_available() == True:
            net.cuda()

        models[task] = net

    res = []

    for img in img_paths:

        attr = {}

        for task in tasks:

            # Load model
            # saved_model = 'checkpoint/' + task + '_model.pkl'
            # net = torch.load(saved_model)
            # if torch.cuda.is_available() == True:
            #     net.cuda()
            net = models[task]

            # data
            pred_transform = transforms.Compose([
                transforms.Resize(512),
                transforms.CenterCrop(500),
                transforms.ToTensor(),
                transforms.Normalize(mean=(0.5, 0.5, 0.5),
                                     std=(0.5, 0.5, 0.5))])

            # root = "./pred_pic"
            # img_file = []

            # for file in os.listdir(root):
            #     file_path = os.path.join(root, file)
            #     if os.path.isdir(file_path):
            #         pass
            #     else:
            #         img_file.append(file)


            net.eval()

            softmax = nn.Softmax(dim=1)
            # for img in img_path:
            # img_path = os.path.join(root, img)
            image = Image.open(img)
            image = pred_transform(image)
            image = image.unsqueeze_(0)
            out = net(Variable(image.cuda()))
            out = softmax(out)
            _, pred_out = torch.max(out.data, 1)
            attr[task] = label_dict[task][pred_out]

                # line_out = ','.join([img, task, label_dict[task][pred_out]])

                # with open("./pred_res/result.txt", "a+") as f_out:
                #     f_out.write(line_out + '\n')

            # print('Submission for %s is done!!!' % task)
        res.append(attr)

    return res

if __name__ == '__main__':
    # task_list = ['collar_design_labels', 'skirt_length_labels', 'lapel_design_labels',
    #              'neckline_design_labels', 'coat_length_labels', 'neck_design_labels',
    #              'pant_length_labels', 'sleeve_length_labels']

    task_list = ['collar_design_labels', 'skirt_length_labels']

    for task in task_list:
        predict(task)

    #
    res = predict(["collar_design_labels", "skirt_length_labels"], ["trousers_red.png"])