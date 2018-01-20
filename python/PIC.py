import time
import sys
import VL53L0X
import cv2
import os
import sqlite3
import requests
import json
import numpy as np
from subprocess import Popen, PIPE
from PIL import Image
import FaceRecogniser
#import FaceProcessing

#Person Identity Checker
class PIC:
	def check_distance(self, tof):
		tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

		timing = tof.get_timing()
		if (timing < 20000):
		    timing = 20000
		print ("Timing %d ms" % (timing/1000))
		distance = tof.get_distance()
		print(distance)
		
		time.sleep(timing/1000000.00)

		tof.stop_ranging()

		return distance

	def recognize_face(self):
		trainerName = "Trainer/Face_Trainer.yml"
		recognizer = cv2.face.createLBPHFaceRecognizer()
		recognizer.load(trainerName)
		faceProcessing = FaceProcessing.FaceProcessing(recognizer)
		
		faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
		video_capture = cv2.VideoCapture(0)

		#Go For 5 recognitions and then choose the Maximum No amongst the predicted IDs
		Id = faceProcessing.video_frame_capture(video_capture, "Recognition", faceCascade)
		video_capture.release()
		return Id

	def parse_json_response(self, content):
		print(content)
		IdR = "Unknown"
		status = content["images"][0]["transaction"]["status"]
		if status == "success":
			Id = content["images"][0]["transaction"]["subject_id"]
			confidence = content["images"][0]["transaction"]["confidence"]
			print(Id, confidence, status)
			IdR = Id
		else:
			print(status)

		return IdR

	def recognize_face_kairos(self):
		os.system("fswebcam SavedImages/ImgName.jpg")

		url = "https://api.kairos.com/recognize"

		headers = {
		'app_id': '5c6933d9',
		'app_key': '673c678af63f93255d6faf0e2a0a9ce1'
		}

		files = {'image': open('SavedImages/ImgName.jpg', 'rb')}
		payload= {"gallery_name":"CNProj"}
		response = requests.post(url, headers=headers, data=payload, files=files)

		Id = ""
		if response.status_code is 200:
			if len(response.content) < 100:
				Id = self.recognize_face_kairos()
				return Id
			else:
				data = json.loads(response.text)
				Id = self.parse_json_response(data)
				
				ImgName = "Image_" + Id + ".jpg"
				print("Id is ->", Id)
				return Id

		return Id

	def train_face_kairos(self, path, tag):
		imagePaths = [os.path.join(path,f) for f in os.listdir(path)] 

		for count in range(5):
			imgName = path + "ImgName_"+ str(count) +".jpg"
			os.system("fswebcam " + imgName)
			self.enroll_to_kairos(imgName, tag)

	def detect_train_face(self, tag):
		print("Training Open CV Trainer")
		trainerName = "Trainer/Face_Trainer.yml"
		recognizer = cv2.face.createLBPHFaceRecognizer()
		recognizer.load(trainerName)
		faceProcessing = FaceProcessing.FaceProcessing(recognizer)
		faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
		video_capture = cv2.VideoCapture(0)
		
		capture_Id = faceProcessing.next_capture_Id("DataSets/")
		faceProcessing.video_frame_capture(video_capture, "Detection", capture_Id)
		faces, Ids = faceProcessing.fetch_Load_Image_Data("DataSets/")
		recognizer.train(faces, np.array(Ids))
		recognizer.save(trainerName)

		location = "SavedImage"
		Image_name = "Image_" + capture_Id + ".jpg"
		faceProcessing.save_faceCurr(Image_name)
		self.insert_into_faceid(capture_id, tag)

		return Image_name, capture_Id

	def enroll_to_kairos(self, imgName, tag):
		url = "https://api.kairos.com/enroll"

		headers = {
			    'app_id': '5c6933d9',
			    'app_key': '673c678af63f93255d6faf0e2a0a9ce1'
		    }

		files = {'image': open(imgName, 'rb')}
		payload= {"gallery_name":"CNProj"}
		response = requests.post(url, headers=headers, data=payload, files=files)
		print (response)

	def data_to_ec2(self, fileName, imageOrFile = 1):
		if imageOrFile is 0:
			status = os.system("sudo scp -i EC2_ROG.pem SavedImages/" + fileName + " ubuntu@54.163.103.176:")
		elif imageOrFile is 1:
			status = os.system("sudo scp -i EC2_ROG.pem " + fileName + " ubuntu@54.163.103.176:")			
		return status

	def match_password(self, tof):
		passwordMatch = False
		distance_1 = self.check_distance(tof)
		self.speech("Last Recorded distance was, " + str(distance_1) + "mm")
		time.sleep(2) #in Seconds
		distance_2 = self.check_distance(tof)
		self.speech("Last Recorded distance was, " + str(distance_2) + "mm")
		time.sleep(2)
		distance_3 = self.check_distance(tof)
		self.speech("Last Recorded distance was, " + str(distance_3) + "mm")
		time.sleep(2)

		print("Done Reading")
		conn = sqlite3.connect('Database/userDB.sqlite')
		cur = conn.cursor()
		selectQuery = "SELECT * from User WHERE distance_1_L < ? and distance_1_R > ?"

		db_id = 0
		for row in cur.execute(selectQuery, (distance_1, distance_1)):
			db_id = row[0]
			if (row[4] < distance_2 and row[5] > distance_2) and (row[6] < distance_3 and row[7] > distance_3):
				passwordMatch = True
				break
		cur.close()

		print(db_id)
		return passwordMatch, db_id

	def register_password(self, tof):
		#1st pattern		
		time.sleep(3)
		distance_1 =  self.check_distance(tof)
		self.speech("Registered distance was, " + str(distance_1) + "mm")
		time.sleep(2)
		#2nd pattern
		distance_2 =  self.check_distance(tof)
		self.speech("Registered distance was, " + str(distance_2) + "mm")
		time.sleep(2)
		#3rd pattern
		distance_3 =  self.check_distance(tof)
		self.speech("Registered distance was, " + str(distance_3) + "mm")
		time.sleep(3)

		return (distance_1, distance_2, distance_3)
		# padding = 30 #in mm
		# self.insert_into_user(distance_1-padding, distance_1+padding, distance_2-padding, distance_2+padding, distance_3-padding, distance_3+padding)
			
	def create_db(self):
		conn = sqlite3.connect('Database/userDB.sqlite')	# Connect with Database
		cur = conn.cursor()

		createTableQueries = ''' 
		CREATE TABLE IF NOT EXISTS User (
		    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		    name     Text,
		    distance_1_L     INTEGER,
		    distance_1_R     INTEGER,
		    distance_2_L     INTEGER,
		    distance_2_R	 INTEGER,
		    distance_3_L     INTEGER,
		    distance_3_R     INTEGER
		);

		CREATE TABLE IF NOT EXISTS Login (
		    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		    last_login	INTEGER,
		    identity	INTEGER
		);

		CREATE TABLE IF NOT EXISTS Faceid (
		    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		    capture_id	INTEGER,
		    name	Text
		);

		'''
		self.create_table(createTableQueries, cur, conn)
		cur.close()

	def create_table(self, createTableQueries, cur, conn):
		print ("Please wait! creating Tables in DB..")
		cur.executescript(createTableQueries)		
		conn.commit()
		cur.close()

	def insert_into_user(self, name, distance_1_L, distance_1_R, distance_2_L, distance_2_R, distance_3_L, distance_3_R):
		conn = sqlite3.connect('Database/userDB.sqlite')
		cur = conn.cursor()

		insertionQuery_User = 'INSERT OR IGNORE INTO User (name, distance_1_L, distance_1_R, distance_2_L, distance_2_R, distance_3_L, distance_3_R) VALUES (?, ?, ?, ?, ?, ?, ?)'
		cur.execute(insertionQuery_User, (name, distance_1_L, distance_1_R, distance_2_L, distance_2_R, distance_3_L, distance_3_R))
		conn.commit()
		cur.close()

	def insert_into_login(self, time_curr, user):
		conn = sqlite3.connect('Database/userDB.sqlite')
		cur = conn.cursor()

		insertionQuery = 'INSERT OR IGNORE INTO Login (last_login, identity) VALUES (?, ?)'
		cur.execute(insertionQuery, (time_curr, user))
		conn.commit()
		cur.close()

	def insert_into_faceid(self, capture_id, name):
		conn = sqlite3.connect('Database/userDB.sqlite')
		cur = conn.cursor()

		insertionQuery = 'INSERT OR IGNORE INTO Faceid (capture_id, name) VALUES (?, ?)'
		cur.execute(insertionQuery, (capture_id, name))
		conn.commit()
		cur.close()

	def findAptResolution(self):
		avg_latency = 0.0
		p = Popen(["ping", "-c", "4", "google.com"], stdout=PIPE)
		while True:
			line = p.stdout.readline()
			if not line:
				break

			line2 = str(line)
			if line2.startswith('b\'rtt'):    	
				avg_latency = float(line2.split("=")[1].split("/")[1])

		resolution = "" #Resolutions Available: 160*120, 176*144, 352*288, 640*480
		if avg_latency < 30:
			resolution = "-r 640*480"
		elif avg_latency < 60:
			resolution = "-r 352*288"
		elif avg_latency < 90:
			resolution = "-r 176*144"
		else:
			resolution = "-r 160*120"

		return resolution

	def post_pi_processing_unknown(self, tof):
		resolution = self.findAptResolution()
		os.system("fswebcam " + resolution + " SavedImages/image_ImgName.jpg")
		# recognisedImg = cv2.imread("SavedImages/ImgName.jpg", 0)
		# faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
		# cv2.imwrite('SavedImages/ImgName.jpg', pic.rectangleImg(recognisedImg, faceCascade, Id))
		self.data_to_ec2("ImgName.jpg", 0)

		img_detail_file = open("ImageName.txt", "w")
		img_detail_file.write("Name:ImgName.jpg")
		img_detail_file.close()
		self.data_to_ec2("ImageName.txt", 1)

	def speech(self, message):
		# os.system("echo Welcome Please Enter Password after 2 Seconds| festival --tts")
		os.system("sh speech.sh " + message)

	def post_pi_processing_known(self, Id, tof):
		resolution = self.findAptResolution()
		os.system("fswebcam " + resolution + " SavedImages/image_" + str(Id) + ".jpg")
		# recognisedImg = cv2.imread("SavedImages/" + "image_" + str(Id) + ".jpg", 0)
		# faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
		# cv2.imwrite("SavedImages/" + "image_" + str(Id) + ".jpg", pic.rectangleImg(recognisedImg, faceCascade, Id))
		self.data_to_ec2("image_" + str(Id) + ".jpg", 0)

		startTime = int(round(time.time() * 1000))

		img_detail_file = open("ImageName.txt", "w")
		img_detail_file.write("Name:image_" + str(Id) + ".jpg\n")
		img_detail_file.write(pic.lastLogin(Id) + "\n")
		img_detail_file.write(str(self.check_distance(tof)/10) + "cm")
		img_detail_file.close()
		self.data_to_ec2("ImageName.txt", 1)
		
	def authentication_processing(self, Id, tof=None, sentTime=None):
		authentication_status = ""
		startTime = int(round(time.time()))

		content = []
		while True:
			# os.system("sudo scp -i EC2_ROG.pem ubuntu@54.163.103.176:authenticate.txt ~/IoTProject/python/") #Polling
			file = open("authenticate.txt", "r")

			count = 0
			for line in file:
				if count is 0:
					content = []
					count = count + 1
				content.append(line)

			authentication_status = content[0].split(':')[1].rstrip('\n')
			print("authentication_status", authentication_status)
			
			receivedTime = int(content[2])
			if receivedTime >= startTime:
				break; 
			else:
				print("Whiling")

			time.sleep(1)
			self.post_pi_processing_known(Id, tof)

		if authentication_status.rstrip('\w\r\n') == " accepted" or authentication_status.rstrip('\w\r\n') == "accepted":
			if Id is not "Unknown":
				self.speech("Welcome Home, " + str(Id))
			else:
				self.speech("You have been authorised but we will need a bit more time to grant access")
				print("Please Wait for some more time")
		else:
			self.speech("Sorry, You were not authenticated, try again later")

	def lastLogin(self, Id):
		conn = sqlite3.connect('Database/userDB.sqlite')
		cur = conn.cursor()
		selectQuery = "SELECT * from Login WHERE identity = ? ORDER BY identity DESC"
		print(Id)
		count = 0
		last_login_time = ""
		for row in cur.execute(selectQuery, (Id, )):
			last_login_time = row[1]
			count = count + 1
			if count == 2:
				break
		cur.close()
		return last_login_time

	def rectangleImg(self, frame, faceCascade, Id):
		#frame_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = faceCascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
		recognisedImg = None
		for (x, y, w, h) in faces:
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
			font = cv2.FONT_HERSHEY_SIMPLEX
			recognisedImg = cv2.putText(frame, str(Id), (x, y+h), font, 1, (0, 255, 255), 2)  #Font Color scheme - BGR
			return recognisedImg
		return recognisedImg

