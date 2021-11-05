'''
*****************************************************************************************
*
*        		===============================================
*           		Berryminator (BM) Theme (eYRC 2021-22)
*        		===============================================
*
*  This script is to implement Task 1B of Berryminator(BM) Theme (eYRC 2021-22).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*
*****************************************************************************************
'''


# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_1b.py
# Functions:		init_remote_api_server, start_simulation, stop_simulation, exit_remote_api_server, 
#                   get_vision_sensor_image, transform_vision_sensor_image, detect_qr_codes
# Global variables:	
# 					[ List of global variables defined in this file ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv, os)                ##
##############################################################
#from collections import Counter
import cv2
import numpy as np
import os, sys
import traceback
from pyzbar.pyzbar import decode
##############################################################

# Importing the sim module for Remote API connection with CoppeliaSim
try:
	import sim
	
except Exception:
	print('\n[ERROR] It seems the sim.py OR simConst.py files are not found!')
	print('\n[WARNING] Make sure to have following files in the directory:')
	print('sim.py, simConst.py and appropriate library - remoteApi.dll (if on Windows), remoteApi.so (if on Linux) or remoteApi.dylib (if on Mac).\n')
	sys.exit()



################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.      ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.                         ##
##############################################################
# def mid_points(decodedObjects):
# 	M = cv2.moments(decodedObjects)
# 	if M['m00'] != 0.0:
# 		x = int(M['m10'] / M['m00'])
# 		y = int(M['m01'] / M['m00'])
# 		return (x, y)


# def find_colour(transformed_image,midpoints):
# 	blue, green, red = cv2.split(transformed_image)
# 	red1 = red[midpoints[1]][midpoints[0]]
# 	green1 = green[midpoints[1]][midpoints[0]]
# 	blue1 = blue[midpoints[1]][midpoints[0]]
# 	if red1 == 255 and green1 == 0 and blue1 == 0:
# 		color = "Red"
# 	elif red1 == 0 and green1 == 255 and blue1 == 0:
# 		color = "Green"
# 	elif red1 == 0 and green1 == 0 and blue1 == 255:
# 		color = "Blue"
# 	else:
# 		color = "Orange"
# 	return color





##############################################################


def init_remote_api_server():

	"""
	Purpose:
	---
	This function should first close any open connections and then start
	communication thread with server i.e. CoppeliaSim.
	
	Input Arguments:
	---
	None
	
	Returns:
	---
	`client_id` 	:  [ integer ]
		the client_id generated from start connection remote API
	
	Example call:
	---
	client_id = init_remote_api_server()
	
	"""

	client_id = -1

	##############	ADD YOUR CODE HERE	##############
	sim.simxFinish(client_id)  # just in case, close all opened connections
	client_id = sim.simxStart('127.0.0.1', 19997, True, True, 5000, 5)  # Connect to CoppeliaSim
	if client_id != -1:
		print('Connected to remote API server')


	##################################################

	return client_id


def start_simulation(client_id):

	"""
	Purpose:
	---
	This function should first start the simulation if the connection to server
	i.e. CoppeliaSim was successful and then wait for last command sent to arrive
	at CoppeliaSim server end.
	
	Input Arguments:
	---
	`client_id`    :   [ integer ]
		the client id of the communication thread returned by init_remote_api_server()

	Returns:
	---
	`return_code` 	:  [ integer ]
		the return code generated from the start running simulation remote API
	
	Example call:
	---
	return_code = start_simulation(client_id)
	
	"""
	return_code = -2

	##############	ADD YOUR CODE HERE	##############
	if client_id != -1:
		return_code = sim.simxStartSimulation(client_id, sim.simx_opmode_oneshot)
	# return_code = sim.simxSynchronous(client_id, True)
	return_code, pingtime = sim.simxGetPingTime(client_id)
	

	##################################################

	return return_code


def get_vision_sensor_image(client_id):
	
	"""
	Purpose:
	---
	This function should first get the handle of the Vision Sensor object from the scene.
	After that it should get the Vision Sensor's image array from the CoppeliaSim scene.
	Input Arguments:
	---
	`client_id`    :   [ integer ]
		the client id of the communication thread returned by init_remote_api_server()
	
	Returns:
	---
	`vision_sensor_image` 	:  [ list ]
		the image array returned from the get vision sensor image remote API
	`image_resolution` 		:  [ list ]
		the image resolution returned from the get vision sensor image remote API
	`return_code` 			:  [ integer ]
		the return code generated from the remote API
	
	Example call:
	---
	vision_sensor_image, image_resolution, return_code = get_vision_sensor_image(client_id)
	"""

	vision_sensor_image = []
	image_resolution = []
	return_code = 0

	##############	ADD YOUR CODE HERE	##############
	return_code, handle = sim.simxGetObjectHandle(client_id, "vision_sensor", sim.simx_opmode_oneshot_wait)
	return_code, image_resolution, vision_sensor_image = sim.simxGetVisionSensorImage(client_id, handle, 0,sim.simx_opmode_streaming)
	while (client_id != 1):
		return_code, image_resolution, vision_sensor_image = sim.simxGetVisionSensorImage(client_id, handle, 0,sim.simx_opmode_buffer)
		if return_code == sim.simx_return_ok:
			break


	##################################################

	return vision_sensor_image, image_resolution, return_code


