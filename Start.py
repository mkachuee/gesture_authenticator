
# Imports
import pdb
import time
import sys

import numpy as np
import matplotlib.pyplot as plt
import cv2
import cv
import pyttsx
import pickle

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
import pattern_match

# Script options
FLAG_FULL_SCREEN = False
FLAG_LEARN = True
TEXT_NAME = ''
KEYRING = []
PATTERN_BUFFER = np.zeros((16, 16), np.uint8)


VIDEO_SOURCE = \
    '0.avi'
    #'../../SmartVision/Hand_PatternDrawing.avi'
                #'/home/mehdi/vision/Sample-Video/Hand_PatternDrawing.avi'
write_file = ''
pattern_file = 'Pattern_File.txt'
# initialize of FSM variables
fgbg = cv2.BackgroundSubtractorMOG2(history=50, varThreshold=332)

count_2=0
count_1=0
count_n1=0
Last_HandMode="Deactive"
HandMode="Deactive"
VIDEO_FR = 15.0
# Script starts here
video_capture = cv2.VideoCapture(VIDEO_SOURCE)
frame_number = 0
frame_time = 0
frames_first3s = []
hand_points = []
crop_points = []
# tts engine
tts_engine = pyttsx.init()
tts_engine.setProperty('rate', 70)
tts_engine.runAndWait()

