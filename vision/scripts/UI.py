#!/usr/bin/env python3

import PySimpleGUI as sg
import screeninfo
import sys
from PIL import ImageTk, Image
import os
import glob

class UI:
  def __init__(self):
    self.current_image = 0
    self.file_list = []
    self.IMAGE_WIDTH = 640
    self.IMAGE_HEIGHT = 480
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

  def updateInputImage(self):
    image = Image.open(self.file_list[self.current_image])
    image = image.resize((self.IMAGE_WIDTH, self.IMAGE_HEIGHT), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(image)
    self.window['InputImages'].update(data=image)

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
          self.__IButton('Next Photo', key='InputPhoto.next', visible=False)
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
      loc = (monitor.x + (monitor.width / 3), monitor.height / 4)

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
          self.updateInputImage()
          self.window['InputPhoto.prev'].update(visible=True)
          self.window['InputPhoto.next'].update(visible=True)
          self.updateVisiblePhotoCounter()

      if event == 'InputPhoto.prev':
        if self.isListEmpty(self.file_list):
          print("error, no photos to load")
        else:
          if self.current_image - 1 < 0:
            self.current_image = len(self.file_list) - 1
          else:
            self.current_image -= 1
          self.updateInputImage()
          self.updateVisiblePhotoCounter()

      if event == 'InputPhoto.next':
        if self.isListEmpty(self.file_list):
          print("error, no photos to load")
        else:
          if self.current_image + 1 >= len(self.file_list) :
            self.current_image = 0
          else:
            self.current_image += 1
          self.updateInputImage()
          self.updateVisiblePhotoCounter()


    self.window.close()


if __name__ == '__main__':

  print(sys.argv)
  print(screeninfo.get_monitors())
  ui = UI()
  ui.loop()