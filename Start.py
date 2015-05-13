
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
    QPushButton, QLineEdit, QRadioButton, QCheckBox, QListWidget, 
    QComboBox)
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QImage, QFont

import background
import skindetection
import face
import handdetection
import handgesture
import handmode

# Script options
FLAG_FULL_SCREEN = False
FLAG_LEARN = True
VIDEO_SOURCE = \
    '../../SmartVision/Hand_PatternDrawing.avi'
                #'/home/mehdi/vision/Sample-Video/Hand_PatternDrawing.avi'
write_file = ''
#WriteFile = cv2.VideoWriter("Phase1and2_Out_Video.avi", cv.CV_FOURCC('M', 'J', 'P', 'G'), 30, (1080, 720))

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
        self.label_name = QLabel(
            'Smart Environment Vision Project\nMohamad Kachuee, Mehdi Hosseini')
        self.label_name.setFont(QFont('Serif', 16))
        self.label_runname = QLabel('Run Name', self)
        self.label_time = QLabel('Time ', self)
        self.label_capture = QLabel('Capture Source ', self)
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
        self.display_1.mouseDoubleClickEvent = self.display_clicked
        
        self.display_2 = QLabel('display_2', self)
        self.display_2.resize(self.grid_size*16, self.grid_size*16)
        pixmap_2 = pixmap_2.scaled(self.display_2.height(), self.display_2.width(), 
            aspectRatioMode=Qt.KeepAspectRatio)
        self.display_2.mouseDoubleClickEvent = self.display_clicked
        self.display_2.setPixmap(pixmap_2)
        # buttons
        self.button_start = QPushButton('Start')
        self.button_start.clicked.connect(self.button_start_clicked)
        
        self.button_stop = QPushButton('Stop')
        self.button_stop.clicked.connect(self.button_stop_clicked)
        
        self.button_capture = QPushButton('Open Capture Device')
        self.button_capture.clicked.connect(self.button_capture_clicked)
        
        self.button_restart = QPushButton('Restart')
        self.button_restart.clicked.connect(self.button_restart_clicked)
        # radio buttons
        self.radiobutton_save = QRadioButton('Save Output ', self)
        self.radiobutton_save.toggled.connect(self.radiobutton_save_toggled)
        # check boxes
        self.checkbox_save1 = QCheckBox('Save 1', self)
        self.checkbox_save2 = QCheckBox('Save 2', self)
        self.checkbox_save3 = QCheckBox('Save 3', self)
        
        self.checkbox_learn = QCheckBox('Learn Mode ', self)
        self.checkbox_learn.toggled.connect(
            self.checkbox_learn_toggled)
        # combo boxes
        self.combobox_disp1 = QComboBox(self)
        self.combobox_disp1.addItems(['frame_input', 'frame_hand', 
            'frame_output', 'frame_foreground'])
        
        self.combobox_disp2 = QComboBox(self)
        self.combobox_disp2.addItems(['frame_input', 'frame_hand', 
            'frame_output', 'frame_foreground'])
        
        self.combobox_disp3 = QComboBox(self)
        self.combobox_disp3.addItems(['frame_input', 'frame_hand', 
            'frame_output', 'frame_foreground'])
        # line edits
        self.lineedit_runname = QLineEdit()
        self.lineedit_runname.setText('Run_0')
        self.lineedit_capture = QLineEdit()
        self.lineedit_capture.setText('0')
        # lcds displays
        self.lcd_time = QLCDNumber(self)
        self.lcd_time.setNumDigits(3)
        self.lcd_time.SegmentStyle(QLCDNumber.Filled)
        # place widgets
        grid = QGridLayout()
        grid.setSpacing(self.grid_size)
        #grid.addWidget(self.label_name, 0, 0)
        grid.addWidget(self.display_0, 0, 0, 32, 32)
        grid.addWidget(self.display_1, 31, 0, 16, 16)
        grid.addWidget(self.display_2, 31, 16, 16, 16)
        grid.addWidget(self.button_start, 0, 32, 1, 4)
        grid.addWidget(self.button_stop, 1, 32, 1, 4)
        grid.addWidget(self.button_restart, 2, 32, 1, 4)
        grid.addWidget(self.label_runname, 4, 32, 2, 2)
        grid.addWidget(self.lineedit_runname, 4, 34, 2, 2)
        grid.addWidget(self.radiobutton_save, 6, 32, 2, 4)
        grid.addWidget(self.label_time, 8, 32, 2, 2)
        grid.addWidget(self.lcd_time, 8, 33, 2, 3)
        grid.addWidget(self.label_capture, 10, 32, 2, 2)
        grid.addWidget(self.lineedit_capture, 10, 34, 2, 2)
        grid.addWidget(self.button_capture, 12, 32, 2, 4)
        grid.addWidget(self.checkbox_save1, 18, 32, 2, 4)
        grid.addWidget(self.checkbox_save2, 20, 32, 2, 4)
        grid.addWidget(self.checkbox_save3, 22, 32, 2, 4)
        grid.addWidget(self.combobox_disp1, 24, 32, 2, 4)
        grid.addWidget(self.combobox_disp2, 26, 32, 2, 4)
        grid.addWidget(self.combobox_disp3, 28, 32, 2, 4)
        grid.addWidget(self.checkbox_learn, 30, 32, 2, 4)
        # set layout
        self.setLayout(grid)
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Test')
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
    def radiobutton_save_toggled(self, e):
        global write_file
        if self.radiobutton_save.isChecked():
            write_file = cv2.VideoWriter(
                self.lineedit_runname.text()+'.avi', 
                cv.CV_FOURCC('M', 'J', 'P', 'G'), 30, (1080, 720))
    def checkbox_learn_toggled(self, e):
        global FLAG_LEARN
        if self.checkbox_learn.isChecked():
            FLAG_LEARN = True
        else:
            FLAG_LEARN = False

    def button_start_clicked(self):
        print('Run name is : ' + self.lineedit_runname.text())
        print('Starting ...')
        self.timer_0.start(1000/VIDEO_FR)

    def button_stop_clicked(self):
        print('Stopped')
        self.timer_0.stop()

    def button_restart_clicked(self):
        global video_capture, frame_number
        video_capture = cv2.VideoCapture(VIDEO_SOURCE)
        frame_number = 0

    def display_clicked(self, e):
        global FLAG_FULL_SCREEN
        print('Entering full screen mode')
        self.window_popup = PopupWindow()
        self.window_popup.showMaximized()
        self.window_popup.show()
        FLAG_FULL_SCREEN = True

    def button_capture_clicked(self):
        global video_capture
        video_capture = cv2.VideoCapture(int(self.lineedit_capture.text()))

    def timer_0_handler(self):
        # run main loop
        main_out = main_loop()
        # select three frame
        try:
            frame_1 = main_out[self.combobox_disp1.currentText()]
            frame_2 = main_out[self.combobox_disp2.currentText()]
            frame_3 = main_out[self.combobox_disp3.currentText()]
        except:
            frame_1 = np.zeros((2, 2))
            frame_2 = np.zeros((2, 2))
            frame_3 = np.zeros((2, 2))
        # display frames
        pixmap_0 = cv22pixmap(frame_1)
        pixmap_0 = pixmap_0.scaled(self.display_0.height(), 
            self.display_0.width(),
            aspectRatioMode=Qt.KeepAspectRatio)
        self.display_0.setPixmap(pixmap_0)
        
        pixmap_1 = cv22pixmap(frame_2)
        pixmap_1 = pixmap_1.scaled(self.display_1.height(), self.display_1.width(),
            aspectRatioMode=Qt.KeepAspectRatio)
        self.display_1.setPixmap(pixmap_1)

        pixmap_2 = cv22pixmap(frame_3)
        pixmap_2 = pixmap_2.scaled(self.display_2.height(), self.display_2.width(),
            aspectRatioMode=Qt.KeepAspectRatio)
        self.display_2.setPixmap(pixmap_2)
        # display on popup
        if FLAG_FULL_SCREEN:
            pixmap_0 = cv22pixmap(frame_1)
            self.window_popup.set_display(pixmap_0)
        # display time on the lcd
        self.lcd_time.display(main_loop.frame_time)
        # save the frame if the save option is set
        if self.radiobutton_save.isChecked():
            if self.checkbox_save1.isChecked():
                write_file.write(frame_input)
            elif self.checkbox_save2.isChecked():
                write_file.write(frame_input)
            else:
                write_file.write(frame_input)

