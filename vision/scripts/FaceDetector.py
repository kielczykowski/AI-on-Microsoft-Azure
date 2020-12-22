#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont
import os
import glob
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face import FaceClient

class FaceDetector(FaceClient):
  def __init__(self):
    SUBSCRIPTION_KEY = os.environ["COGNITIVE_FACE_API_KEY"]
    ENDPOINT = os.environ["COGNITIVE_FACE_API_ENDPOINT"]
    credential = CognitiveServicesCredentials(SUBSCRIPTION_KEY)
    super(FaceDetector, self).__init__(ENDPOINT, credential)

  def detectFaceFeatures(self, image_list):
    face_features = []
    for image in image_list:
      face_features.append(self.face.detect_with_stream(image, detection_model='detection_02'))
    return face_features

class ImagePresenter:
  def drawDetectedFaces(self, features, image_dirs):
    for i,elem in enumerate(features):
      if not elem:
        print('no face found in {} image, skipping'.format(image_dirs[i]))
        continue
      img = Image.open(image_dirs[i])
      for e in elem:
        image_presenter.drawROI(img, e.face_rectangle)
      img.show()
      input("Press Enter to continue...")

  def getPILROI(self, roi_raw):
    left, top = roi_raw.left, roi_raw.top
    right, bottom = left + roi_raw.width, top + roi_raw.height
    return (left, top, right, bottom)

  def drawROI(self, image, roi, color = 'green'):
    draw = ImageDraw.Draw(image)
    left, top = roi.left, roi.top
    right, bottom = left + roi.width, top + roi.height
    draw.rectangle(((left,top), (right, bottom)), outline=color)
    return image

  def drawTextOnImage(self, image, roi, text='', color='green'):
    draw = ImageDraw.Draw(image)
    left, top = roi.left, roi.top
    draw.text((left, top), text, fill=color)
    return image


if __name__ == '__main__':
  # get all test images paths
  image_dirs = glob.glob('./test/*.jpg')
  # open all test images
  images = [open(dir, 'r+b') for dir in image_dirs]

  face_detector = FaceDetector()
  # create detection for every face
  features = face_detector.detectFaceFeatures(images)


  image_presenter = ImagePresenter()
  image_presenter.drawDetectedFaces(features, image_dirs)