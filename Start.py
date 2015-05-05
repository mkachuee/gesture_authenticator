
"""
ZetCode PyQt5 tutorial 

In this example, we connect a signal
of a QSlider to a slot of a QLCDNumber. 

author: Jan Bodnar
website: zetcode.com 
last edited: January 2015
"""
# Imports
import pdb
import time
import sys
import numpy as np
import matplotlib.pyplot as plt
import cv2
import cv

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (QWidget, QLCDNumber, QSlider, 
    QVBoxLayout, QGridLayout, QApplication, QAction, qApp, QLabel,
    QPushButton, QLineEdit, QRadioButton)
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QImage

import background
import skindetection
import face
import handdetection
import handgesture
import handmode

# Script options
VIDEO_SOURCE = \
    '../../SmartVision/Hand_PatternDrawing.avi'
                #'/home/mehdi/vision/Sample-Video/Hand_PatternDrawing.avi'

WriteFile = cv2.VideoWriter("Phase1and2_Out_Video.avi", cv.CV_FOURCC('M', 'J', 'P', 'G'), 30, (1080, 720))

# initialize of FSM variables
count_2=0
count_1=0
count_n1=0
HandMode="Deactive"
VIDEO_FR = 30.0
# Script starts here
video_capture = cv2.VideoCapture(VIDEO_SOURCE)
frame_number = 0
frame_time = 0
frames_first3s = []

class UserInterface(QWidget):
    
    def __init__(self):
        super(QWidget, self).__init__()

        self.ui_init()

    def ui_init(self):
        self.grid_size = 10
        pixmap_0 = QPixmap('0.jpg')
        pixmap_1 = QPixmap('0.jpg')
        pixmap_2 = QPixmap('0.jpg')
        # instantiate widgets
        # timer
        self.timer_0 = QTimer()
        self.timer_0.timeout.connect(self.timer_0_handler)
        # labels
        self.label_runname = QLabel('Run Name', self)
        # displays
        self.display_0 = QLabel('display_0', self)
        self.display_0.resize(self.grid_size*32, self.grid_size*32)
        pixmap_0 = pixmap_0.scaled(self.display_0.height(), self.display_0.width(), 
            aspectRatioMode=Qt.KeepAspectRatio)
        self.display_0.setPixmap(pixmap_0)
        self.display_0.mouseDoubleClickEvent = self.display_clicked

        self.display_1 = QLabel('display_1', self)
        self.display_1.resize(self.grid_size*16, self.grid_size*16)
        pixmap_1 = pixmap_0.scaled(self.display_1.height(), self.display_1.width(), 
            aspectRatioMode=Qt.KeepAspectRatio)
        self.display_1.setPixmap(pixmap_1)
        
        self.display_2 = QLabel('display_2', self)
        self.display_2.resize(self.grid_size*16, self.grid_size*16)
        pixmap_2 = pixmap_2.scaled(self.display_2.height(), self.display_2.width(), 
            aspectRatioMode=Qt.KeepAspectRatio)
        self.display_2.setPixmap(pixmap_2)
        # buttons
        self.button_start = QPushButton('Start')
        self.button_start.clicked.connect(self.button_start_clicked)
        self.button_stop = QPushButton('Stop')
        self.button_stop.clicked.connect(self.button_stop_clicked)
        # radio buttons
        self.radiobutton_option1 = QRadioButton('Option 1', self)
        # line edits
        self.lineedit_runname = QLineEdit()


        # place widgets
        grid = QGridLayout()
        grid.setSpacing(self.grid_size)
        grid.addWidget(self.display_0, 0, 0, 32, 32)
        grid.addWidget(self.display_1, 31, 0, 16, 16)
        grid.addWidget(self.display_2, 31, 16, 16, 16)
        grid.addWidget(self.button_start, 0, 32, 1, 4)
        grid.addWidget(self.button_stop, 1, 32, 1, 4)
        grid.addWidget(self.label_runname, 4, 32, 2, 2)
        grid.addWidget(self.lineedit_runname, 4, 34, 2, 2)
        grid.addWidget(self.radiobutton_option1, 6, 32, 2, 4)


        self.setLayout(grid)
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Test')
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def button_start_clicked(self):
        print('Run name is : ' + self.lineedit_runname.text())
        print('Starting ...')
        self.timer_0.start(1000/30)

    def button_stop_clicked(self):
        print('Stopped')
        self.timer_0.stop()

    def display_clicked(self, e):
        print('Entering full screen mode')
        #self.showFullScreen()

    def timer_0_handler(self):
        out, frame_input = main_loop()
        image_input = QImage(frame_input.tostring(), frame_input.shape[1], 
            frame_input.shape[0], QImage.Format_RGB888).rgbSwapped()
        pixmap_input = QPixmap.fromImage(image_input)
        pixmap_input = pixmap_input.scaled(self.display_0.height(), self.display_0.width(),
            aspectRatioMode=Qt.KeepAspectRatio)
        self.display_0.setPixmap(pixmap_input)
        print(out)

# main loop for doing things
def main_loop():
    global frame_time, frame_number
    main_loop.cnt += 1
    frame_number = frame_number + 1
    # get a frame
    ret, frame_input = video_capture.read()

    return main_loop.cnt, frame_input
main_loop.cnt = 0

if  __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = UserInterface()
    sys.exit(app.exec_())
