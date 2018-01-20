
# # import time
# # import cv2
# # import numpy as py

# # def rectangleImg(frame, faceCascade, Id):
# # 	frame_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# # 	faces = faceCascade.detectMultiScale(frame_grey, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
# # 	for (x, y, w, h) in faces:
# # 		cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
# # 		font = cv2.FONT_HERSHEY_SIMPLEX
# # 		recognisedImg = cv2.putText(frame, str(Id), (x, y+h), font, 1, (0, 255, 255), 2)  #Font Color scheme - BGR
# # 	return recognisedImg

# # faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# # x = cv2.imread("4.jpg")

# # cv2.imwrite('abc.jpg', rectangleImg(x, faceCascade, "Me"))
# # Id = "Unknown"
# # img_detail_file = open("ImageName.txt", "w")
# # img_detail_file.write("Name:image_" + "X" + ".jpg\n")
# # localtime = time.asctime( time.localtime(time.time()))
# # img_detail_file.write(str(localtime) + "\n")
# # img_detail_file.close()

# import os
# import time
# import re

# # os.system("echo Welcome Mr. | festival --tts")
# startTime = int(round(time.time()))

# file = open("authenticate.txt", "r")

# content = []
# for line in file:
# 	content.append(line)

# print(content[0].split(':')[1].rstrip('\w\r\n'), len(content[0].split(':')[1].rstrip('\w\r\n')), len(re.replace("[^a-zA-Z]+", "", content[0].split(':')[1])))
# if content[0].split(':')[1].rstrip('\w\r\n') == " accepted":
# 	print("Hello")

# # print(content, content[0].split(':')[1][2:])
# # print(content)
# # authentication_status = content[0].split(':')[1]
# # print("authentication_status", authentication_status.rstrip('\w\r\n'), type(authentication_status[0:1])
# # # # receivedTime = content[1]
# # # # newstring = re.replace(r"[^a-zA-Z]+", "", authentication_status)
# # # # print(len(newstring))
# # # if authentication_status == " accepted":
# # # # 		print(receivedTime)

# import json
# import requests
# import time

# class abc:

# 	def parse_json_response(self, content):
# 		print(content)
# 		IdR = "Unknown"
# 		# print(len(content["images"][0]["candidates"]))
# 		status = content["images"][0]["transaction"]["status"]
# 		if status == "success":
# 			Id = content["images"][0]["transaction"]["subject_id"]
# 			confidence = content["images"][0]["transaction"]["confidence"]
# 			print(Id, confidence, status)
# 			IdR = Id
# 		else:
# 			print(status)
# 		# if confidence > 0.5:
# 		# 	return Id
# 		# else:
# 		return IdR

# 	def recognize_face_kairos(self, x = 0):
# 		print("Enter")
# 		time.sleep(1)
# 		# os.system("fswebcam SavedImages/ImgName.jpg")

# 		url = "https://api.kairos.com/recognize"
# 		headers = {
# 		'app_id': '5c6933d9',
# 		'app_key': '673c678af63f93255d6faf0e2a0a9ce1'
# 		}

# 		files = {'image': open('SavedImages/ImgName.jpg', 'rb')}
# 		payload= {"gallery_name":"CNProj"}
# 		response = requests.post(url, headers=headers, data=payload, files=files)

# 		Id = ""
# 		if response.status_code is 200:
# 			if len(response.content) < 100:
# 				print(response.text)
# 				self.recognize_face_kairos()
# 			else:
# 				if x == 0:
# 					x = x + 1
# 					self.recognize_face_kairos()
# 				else:
# 					data = json.loads(response.text)
# 					Id = self.parse_json_response(data)
					
# 					ImgName = "Image_" + Id + ".jpg"
# 					print("Id is ->", Id, ImgName)
# 					if Id is "Unknown":
# 						print("Cool Stuff")
# 		print("ID is ->", Id)
# 		return Id

# abcO = abc()
# print(abcO.recognize_face_kairos())
# import cv2

# def rectangleImg(frame, faceCascade, Id):
# 	#frame_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# 	faces = faceCascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
# 	recognisedImg = None
# 	for (x, y, w, h) in faces:
# 		cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
# 		font = cv2.FONT_HERSHEY_SIMPLEX
# 		recognisedImg = cv2.putText(frame, str(Id), (x, y+h), font, 1, (0, 255, 255), 2)  #Font Color scheme - BGR
# 		return recognisedImg
# 	return recognisedImg

# Id = "TestId"
# recognisedImg = cv2.imread("SavedImages/ImgName.jpg", 0)
# faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# cv2.imwrite('SavedImages/New.jpg', rectangleImg(recognisedImg, faceCascade, Id))


# import subprocess
# import os
# import time
# os.system("pscp ImgName.jpg pi@10.0.0.233:IoTProject/python/ 'raspberry'")
# result = run_command("pscp ImgName.jpg pi@10.0.0.233:IoTProject/python/")[0]

# def run_command(cmd):
		# return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE).communicate()

# result = str(run_command(["ping", "google.com"])[0])

# proc = subprocess.Popen(["ping", "google.com"], stdout=subprocess.PIPE)
# result = str(proc.stdout.read())
# avg_latency = result[result.find("Average") + len("Average") + 3: result.find("Average") + len("Average") + 5]
# print(avg_latency)

from subprocess import Popen, PIPE
p = Popen(["ping", "-c", "4", "google.com"], stdout=PIPE)
while True:
    line = p.stdout.readline()
    
    if not line:
        break

    line2 = str(line)
    print(line2)
    if line2.startswith('b\'rtt'):    	
    	avg = int(line2.split("=")[1].split("/")[1])
    	print(avg)

# test = "ImgName.jpg               | 110 kB | 110.8 kB/s | ETA: 00:00:00 | 100%"
# res = test.split("|")
# print(str.strip(result[1]), str.strip(result[2]))

# file = open(“testfile.txt”, ”r+”)
# content = "fileName | " + time.time() + " | " + str.strip(result[1]) + str.strip(result[2])
# file.write("")
# file.close()
# os.system("raspberry")
# res = subprocess.check_output(lcmd, stderr=subprocess.STDOUT)
# print(res)



# faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# 			img_detail_file = open("ImageName.txt", "w")
			# if Id is "Unknown" or Id is None:
			# 	pic.post_pi_processing_unknown()
			# else: