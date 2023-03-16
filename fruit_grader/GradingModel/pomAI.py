from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.utils.visualizer import ColorMode, Visualizer
from detectron2 import model_zoo

import cv2

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


def model_load():
    # load model and merge on coco instance segmentation
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = .7  # Set threshold for the model
    cfg.MODEL.WEIGHTS = os.path.dirname(os.path.realpath(__file__)) + '\model_final.pth'  # load model_final.pth
    cfg.MODEL.DEVICE = "cpu"  # cpu or gpu
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 5

    predictor = DefaultPredictor(cfg)

    metadata = MetadataCatalog.get("pomegranate_classes").set(thing_classes=['1', '2', '3', '4', '5'])

    return predictor, metadata


def model_inference(imagePath):
    predictor, metadata = model_load()

    image = cv2.imread(imagePath)
    predictions = predictor(image)

    viz = Visualizer(
        image[:, :, ::-1],
        metadata=metadata,
        scale=0.8,
        instance_mode=ColorMode.IMAGE_BW
    )

    output_mode = viz.draw_instance_predictions(predictions['instances'].to('cpu'))
    res = output_mode.get_image()[:, :, ::-1]

    # get score
    score = str(predictions["instances"].scores)
    score = score[score.find("[") + 1: score.find("]")].split(", ")
    score = [round(float(x) * 100) for x in score]

    # get grade
    label = str(predictions["instances"].pred_classes + 1)
    label = label[label.find("[") + 1: label.find("]")].split(", ")

    return res, score[0], label[0]


if __name__ == '__main__':
    imagePath = 'pom_img.jpg'
    res, score, label = model_inference(imagePath)

    print(score)
    print(label)

    # cv2.imshow('image window', res)
    # cv2.waitKey()
    # print(os.path.dirname(os.path.realpath(__file__)))
