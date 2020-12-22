#!/usr/bin/env python3

from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import time
import os
import glob


class MaskClassifier(CustomVisionPredictionClient):
  def __init__(self):
    PREDICTION_KEY = os.environ["COGNITIVE_CUSTOM_VISION_PREDICTOR_KEY"]
    ENDPOINT = os.environ["COGNITIVE_CUSTOM_VISION_PREDICTOR_ENDPOINT"]
    self.PROJECT_ID = os.environ["COGNITIVE_CUSTOM_VISION_PROJECT_ID"]
    self.ITERATION = os.environ["COGNITIVE_CUSTOM_VISION_PROJECT_ITERATION"]

    prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": PREDICTION_KEY})
    super(MaskClassifier, self).__init__(ENDPOINT, prediction_credentials)

  def classify(self, image):
    results = self.classify_image(
      self.PROJECT_ID,
      self.ITERATION,
      image
    )
    return results


if __name__ == '__main__':
  image_dirs = glob.glob('./test/*.jpg')
  # open all test images
  images = [open(dir, 'r+b') for dir in image_dirs]

  mc = MaskClassifier()
  mc.classify(images[0])