def transform_vision_sensor_image(vision_sensor_image, image_resolution):

	"""
	Purpose:
	---
	This function should:
	1. First convert the vision_sensor_image list to a NumPy array with data-type as uint8.
	2. Since the image returned from Vision Sensor is in the form of a 1-D (one dimensional) array,
	the new NumPy array should then be resized to a 3-D (three dimensional) NumPy array.
	3. Change the color of the new image array from BGR to RGB.
	4. Flip the resultant image array about the X-axis.
	The resultant image NumPy array should be returned.
	
	Input Arguments:
	---
	`vision_sensor_image` 	:  [ list ]
		the image array returned from the get vision sensor image remote API
	`image_resolution` 		:  [ list ]
		the image resolution returned from the get vision sensor image remote API
	
	Returns:
	---
	`transformed_image` 	:  [ numpy array ]
		the resultant transformed image array after performing above 4 steps
	
	Example call:
	---
	transformed_image = transform_vision_sensor_image(vision_sensor_image, image_resolution)
	
	"""

	transformed_image = None

	##############	ADD YOUR CODE HERE	##############
	img = np.array(vision_sensor_image, dtype=np.uint8)
	img.resize([image_resolution[1], image_resolution[0], 3])
	image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	transformed_image = cv2.flip(image_rgb, 0)
	##################################################
	
	return transformed_image


def stop_simulation(client_id):
	"""
	Purpose:
	---
	This function should stop the running simulation in CoppeliaSim server.
	NOTE: In this Task, do not call the exit_remote_api_server function in case of failed connection to the server.

	Input Arguments:
	---
	`client_id`    :   [ integer ]
		the client id of the communication thread returned by init_remote_api_server()

	Returns:
	---
	`return_code` 	:  [ integer ]
		the return code generated from the stop running simulation remote API

	Example call:
	---
	return_code = stop_simulation(client_id)

	"""

	return_code = -2

	##############	ADD YOUR CODE HERE	##############
	# if client_id != -1:
	return_code = sim.simxStopSimulation(client_id, sim.simx_opmode_oneshot)



	##################################################

	return return_code


def exit_remote_api_server(client_id):

	"""
	Purpose:
	---
	This function should wait for the last command sent to arrive at the Coppeliasim server
	before closing the connection and then end the communication thread with server
	i.e. CoppeliaSim using simxFinish Remote API.
	Input Arguments:
	---
	`client_id`    :   [ integer ]
		the client id of the communication thread returned by init_remote_api_server()

	Returns:
	---
	None

	Example call:
	---
	exit_remote_api_server(client_id)

	"""

	##############	ADD YOUR CODE HERE	##############
	#return_code, pingTime = sim.simxGetPingTime(client_id)
	sim.simxGetPingTime(client_id)
	return_code = sim.simxSynchronous(client_id, True)
	sim.simxFinish(client_id)
	#return_code, pingTime = sim.simxGetPingTime(client_id)
	##################################################
#
def detect_qr_codes(transformed_image):

	"""
	Purpose:
	---
	This function receives the transformed image from the vision sensor and detects qr codes in the image

	Input Arguments:
	---
	`transformed_image` 	:  [ numpy array ]
		the transformed image array

	Returns:
	---
	`qr_codes`  :  [ nested list ]
		A nested list is returned in which each element contains
		details of an individual qr code detected in vision sensor image.

	Example call:
	---
	qr_codes = detect_qr_codes(transformed_image)

	"""

	qr_codes = []
	##########################################################
	image=cv2.imread('transformed_image')
	decodedObjects = decode(transformed_image)
	for barcode in decodedObjects:
		(x, y, w, h) = barcode.rect
		cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 5)
		myData= barcode.data.decode('utf-8')
		x = x + (w/2)
		y = y + (h/2)
		qr_codes.append([myData, (x, y)])
	##########################################################

	return qr_codes