class UserInterface(QWidget):
    
    def __init__(self):
        super(QWidget, self).__init__()

        self.ui_init()

    def ui_init(self):
        self.grid_size = 8
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
        pixmap_0 = pixmap_0.scaled(self.display_0.height(), 
            self.display_0.width(), 
            aspectRatioMode=Qt.KeepAspectRatio)
        self.display_0.setPixmap(pixmap_0)
        self.display_0.mouseDoubleClickEvent = self.display_clicked

        self.display_1 = QLabel('display_1', self)
        self.display_1.resize(self.grid_size*16, self.grid_size*16)
        pixmap_1 = pixmap_0.scaled(self.display_1.height(), 
            self.display_1.width(), 
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
        self.checkbox_learn.setChecked(True)
        self.checkbox_learn.toggled.connect(
            self.checkbox_learn_toggled)
        # combo boxes
        self.combobox_disp1 = QComboBox(self)
        list_framename = ['frame_input', 'frame_hand', 
            'frame_output', 'frame_foreground', 'frame_pattern']
        self.combobox_disp1.addItems(list_framename)
        self.combobox_disp1.setCurrentText('frame_output')

        self.combobox_disp2 = QComboBox(self)
        self.combobox_disp2.addItems(list_framename)
        self.combobox_disp2.setCurrentText('frame_foreground')
        
        self.combobox_disp3 = QComboBox(self)
        self.combobox_disp3.addItems(list_framename)
        self.combobox_disp3.setCurrentText('frame_hand')
        # line edits
        self.lineedit_runname = QLineEdit()
        self.lineedit_runname.setText('Run_0')
        self.lineedit_capture = QLineEdit()
        self.lineedit_capture.setText('0')
        self.lineedit_name = QLineEdit()
        self.lineedit_name.setText('MR. Jack')
        global TEXT_NAME
        TEXT_NAME =self.lineedit_name.text()
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
        grid.addWidget(self.lineedit_name, 32, 32, 2, 4)
        # set layout
        self.setLayout(grid)
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
                cv.CV_FOURCC('M', 'J', 'P', 'G'), VIDEO_FR, (1080, 720))
    def checkbox_learn_toggled(self, e):
        global FLAG_LEARN, TEXT_NAME
        if self.checkbox_learn.isChecked():
            FLAG_LEARN = True
            TEXT_NAME = self.lineedit_name.text()
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
        global KEYRING
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
        pixmap_1 = pixmap_1.scaled(self.display_1.height(), 
            self.display_1.width(),
            aspectRatioMode=Qt.KeepAspectRatio)
        self.display_1.setPixmap(pixmap_1)

        pixmap_2 = cv22pixmap(frame_3)
        pixmap_2 = pixmap_2.scaled(self.display_2.height(), 
            self.display_2.width(),
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
                write_file.write(frame_1)
            elif self.checkbox_save2.isChecked():
                write_file.write(frame_2)
            else:
                write_file.write(frame_3)
        # if key status is other than -2
        try:
            if main_out['key_status'] != -2:
                self.window_access = PopupAccess()
                if main_out['key_status'] != -1:
                    self.window_access.set_message(
                        'Wellcome ' + KEYRING[main_out['key_status']][0])
                    self.window_access.set_display(
                        cv22pixmap(KEYRING[main_out['key_status']][2]))
                    print('Access granted')
                    tts_engine.say('Access granted')
                    tts_engine.say(
                        '    Wellcome ' + KEYRING[main_out['key_status']][0])
                    tts_engine.runAndWait()
                else:
                    self.window_access.set_message('Access denied')
                    self.window_access.set_display(QPixmap('denied.png'))
                    print('Access denied')
                    tts_engine.say('Access denied')
                    tts_engine.runAndWait()
                self.window_access.show()
        except:
            pass

def cv22pixmap(frame_input, channels=3):
    """
    Convert from opencv to QT format.
    """
    if len(frame_input.shape) == 3:
        image_input = QImage(frame_input.tostring(), frame_input.shape[1], 
             frame_input.shape[0], frame_input.shape[1]*channels, 
            QImage.Format_RGB888).rgbSwapped()
    else:
        channels = 1
        image_input = QImage(frame_input.tostring(), frame_input.shape[1], 
             frame_input.shape[0], frame_input.shape[1]*channels, 
             QImage.Format_Indexed8)
        
    pixmap = QPixmap.fromImage(image_input)
    
    return pixmap

class PopupWindow(QWidget):
    """
    Fullscreen popup window.
    """
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

class PopupAccess(QWidget):
    """
    Popup for access messages.
    """
    def __init__(self):
        QWidget.__init__(self)
        #self.resize( 200, 200)
        # displays
        self.display_image = QLabel('display_image', self)

        # labels
        self.label_message = QLabel('message', self)
        self.label_message.setFont(QFont('Serif', 26))
        
        # place them on a grid
        grid = QGridLayout()

        grid.addWidget(self.display_image, 0, 0, 16, 16)
        grid.addWidget(self.label_message, 16, 0, 4, 8)
        
        self.setLayout(grid)

    def set_display(self, pixmap):
        pixmap = pixmap.scaled(100, 100, 
            aspectRatioMode=Qt.KeepAspectRatio)
        self.display_image.setPixmap(pixmap)

    def set_message(self, message):
        self.label_message.setText(message)

# main loop for doing things
def main_loop():
    """
    Main loop of frame and video processing.
    Important things happen here ...
    """
    global frame_time, frame_number, HandMode, count_1, count_2, \
        count_n1, video_capture, KEYRING, PATTERN_BUFFER, TEXT_NAME, fgbg, \
        hand_points, crop_points
    # outputs
    frame_input = np.zeros((0, 0))
    frame_output_1 = np.zeros((0, 0))
    frame_output_2 = np.zeros((0, 0))
    main_loop.cnt += 1
    frame_number = frame_number + 1
    main_loop.frame_time = frame_number / VIDEO_FR
    # get a frame
    try:
        ret, frame_input = video_capture.read()
        ret, frame_input = video_capture.read()
        if ret == 0:
            frame_input = np.zeros((2, 2, 3), np.uint8)
        frame_input = cv2.resize(frame_input, (1080, 720))
        main_outputs = {'frame_input':frame_input.copy()}
    except:
        frame_input = np.zeros((2, 2, 3), np.uint8)
        main_outputs = {'frame_input':frame_input.copy()}

    ################### phase 1 starts here ###################
    main_outputs['key_status'] = -2 # -2 means do nothing
    # store first 3s frames
    if frame_number < 5:
        frames_first3s.append(frame_input)
    elif frame_number == 5:
        main_loop.frame_background = np.uint8(np.mean(frames_first3s, axis=0))
    # process from 3s
    else:
        crop_point, frame_output_11, frame_output_22 = \
            background.remove_background(
            frame_background=fgbg, 
            frame_input=frame_input)
        main_outputs['frame_foreground'] = frame_output_11
        # ignore empty frames
        if crop_point[0]==-1 or crop_point[1]==-1 or \
            np.min([frame_output_11.shape[0], frame_output_11.shape[1]])<4:
            return frame_input, frame_output_1, frame_output_2
        
        ################### phase 2 starts here ###################
        face_rectangles = -1
        frame_skin, frame_justSkin = skindetection.skin_detector2(
            frame_input, frame_output_11, face_rectangles)
        main_outputs['frame_skin'] = frame_justSkin
        # find active hand
        hand_pos, frame_hand, frame_contours = \
            handdetection.find_active_hand(frame_justSkin)
        
        hand_points.insert(1, hand_pos)
        crop_points.insert(1, crop_point)
        if len(hand_points) > 30:
            del hand_points[30]
            del crop_points[30]

	hand_points_mean = np.mean(hand_points, axis=0)
        crop_points_mean = np.mean(crop_points, axis=0)
        dist = np.sum(((hand_points_mean - hand_pos)**2))
        #print(dist)
        if dist > 100000:
            print('Warning : hand track')
            hand_pos =  (int(hand_points_mean[0]), int(hand_points_mean[1])) 
            crop_point =  (int(crop_points_mean[0]), int(crop_points_mean[1])) 
        
        frame_h =  frame_skin[hand_pos[1]-20+crop_point[0]:hand_pos[1]+frame_hand.shape[0]+crop_point[0]+20, hand_pos[0]-20+crop_point[1]:hand_pos[0]+frame_hand.shape[1]+20+crop_point[1], :]	
	hand_pos = (hand_pos[0]-20,hand_pos[1]-20)
	#print('AA', (crop_point[1],crop_point[0]), (hand_pos[1], hand_pos[0]) , frame_hand.shape)
        if frame_h is None:
            frame_h = np.zeros((2, 2))
        main_outputs['frame_hand'] = frame_h
        # find hand gesture
        frame_gesture, est_gesture, indicator = \
            handgesture.detect_gesture(frame_h)
        # find hand mode
	Last_HandMode = HandMode
        #HandMode,count_2,count_1,count_n1 = \
        #    handmode.hand_mode(est_gesture,HandMode,count_2,count_1,count_n1)
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

        ################### phase 3, 4 starts here ###################
	
        # if hand mode is start
        if HandMode == 'Start':
            main_loop.Sketch_points = []
            # start saving points
            PATTERN_BUFFER = np.zeros((frame_input.shape[0], 
                frame_input.shape[1]), np.uint8)
        
        # check if hand is deactivated
	elif HandMode == 'Deactive':
            main_loop.Sketch_points = []
            # start saving points
            PATTERN_BUFFER = np.zeros((frame_input.shape[0], 
                frame_input.shape[1]), np.uint8)
	
        # correct some problemetic states
        if HandMode == 'Stop' and Last_HandMode == 'Active':
            # crop black areas
            ind = np.nonzero(PATTERN_BUFFER)
            if len(ind[0] != 0):
                crop_point = (np.min(ind[0]), np.min(ind[1]))
                PATTERN_BUFFER = PATTERN_BUFFER[
                    np.min(ind[0]):np.max(ind[0]),
                    np.min(ind[1]):np.max(ind[1])]
            
            # if we are in learning mode
	    if FLAG_LEARN:
                print('learning a new pattern')
                faces = face.face_detect(frame_output_11)
                if len(faces) != 0 :
		    for (x, y, w, h) in faces:
		    	face_box = frame_output_11[y:y+h,x:x+w]
			new_key = (TEXT_NAME, PATTERN_BUFFER, face_box)
		#cv2.imshow('output video 1', face_box)
                else :
                    face_box = np.zeros((2, 2))
                    new_key = (TEXT_NAME, PATTERN_BUFFER, face_box)
		    print('no face!')
		try:
			pattern_w = open(pattern_file, 'a+')
			pattern_w.seek(0)    		
			keys_1 = pickle.load(pattern_w)
			pattern_w.close()
		except:
			keys_1 = []
		keys_1.append(new_key)
                KEYRING = keys_1
		with open(pattern_file, 'wb') as f:
    			pickle.dump(keys_1, f)
		
                tts_engine.say('a new pattern registered')
                tts_engine.runAndWait()
            else:
                print('start matching now')
		#read_keys = []
		pattern_open = open(pattern_file, 'rb')
    		read_keys = pickle.load(pattern_open)
		pattern_name, pattern_index = pattern_match.match_pattern(PATTERN_BUFFER, read_keys)
                #print((PATTERN_BUFFER.shape, TEXT_NAME))
		pattern_open.close()
		print((pattern_name, pattern_index))
                KEYRING = read_keys
                main_outputs['key_status'] = pattern_index
		
                
        # if hand mode is in active mode	
        if HandMode == 'Active':
	    if indicator[0] == -1:
		main_loop.Sketch_points.append(main_loop.Sketch_points[-1])
	    else:	    
		main_loop.Sketch_points.append(point_text)
	    for i,p1 in enumerate(main_loop.Sketch_points):
		if i != (len(main_loop.Sketch_points)-1) :
                    if cv2.norm(main_loop.Sketch_points[i], 
                        main_loop.Sketch_points[i+1]) < 80*1:
                            cv2.line(frame_input, 
                                main_loop.Sketch_points[i], 
                                main_loop.Sketch_points[i+1], 
                                    [0,255,0], 10)
                            cv2.line(PATTERN_BUFFER, 
                                main_loop.Sketch_points[i], 
                                main_loop.Sketch_points[i+1], 
                                    [255], 5)
                    else:
                        print('Warning : path correction')
                        main_loop.Sketch_points[i+1] = main_loop.Sketch_points[i]
        main_outputs['frame_output'] = frame_input
        main_outputs['frame_pattern'] = cv2.cvtColor(
            PATTERN_BUFFER, cv2.COLOR_GRAY2BGR)

    return main_outputs
main_loop.cnt = 0
main_loop.Sketch_points = []

if  __name__ == '__main__':
    # handle main operations
    app = QApplication(sys.argv)
    ex = UserInterface()
    sys.exit(app.exec_())
