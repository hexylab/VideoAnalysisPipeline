# detectors/yolox_detector.py
from ..base_detector import Detector

import cv2
import numpy as np
import torch

from yolox.data.data_augment import preproc
from yolox.data.datasets import COCO_CLASSES
from yolox.exp import get_exp
from yolox.utils import postprocess

class YOLOXDetector(Detector):
    def __init__(self, config_path="./config.yaml"):
        super().__init__(config_path)  # 基底クラスの__init__を呼び出してコンフィグを読み込む
        self.model_path = self.config["model_path"]
        self.input_shape = self.config["input_shape"]
        self.class_score_th = self.config["class_score_th"]
        self.nms_th = self.config["nms_th"]

        self.exp = get_exp(None, "yolox-nano")
        self.model = self.exp.get_model()
        self.model.eval()
        ckpt = torch.load("./yolox_nano.pth", map_location="cpu")
        self.model.load_state_dict(ckpt["model"])


    def detect(self, frame):
        img, r = preproc(frame.image_data, self.input_shape)
        with torch.no_grad():
            outputs = self.model(img)
            outputs = postprocess(outputs,
                                  self.exp.num_classes,
                                  self.class_score_th,
                                  self.nms_th,
                                  class_agnostic=True
                                  )
            if outputs[0] is None:
                return frame
            frame.bboxes = outputs[0][:, 0:4]/r
            class_ids = outputs[0][:, 6]
            for class_id in class_ids:
                frame.classes.append(COCO_CLASSES[class_id])
            frame.scores = outputs[0][:, 4] * outputs[0][:, 5]
            return frame