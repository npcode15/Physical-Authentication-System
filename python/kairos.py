#import json
import requests

url = "https://api.kairos.com/enroll"

headers = {
	    'app_id': '5c6933d9',
	    'app_key': '673c678af63f93255d6faf0e2a0a9ce1'
    }

files = {'image': open('ImgName' + '.jpg', 'rb')}
payload= {"subject_id":"Navneet", "gallery_name":"CNProj"}
r = requests.post(url, headers=headers, data=payload, files=files)

print (r.text)
print (r)

# import requests

# # import requests
# def LookUp(content):
# 	# print(len(content["images"][0]["candidates"]))
# 	status = content["images"][0]["transaction"]["status"]
# 	print(len(status))
# 	if status == "failure":
# 		print("WTF")
# 		Id = content["images"][0]["transaction"]["subject_id"]
# 	# confidence = content["Errors"][0]["ErrCode"]
# 	print(len(r.content))
# 	# print(confidence)

# url = "https://api.kairos.com/recognize"
# headers = {
#     'app_id': '5c6933d9',
#     'app_key': '673c678af63f93255d6faf0e2a0a9ce1'
# }

# files = {'image': open('ImgName' + '.jpg', 'rb')}
# payload= {"gallery_name":"CNProj"} #MyGallery"}
# r = requests.post(url, headers=headers, data=payload, files=files)

# print(r.status_code, r.text)
# print(.find(200))

# r = xyz()
# print(r)
# # import requests

# url = "https://api.kairos.com/verify"
# headers = {
# 	    'app_id': '5c6933d9',
# 	    'app_key': '673c678af63f93255d6faf0e2a0a9ce1'
#     }

# x = str(3) 
# files = {'image': open(x + '_26.jpg', 'rb')}
# payload= {"gallery_name":"MyGallery", "subject_id":"SRT"}
# r = requests.post(url, headers=headers, data=payload, files=files)

# print (r.text)

# # def ReadAndParseJSON():
# # 	fName = input('Enter file name: ')
# # 	if (len(fName) < 1): fName = 'roster_data.json'
# # 	fHandle = open(fName).read()
# # 	stuff = json.loads(fHandle)
# # 	return stuff

# def LookUp(content):
# 	data = json.loads(r.text)
# 	LookUp(data)
# 	print(len(content["images"][0]["candidates"]))
# 	status = content["images"][0]["transaction"]["status"]
# 	Id = content["images"][0]["transaction"]["subject_id"]
# 	confidence = content["images"][0]["transaction"]["confidence"]
	# for keys, values in content.items():
	# 	print(keys[0])
	# 	course_Title = item[1]
	# 	role = item[2]

# urlHandle =r.text.read()
# data = json.loads(r.text)
# LookUp(data)
# print(data)