#!/usr/bin/env python3

import PySimpleGUI as sg
from PIL import ImageTk
import os
import glob

class UI:
  def __init__(self):
    self.current_image = 1
    self.file_list = []
    self.createUI()

  def createUI(self):
    self.input_images_column = [
        [
          sg.Text("Images Folder"),
          sg.In(size=(25, 1), enable_events=True, key="InputImagesFolder"),
          sg.FolderBrowse()
        ],
        [sg.Image(key="InputImages")]
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
          # for i, elem in enumerate(self.file_list):
          #   print(elem[-3:])
          #   if elem[-3:] == 'jpg':
          #     print(elem)
          #     self.file_list[i] = elem[:-3] + 'gif'
          #     print(elem)
          print()
          print(self.file_list)
          print(self.file_list[self.current_image])
          img = ImageTk.PhotoImage(file=self.file_list[self.current_image])
          # data = PhotoImage(file=self.file_list[self.current_image])
          self.window['InputImages'].update(data=img)

    self.window.close()


if __name__ == '__main__':
  print("XD")
  ui = UI()
  ui.loop()