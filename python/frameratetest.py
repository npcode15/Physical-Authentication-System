import os

resolution = "-r 160*120"
count = 0

while count < 50:
	count = count + 1
	os.system("fswebcam " + resolution + " SavedImages/ImgName.jpg")
	os.system("sudo scp -i EC2_ROG.pem SavedImages/ImgName.jpg ubuntu@54.236.4.176:")
	# img_detail_file = open("ImageName.txt", "w")
	# img_detail_file.write("Name:ImgName.jpg")
	# img_detail_file.close()

	# os.system("sudo scp -i EC2_ROG.pem SavedImages/ImageName.txt ubuntu@54.236.4.176:")