def cv22pixmap(frame_input):
    image_input = QImage(frame_input.tostring(), frame_input.shape[1], 
         frame_input.shape[0], frame_input.shape[1]*3,QImage.Format_RGB888).rgbSwapped()
    pixmap = QPixmap.fromImage(image_input)
    return pixmap

class PopupWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.display_popup = QLabel('display_popup', self)
        self.screen = QApplication.desktop().screen()
        self.display_popup.resize(self.screen.width(), self.screen.height())

    def closeEvent(self, event):
        global FLAG_FULL_SCREEN
        FLAG_FULL_SCREEN = True
        event.accept()

    def set_display(self, pixmap):
        pixmap = pixmap.scaled(self.screen.width(), self.screen.height(), 
            aspectRatioMode=Qt.KeepAspectRatio)
        self.display_popup.setPixmap(pixmap)


# main loop for doing things
def main_loop():
    global frame_time, frame_number, HandMode, count_1, count_2, count_n1, video_capture
    # outputs
    frame_input = np.zeros((0, 0))
    frame_output_1 = np.zeros((0, 0))
    frame_output_2 = np.zeros((0, 0))
    main_loop.cnt += 1
    frame_number = frame_number + 1
    main_loop.frame_time = frame_number / VIDEO_FR
    # get a frame
    ret, frame_input = video_capture.read()
    main_outputs = {'frame_input':frame_input.copy()}
    # store first 3s frames
    if frame_number < 5:
        frames_first3s.append(frame_input)
    elif frame_number == 5:
        main_loop.frame_background = np.uint8(np.mean(frames_first3s, axis=0))
    # process from 3s
    else:
        crop_point, frame_output_11, frame_output_22 = \
            background.remove_background(
            frame_background=main_loop.frame_background, 
            frame_input=frame_input)
        main_outputs['frame_foreground'] = frame_output_11
        # ignore empty frames
        if crop_point[0]==-1 or crop_point[1]==-1 or \
            np.min([frame_output_11.shape[0], frame_output_11.shape[1]])<4:
            return frame_input, frame_output_1, frame_output_2
        
        # phase 2 starts here
        face_rectangles = -1
        frame_justSkin = skindetection.skin_detector(
            frame_output_11, face_rectangles)
        main_outputs['frame_skin'] = frame_justSkin
        # find active hand
        hand_pos, frame_hand, frame_contours = \
            handdetection.find_active_hand(frame_justSkin)
        main_outputs['frame_hand'] = frame_hand
        # find hand gesture
        frame_gesture, est_gesture, indicator = \
            handgesture.detect_gesture(frame_hand)
        # find hand mode
        HandMode,count_2,count_1,count_n1 = \
            handmode.hand_mode(est_gesture,HandMode,count_2,count_1,count_n1)
        main_outputs['state_hand'] = HandMode
        if HandMode != 'Deactive':
            point_text = (hand_pos[0]+crop_point[1]+indicator[0],
                hand_pos[1]+crop_point[0]+indicator[1])
            cv2.putText(frame_input,str(HandMode), point_text,
                cv2.FONT_HERSHEY_SIMPLEX, 1, (155, 200, 0))
            if indicator[0] != -1:
                cv2.circle(frame_input, point_text, 5, [255,255,255], -1)
            
            frame_output_2 = frame_hand
        frame_output_1 = frame_output_11

	if HandMode == 'Start':
		main_loop.Sketch_points = []
	if HandMode == 'Stop':
		main_loop.Sketch_points = []
	if HandMode == 'Active':
		main_loop.Sketch_points.append(point_text)
		for i,p1 in enumerate(main_loop.Sketch_points):
			if i != (len(main_loop.Sketch_points)-1) :
				cv2.line(frame_input, main_loop.Sketch_points[i], main_loop.Sketch_points[i+1], [0,255,0], 10)
        main_outputs['frame_output'] = frame_input

    return main_outputs
main_loop.cnt = 0
main_loop.Sketch_points = []
if  __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = UserInterface()
    sys.exit(app.exec_())
