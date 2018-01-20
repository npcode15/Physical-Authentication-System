import cv2
import os
import sys
import numpy as np
from PIL import Image
class FaceRecogniser:

	def face_predictor(self, x, y, w, h, frame_grey, Id, recognizer):
	    confidence = 0
	    predicted_id , confidence = recognizer.predict(frame_grey[y:y+h, x:x+w])
	    # predicted_id = recognizer.predict(frame_grey[y:y+h,x:x+w]) 
	    
	    print(predicted_id, confidence)

	    if confidence >= 50:
	        print(confidence)
	        if predicted_id is  1:
	            Id = "Sachin"
	        elif predicted_id is 2 or predicted_id is 3:
	            Id = "Navneet"
	        elif predicted_id is 4:
	            Id = "Utkarsh"
	        elif predicted_id is 5:
	            Id = "Prakhar"
	        elif predicted_id is 6:
	            Id = "Tanay"
	        else:
	            Id = "Unknown"
	    else:
	        return Id

	    return Id

	def video_frame_capture (video_capture, faceCascade, task):
	    if video_capture.isOpened() is not True: 
	      print("Error opening video stream or file")
	    
	    sampleNum = 0
	    Id = ""
	    while video_capture.isOpened() is True:
	        ret, frame = video_capture.read()
	        
	        if ret is True:
	            frame_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	            faces = faceCascade.detectMultiScale(frame_grey, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE) #scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.cv.CV_HAAR_SCALE_IMAGE)

	            for (x, y, w, h) in faces:
	                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)

	                if task is "Detection":
	                    print(Id)
	                    sampleNum = self.save_faces(x, y, w, h, sampleNum, frame_grey)
	                elif task is "Recognition":
	                    Id = self.face_predictor(x, y, w, h, frame_grey, Id)
	                    print(Id)

	                if task is "Recognition":
	                    font = cv2.FONT_HERSHEY_SIMPLEX
	                    cv2.putText(frame, str(Id), (x,y+h), font, 1, (0, 255, 255), 2)  #Font Color scheme - BGR

	            cv2.imshow('Frame', frame)
	            cv2.imwrite("image_" + str(Id) + ".jpg", frame)

	        if task is "Detection":
	            if sampleNum > 25:
	                break
	            else:
	                print(sampleNum)

	        if cv2.waitKey(25) & 0xFF == ord('q'):
	            break
	    cv2.destroyAllWindows()
 
# Capturing Video from WebCamera
# faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# video_capture = cv2.VideoCapture(0)

# recognizer = cv2.face.createLBPHFaceRecognizer()
# recognizer.load('Trainer/Face_Trainer.yml')

# # Face Recognition
# faceRecogniser = FaceRecogniser()
# FaceRecogniser.video_frame_capture(video_capture, "Recognition")
# video_capture.release()