if __name__ == "__main__":

	qr_codes_list = []

	# Initiate the Remote API connection with CoppeliaSim server
	print('\nConnection to CoppeliaSim Remote API Server initiated.')
	print('Trying to connect to Remote API Server...')
	cv2.namedWindow('transformed image', cv2.WINDOW_AUTOSIZE)

	try:
		client_id = init_remote_api_server()

		if (client_id != -1):
			print('\nConnected successfully to Remote API Server in CoppeliaSim!')

			# Starting the Simulation
			try:
				return_code = start_simulation(client_id)

				if (return_code == sim.simx_return_novalue_flag) or (return_code == sim.simx_return_ok):
					print('\nSimulation started correctly in CoppeliaSim.')

				else:
					print('\n[ERROR] Failed starting the simulation in CoppeliaSim!')
					print('start_simulation function is not configured correctly, check the code!')
					print()
					sys.exit()

			except Exception:
				print('\n[ERROR] Your start_simulation function throwed an Exception, kindly debug your code!')
				print('Stop the CoppeliaSim simulation manually.\n')
				traceback.print_exc(file=sys.stdout)
				print()
				sys.exit()
		
		else:
			print('\n[ERROR] Failed connecting to Remote API server!')
			print('[WARNING] Make sure the CoppeliaSim software is running and')
			print('[WARNING] Make sure the Port number for Remote API Server is set to 19997.')
			print('[ERROR] OR init_remote_api_server function is not configured correctly, check the code!')
			print()
			sys.exit()

	except Exception:
		print('\n[ERROR] Your init_remote_api_server function throwed an Exception, kindly debug your code!')
		print('Stop the CoppeliaSim simulation manually if started.\n')
		traceback.print_exc(file=sys.stdout)
		print()
		sys.exit()

	while True:

	# Get image array and its resolution from Vision Sensor in ComppeliaSim scene
		try:
			vision_sensor_image, image_resolution, return_code = get_vision_sensor_image(client_id)

			if ((return_code == sim.simx_return_ok) and (len(image_resolution) == 2) and (len(vision_sensor_image) > 0)):
				print('\nImage captured from Vision Sensor in CoppeliaSim successfully!')

				# Get the transformed vision sensor image captured in correct format
				try:
					transformed_image = transform_vision_sensor_image(vision_sensor_image, image_resolution)

					if (type(transformed_image) is np.ndarray):

						qr_codes_list = detect_qr_codes(transformed_image)
						print(qr_codes_list)

						cv2.imshow('transformed image', transformed_image)
						if cv2.waitKey(1) & 0xFF == ord('q'):
							break
						

					else:
						print('\n[ERROR] transform_vision_sensor_image function is not configured correctly, check the code.')
						print('Stop the CoppeliaSim simulation manually.')
						print()
						sys.exit()

				except Exception:
					print('\n[ERROR] Your transform_vision_sensor_image function throwed an Exception, kindly debug your code!')
					print('Stop the CoppeliaSim simulation manually.\n')
					traceback.print_exc(file=sys.stdout)
					print()
					sys.exit()

			else:
				print('\n[ERROR] get_vision_sensor function is not configured correctly, check the code.')
				print('Stop the CoppeliaSim simulation manually.')
				print()
				sys.exit()

		except Exception:
			print('\n[ERROR] Your get_vision_sensor_image function throwed an Exception, kindly debug your code!')
			print('Stop the CoppeliaSim simulation manually.\n')
			traceback.print_exc(file=sys.stdout)
			print()
			sys.exit()
		
		
	cv2.destroyAllWindows()

	
	# Ending the Simulation
	try:
		return_code = stop_simulation(client_id)

		if (return_code == sim.simx_return_novalue_flag) or (return_code == sim.simx_return_ok):
			print('\nSimulation stopped correctly.')

			#Stop the Remote API connection with CoppeliaSim server
			try:
				exit_remote_api_server(client_id)

				if (start_simulation(client_id) == sim.simx_return_initialize_error_flag):
					print('\nDisconnected successfully from Remote API Server in CoppeliaSim!')

				else:
					print('\n[ERROR] Failed disconnecting from Remote API server!')
					print('[ERROR] exit_remote_api_server function is not configured correctly, check the code!')

			except Exception:
				print('\n[ERROR] Your exit_remote_api_server function throwed an Exception, kindly debug your code!')
				print('Stop the CoppeliaSim simulation manually.\n')
				traceback.print_exc(file=sys.stdout)
				print()
				sys.exit()

		else:
			print('\n[ERROR] Failed stopping the simulation in CoppeliaSim server!')
			print('[ERROR] stop_simulation function is not configured correctly, check the code!')
			print('Stop the CoppeliaSim simulation manually.')

		print()
		sys.exit()

	except Exception:
		print('\n[ERROR] Your stop_simulation function throwed an Exception, kindly debug your code!')
		print('Stop the CoppeliaSim simulation manually.\n')
		traceback.print_exc(file=sys.stdout)
		print()
		sys.exit()
