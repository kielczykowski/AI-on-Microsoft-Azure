#!/usr/bin/env python3

import PySimpleGUI as sg
import screeninfo
import sys
from PIL import ImageTk, Image
import os
import io
import glob
from FaceDetector import FaceDetector, ImagePresenter
from MaskClassifier import MaskClassifier
import copy

class UI:
  def __init__(self):
    self.current_image = 0
    self.file_list = []
    self.IMAGE_WIDTH = 640
    self.IMAGE_HEIGHT = 480
    self.face_detector = FaceDetector()
    self.mask_classifier = MaskClassifier()
    self.image_presenter = ImagePresenter()
    self.createUI()

  # workaround to keep buttons in line
  def __IButton(self, *args, **kwargs):
    return sg.Col([[sg.Button(*args, **kwargs)]], pad=(0,0))

  def updateVisiblePhotoCounter(self):
    self.window['InputPhoto.text'].update(visible=True, value='Photo {}/{}'.format(self.current_image + 1, len(self.file_list)))

  def isListEmpty(self, list_elem):
    if len(list_elem) == 0:
      return True
    return False

  def drawDetectionsOnPhoto(self, image, features):
    for i,elem in enumerate(features):
      if not elem:
        raise RuntimeError('no face found in image, skipping')
      for e in elem:
        color = 'green'
        tag = 'OK'
        print(e.face_rectangle.additional_properties['detection'][0])
        print(e.face_rectangle.additional_properties['detection'][0].tag_name)
        if(e.face_rectangle.additional_properties['detection'][0].tag_name != 'GoodMaskPlacement'):
          tag = str(e.face_rectangle.additional_properties['detection'][0].tag_name)\
            + ' {:.2f} '.format(e.face_rectangle.additional_properties['detection'][0].probability * 100.0)\
            + '%'
          color = 'red'
        image = self.image_presenter.drawROI(image, e.face_rectangle, color=color)
        image = self.image_presenter.drawTextOnImage(image,e.face_rectangle, text = tag, color=color)
    return image

  def analyzeROIs(self, features):
    attributes = copy.deepcopy(features)
    for i,elem in enumerate(features):
      if not elem:
        print('no face found in image, skipping')
        continue
      for j, e in enumerate(elem):
        image = Image.open(self.file_list[self.current_image])
        print(e.face_rectangle)
        crop_image = image.crop(self.image_presenter.getPILROI(e.face_rectangle))
        buf = io.BytesIO()
        crop_image.save(buf, format='PNG')
        byte_img = buf.getvalue()
        result = self.mask_classifier.classify(byte_img)
        attributes[i][j].face_rectangle.additional_properties = {'detection':result.predictions}
    return attributes

  def updateInputImage(self, window_part, features = []):
    image = Image.open(self.file_list[self.current_image])
    if len(features) != 0:
      try:
        image = self.drawDetectionsOnPhoto(image, features)
      except RuntimeError as err:
        sg.popup_error(err)
        return
    image = image.resize((self.IMAGE_WIDTH, self.IMAGE_HEIGHT), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(image)
    self.window[window_part].update(data=image)

  def createUI(self):
    self.input_images_column = [
        [
          sg.Text("Images Folder"),
          sg.In(size=(25, 1), enable_events=True, key="InputImagesFolder"),
          sg.FolderBrowse()
        ],
        [sg.Image(key="InputImages", size=(self.IMAGE_WIDTH, self.IMAGE_HEIGHT))],
        [
          sg.Text('', key='InputPhoto.text', size=(20,1), font='Courier 10', visible=False),
          self.__IButton('Previous Photo', key='InputPhoto.prev', visible=False),
          self.__IButton('Next Photo', key='InputPhoto.next', visible=False),
          self.__IButton('Analyze Photo', key='InputPhoto.analyze', visible=False)
        ]
    ]

    self.output_images_column = [
      [sg.Text("Ouput Image")],
      [sg.Image(key="OutputImages", size=(self.IMAGE_WIDTH, self.IMAGE_HEIGHT))]
    ]

    self.layout = [
        [sg.Text("Mask Placement Detector",font=(25), justification='center')],
        [
          sg.Column(self.input_images_column),
          sg.VSeparator(),
          sg.Column(self.output_images_column)
        ]
    ]
    # ! TODO
    loc = (0,0)
    size = (100 + self.IMAGE_WIDTH * 2, self.IMAGE_HEIGHT + 200)
    if len(screeninfo.get_monitors()) == 1 or len(sys.argv) == 1:
      loc = (screeninfo.get_monitors()[0].width / 3, screeninfo.get_monitors()[0].height / 4)
    else:
      index =  int(sys.argv[1])
      monitor = screeninfo.get_monitors()[index]
      loc = (monitor.x + (monitor.width / 3), monitor.y + monitor.height / 4)

    self.window = sg.Window("MPD v 1.0", self.layout, location=loc, size=size, font='Courier 10', element_justification='c')

  def loop(self):
    # if (self.window['InputImages'].get_size() == (None, None)):
    #     print("YES")
    while True:
      event, values = self.window.read()

      if event == sg.WIN_CLOSED:
        break

      if event == 'InputImagesFolder':
        folder = values['InputImagesFolder']
        self.file_list = glob.glob(folder + '/*.jpg')
        self.file_list += glob.glob(folder + '/*.png')
        if len(self.file_list) == 0:
          sg.popup_error('No input file with .jpg or .png extenstion found in directory')
        else:
          self.updateInputImage('InputImages')
          self.window['InputPhoto.prev'].update(visible=True)
          self.window['InputPhoto.next'].update(visible=True)
          self.window['InputPhoto.analyze'].update(visible=True)
          self.updateVisiblePhotoCounter()

      if event == 'InputPhoto.prev':
        if self.isListEmpty(self.file_list):
          print("error, no photos to load")
        else:
          if self.current_image - 1 < 0:
            self.current_image = len(self.file_list) - 1
          else:
            self.current_image -= 1
          self.updateInputImage('InputImages')
          self.updateVisiblePhotoCounter()

      if event == 'InputPhoto.next':
        if self.isListEmpty(self.file_list):
          print("error, no photos to load")
        else:
          if self.current_image + 1 >= len(self.file_list) :
            self.current_image = 0
          else:
            self.current_image += 1
          self.updateInputImage('InputImages')
          self.updateVisiblePhotoCounter()
      if event == 'InputPhoto.analyze':
        image = [open(self.file_list[self.current_image], 'r+b')]
        features = self.face_detector.detectFaceFeatures(image)
        features = self.analyzeROIs(features)
        self.updateInputImage('OutputImages', features=features)
        # self.image_presenter


    self.window.close()


if __name__ == '__main__':

  print(sys.argv)
  print(screeninfo.get_monitors())
  ui = UI()
  ui.loop()