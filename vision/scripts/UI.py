#!/usr/bin/env python3

import PySimpleGUI as sg
from PIL import ImageTk
import os
import glob

class UI:
  def __init__(self):
    self.current_image = 0
    self.file_list = []
    self.createUI()

  # workaround to keep buttons in line
  def __IButton(self, *args, **kwargs):
    return sg.Col([[sg.Button(*args, **kwargs)]], pad=(0,0))

  def updateVisiblePhotoCounter(self, text_element):
    self.window[text_element].update(visible=True, value='Photo {}/{}'.format(self.current_image, len(self.file_list)))

  def createUI(self):
    self.input_images_column = [
        [
          sg.Text("Images Folder"),
          sg.In(size=(25, 1), enable_events=True, key="InputImagesFolder"),
          sg.FolderBrowse()
        ],
        [sg.Image(key="InputImages")],
        [
          sg.Text('', key='InputPhoto.text', size=(20,1), font='Courier 10', visible=False),
          self.__IButton('Previous Photo', key='InputPhoto.prev', visible=False),
          self.__IButton('Next Photo', key='InputPhoto.next', visible=False)
        ]
    ]

    self.output_images_column = [
      [sg.Text("Ouput Image")],
      [sg.Image(key="OutputImages")]
    ]

    self.layout = [
        [sg.Text("Mask Placement Detector")],
        [
          sg.Column(self.input_images_column),
          sg.VSeparator(),
          sg.Column(self.output_images_column)
        ]
    ]
    self.window = sg.Window("MPD v 1.0", self.layout)

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
          img = ImageTk.PhotoImage(file=self.file_list[self.current_image])
          self.window['InputImages'].update(data=img)
          self.window['InputPhoto.prev'].update(visible=True)
          self.window['InputPhoto.next'].update(visible=True)
          self.updateVisiblePhotoCounter('InputPhoto.text')
    self.window.close()


if __name__ == '__main__':
  print("XD")
  ui = UI()
  ui.loop()