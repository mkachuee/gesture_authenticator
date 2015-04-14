"""
This module implements FSM of Hand mode
"""
# imports
import pdb
import numpy as np
import cv2

def hand_mode(est_gesture,current_state,count_2,count_1,count_n1):
	"""
	This function implements FSM of hand mode
	FSM has four states:
	1 - Active : when recording
	2 - Start : start of recording
	3 - Deactive : when hand is down or clenched
	4 - Stop : stop of recording
	"""
	start2active=8
	#start2deactive=
	#stop2active=
	stop2deactive=10
	active2stop=2
	#active2deactive=
	deactive2start=2
	#deactive2active=	

	nextstate = current_state

	if (est_gesture== -1) :
		count_n1 = count_n1 + 1
	elif (est_gesture== 1) :
		count_1 = count_1 + 1
	elif (est_gesture== 2) :
		count_2 = count_2 + 1
	
	if (current_state == "Deactive") :
		if count_1 >= deactive2start :
			nextstate = "Start"
			count_2=0
			count_1=0
			count_n1=0
		#elif count_2 >= deactive2active :
		#	nextstate = "Active"
		#	count_2=0
		#	count_1=0
		#	count_n1=0
		if est_gesture == -1 :
			count_2=0
			count_1=0
			count_n1=0
	elif (current_state == "Start") :
		if count_2 >= start2active :
			nextstate = "Active"
			count_2=0
			count_1=0
			count_n1=0
		#elif count_n1 >= start2deactive :
		#	nextstate = "Deactive"
		#	count_2=0
		#	count_1=0
		#	count_n1=0
		if est_gesture == 1 :
			count_2=0
			count_1=0
			count_n1=0
	elif (current_state == "Stop") :
		if count_n1 >= stop2deactive :
			nextstate = "Deactive"
			count_2=0
			count_1=0
			count_n1=0
		#elif count_2 >= stop2active :
		#	nextstate = "Active"
		#	count_2=0
		#	count_1=0
		#	count_n1=0
		if est_gesture == 1 :
			count_2=0
			count_1=0
			count_n1=0
	elif (current_state == "Active") :
		if count_1 >= active2stop :
			nextstate = "Stop"
			count_2=0
			count_1=0
			count_n1=0
		#elif count_n1 >= active2deactive :
		#	nextstate = "Deactive"
		#	count_2=0
		#	count_1=0
		#	count_n1=0
		if est_gesture == 2 :
			count_2=0
			count_1=0
			count_n1=0
		


	return nextstate,count_2,count_1,count_n1

