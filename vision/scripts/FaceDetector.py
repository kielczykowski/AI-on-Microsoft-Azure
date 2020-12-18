#!/usr/bin/env python3

from PIL import Image, ImageDraw
import os
import glob
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face import FaceClient

class FaceDetector(FaceClient):
  def __init__(self):
    SUBSCRIPTION_KEY = os.environ["COGNITIVE_SERVICE_KEY"]
    ENDPOINT = os.environ["COGNITIVE_SERVICE_ENDPOINT"]
    credential = CognitiveServicesCredentials(SUBSCRIPTION_KEY)
    super(FaceDetector, self).__init__(ENDPOINT, credential)

  def detectFaceFeatures(self, image_list):
    face_features = []
    for image in image_list:
      face_features.append(self.face.detect_with_stream(image, detection_model='detection_02'))
      print(len(face_features))
      print(len(face_features[0]))
    return face_features

class ImagePresenter:
  def drawDetectedFaces(self, features, image_dirs):
    for i,elem in enumerate(features):
      if not elem:
        print('no face found in {} image, skipping'.format(image_dirs[i]))
        continue
      img = Image.open(image_dirs[i])
      for e in elem:
        print(len(elem))
        print(e)
        image_presenter.drawROI(img, e.face_rectangle)
      img.show()
      input("Press Enter to continue...")

  def drawROI(self, image, roi):
    draw = ImageDraw.Draw(image)
    # for roi in rois:
    left, top = roi.left, roi.top
    right, bottom = left + roi.width, top + roi.height
    draw.rectangle(((left,top), (right, bottom)), outline='red')


# get all test images paths
image_dirs = glob.glob('./test/*.jpg')
# open all test images
images = [open(dir, 'r+b') for dir in image_dirs]

face_detector = FaceDetector()
# create detection for every face
features = face_detector.detectFaceFeatures(images)


image_presenter = ImagePresenter()
image_presenter.drawDetectedFaces(features, image_dirs)


# detectFaceFeatures
# print(images)
# print(image_dirs)

# face_client = FaceDetector()
# img = open('./test/test.jpg', 'r+b')
# print(type(img))
# output = Image.open('./test/test.jpg')
# draw = ImageDraw.Draw(output)
# detected_face = face_client.face.detect_with_stream(img, detectionModel='detection_02')
# print(dir(detected_face))
# print(type(detected_face))
# for elem in detected_face:
#   print(elem)
#   print(elem.face_rectangle)
#   left, top = elem.face_rectangle.left, elem.face_rectangle.top
#   right, bottom = left + elem.face_rectangle.width, top + elem.face_rectangle.height
#   draw.rectangle(((left,top), (right, bottom)), outline='red')
# # print(face_client._deserialize())
# # print(dir(face_client))
# output.show()

# url = "https://docs.microsoft.com/en-us/learn/data-ai-cert/identify-faces-with-computer-vision/media/clo19_ubisoft_azure_068.png"

# attributes = ["emotion", "glasses", "smile"]
# include_id = True
# include_landmarks = False

# detected_faces = face_client.face.detect_with_url(url, include_id, include_landmarks, attributes, raw=True)

# if not detected_faces:
#     raise Exception('No face detected in image')

# print(detected_faces.response.json())