pic = PIC()

pic.create_db()
tof = VL53L0X.VL53L0X()
# pic.post_pi_processing_known("Me", tof)
pic.speech("Please place your hands in front of sensor as your password")
time.sleep(2)

distance = pic.check_distance(tof)
print(distance)
pic.speech("Currently you are " + str(distance) + "mm away from sensor")
passwordMatch = False
passwordMatch, db_id = pic.match_password(tof)

pic.speech("Hands in front of Sensor, not needed anymore!!")
print("passwordMatch", passwordMatch)
time.sleep(2)

if passwordMatch is False:
	pic.speech("password did not match")
	pic.speech("Please look in the camera while we try to match your password with the face")
	Id = pic.recognize_face_kairos()
	#Id = pic.recognize_face()
	print("->", Id)
	time.sleep(5)

	distances = ()
	if Id is "Unknown" or Id is None:
		print("Registring password")
		pic.speech("Please put your hands in front of Sensor, so that we can register your password")
		distances = pic.register_password(tof)
		print("Password, Registration Complete")

		pic.speech("Please Wait While You are being authorised")
		pic.post_pi_processing_unknown(tof)
		pic.authentication_processing("Unknown", tof, time.time())
	
		tag = ""		
		while tag is "":
			file = open("authenticate.txt", "r")
			count = 0
			for line in file:
				count =  count + 1
				if count is 2:
					words = line.split(":")
					tag = words[1]
					if tag != "":
						break
				else:
					print("Still Looking for a Tag..")
	
			time.sleep(2)
			pic.post_pi_processing_unknown(tof)
	
		pic.speech("Welcome, " + str(tag) + "Please look into the camera, we need few pictures of you for future")
		Image_name = pic.train_face_kairos("DataSets/", tag)
		# ImageName, captureID = pic.detect_train_face(tag)

		padding = 15 #in mm
		localtime = time.asctime(time.localtime(time.time()))
		pic.insert_into_login(str(localtime), tag)
		pic.insert_into_user(str(tag), distances[0]-padding, distances[0]+padding, distances[1]-padding, distances[1]+padding, distances[2]-padding, distances[2]+padding)
		pic.speech("Thankyou, for being patient, Access Granted")
	elif Id != "Unknown":
		count = 1
		while passwordMatch is False and Id != "Unknown":
			pic.speech("Wrong Password Entered, please try again" + Id)
			time.sleep(2)

			pic.speech("Place your hand in front of sensor once again")
			passwordMatch, db_id = pic.match_password(tof)
			if passwordMatch is True:
				pic.speech("Sorry for Security reasons, Please look in the camera while we try to match your password with the face again")
				Id = pic.recognize_face_kairos()
				# Id = pic.recognize_face()

				localtime = time.asctime(time.localtime(time.time()))
				pic.insert_into_login(str(localtime), Id)
				pic.post_pi_processing_known(Id, tof)
				pic.speech("Please be patient, you will be granted access in a moment")
				pic.authentication_processing(Id, tof, time.time())
				break

			if count >= 3:
				pic.speech("Maximum Attempts reached, please try again later. Sorry!")
				print("Failed to Enter the Correct Password")
				break
			else:
				count = count + 1
else:
	pic.speech("Please look in the camera while we try to match your password with the face")
	Id = pic.recognize_face_kairos()
	# Id = pic.recognize_face()
	found_in_db = False
	
	print("ID ->", Id)
	conn = sqlite3.connect('Database/userDB.sqlite')	# Connect with Database
	cur = conn.cursor()
	selectQuery = "SELECT * from User WHERE name = ?"

	for row in cur.execute(selectQuery, (Id, )):
		found_in_db = True
		if row[0] == db_id:
			Id = str(row[1])

			print(Id, db_id, row[0])
			localtime = time.asctime(time.localtime(time.time()))
			print(localtime)
			pic.insert_into_login(str(localtime), Id)
			cur.close()
			pic.post_pi_processing_known(Id, tof)
			pic.speech("Please be patient, you will be granted access in a moment")
			pic.authentication_processing(Id, tof, time.time())
			break

	if Id is "Unknown" or Id is None or found_in_db is False:
		print('Password/Face does not Match')
		pic.speech("Your Password and Face does not Match, Sorry Please Try again later!")