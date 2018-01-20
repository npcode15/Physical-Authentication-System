import cv2
import os
import sys
import numpy as np
import sqlite3
#import FaceRecogniser
from PIL import Image

class FaceProcessing:
	recognizer = None

	def __init__(self, recognizer):
		self.recognizer = recognizer

	def save_faceD(self, x, y, w, h, sampleNum, frame_grey, capture_Id):
		sampleNum = sampleNum + 1
		file_output_name = "DataSets/" + str(capture_Id) + '_' + str(sampleNum) + ".jpg"
		cv2.imwrite(file_output_name, frame_grey[y:y+h, x:x+w])
		
		return sampleNum

	def save_faceR(self, location, ImgName, frame):
		cv2.imwrite(location + ImgName, frame)

		img_detail_file = open("ImageName.txt", "w")
		img_detail_file.write("Name:" + ImgName)
		img_detail_file.close()

	def save_faceCurr(self, ImgName):
		os.system("fswebcam SavedImages/" + ImgName)

		img_detail_file = open("ImageName.txt", "w")
		img_detail_file.write("Name:" + ImgName)
		img_detail_file.close()

	def fetch_Load_Image_Data(self, path):
		imagePaths = [os.path.join(path,f) for f in os.listdir(path)] 

		faceSamples = []
		Ids = []

		for imagePath in imagePaths:
		    pilImage = Image.open(imagePath).convert('L')
		    imageNp = np.array(pilImage, 'uint8')

		    Id = int((imagePath.split('_')[0]).split('/')[1])
		    faces = faceCascade.detectMultiScale(imageNp)

		    for (x,y,w,h) in faces:
		        faceSamples.append(imageNp[y:y+h, x:x+w])
		        # cv2.imshow("Adding faces to traning set...", imageNp[y: y + h, x: x + w])
		        cv2.waitKey(50)
		        Ids.append(Id)

		cv2.destroyAllWindows()
		return faceSamples, Ids

	def face_predictor(self, x, y, w, h, frame_grey, Id):
	    confidence = 0
	    predicted_id , confidence = self.recognizer.predict(frame_grey[y:y+h, x:x+w])
	    # predicted_id = self.recognizer.predict(frame_grey[y:y+h, x:x+w])
	    # recognizer.predict(frame_grey[y:y+h,x:x+w]) 
	    print(predicted_id, confidence)
	    if confidence >= 50:
			conn = sqlite3.connect('Database/userDB.sqlite')	# Connect with Database
			cur = conn.cursor()
	
			in_db = False
			selectQuery = "SELECT * from Faceid WHERE capture_id = ?"
			for row in cur.execute(selectQuery, (predicted_id, )):
					in_db = False
					Id = str(row[2])

			if in_db is False:
				Id = "Unknown"

	  #       elif predicted_id is 2:	
	  #           Id = "Navneet"
			# elif predicted_id is  3:
	  #           Id = "Sachin"
	  #       elif predicted_id is 4:
	  #           Id = "Utkarsh"
	  #       elif predicted_id is 5:
	  #           Id = "Prakhar"
	  #       elif predicted_id is 4:
	  #           Id = "Milad"
	  #       else:
	  #           Id = "Unknown"
	    else:
	        return Id

	    return Id

	def video_frame_capture (self, video_capture, task, faceCascade, capture_Id=0):
	    if video_capture.isOpened() is not True: 
	      print("Error opening video stream or file")
	    
	    sampleNum = 0
	    Id = ""
	    recognisedImg = None
	    while video_capture.isOpened() is True:
	        ret, frame = video_capture.read()
	        
	        if ret is True:
	            frame_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	            faces = faceCascade.detectMultiScale(frame_grey, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
	            for (x, y, w, h) in faces:
	                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)

	                if task is "Detection":
	                	sampleNum = self.save_faceD(x, y, w, h, sampleNum, frame_grey, capture_Id)
	                elif task is "Recognition":
	                	Id = self.face_predictor(x, y, w, h, frame_grey, Id);#, cv2.face.createLBPHFaceRecognizer())
	                	font = cv2.FONT_HERSHEY_SIMPLEX
	                	recognisedImg = cv2.putText(frame, str(Id), (x, y+h), font, 1, (0, 255, 255), 2)  #Font Color scheme - BGR

	        if task is "Detection":
	            if sampleNum > 5:
	            	break
	            else:
	            	# cv2.imshow('Frame', frame)
	            	print(sampleNum)
	        elif task is "Recognition":
	        	#cv2.imshow('Frame', frame)
	        	if recognisedImg is not None:
	        		font = cv2.FONT_HERSHEY_SIMPLEX
	        		recognisedImg = cv2.putText(frame, str(Id), (x, y+h), font, 1, (0, 255, 255), 2)
	        		self.save_faceR("SavedImages/", "image_" + str(Id) + ".jpg", recognisedImg)
	        		return Id

	        if cv2.waitKey(25) & 0xFF == ord('q'):
	            break
	    cv2.destroyAllWindows()

	def next_capture_Id(self, path):
		print(path)
		imagePaths = [os.path.join(path,f) for f in os.listdir(path)] 
		
		thisId = 0
		for imagePath in imagePaths:
			print(imagePath)
			thisId = int(imagePath.split('_')[0].split("/")[1])

		return thisId + 1

# trainerName = "Trainer/Face_Trainer.yml"
# recognizer = cv2.face.createLBPHFaceRecognizer()
# recognizer.load(trainerName)
# faceProcessing = FaceProcessing(recognizer)

# # Capturing Video from WebCamera
# faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# video_capture = cv2.VideoCapture(0)

# # # Capturing Video from WebCamera
# # faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# # video_capture = cv2.VideoCapture(0)

# # # Face Detection 
# # Face Recognition
# faceProcessing.video_frame_capture(video_capture, "Recognition", faceCascade)
# video_capture.release()