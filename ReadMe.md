Objective - The objective of this system is put automatic authentication system at home. This system uses two-step verification to determine whether guest at the door should be granted access or not. Two verification methods are ‘Face Recognition’ and Distance based Password’. Just to add extra security layer, a secondary verification is made by the owner by authorizing the guest using an android application.

Project Requirements
• Hardware
	▪ Raspberry Pi – Raspberry Pi 2B was used for this project
	▪ Distance Sensor – VL53L0X Time of Flight distance sensor was used for this project
	▪ Webcam – Fosmon USB webcam was used for face recognition
	▪ Server – AWS EC2 instance for this project
	▪ Speakers
	▪ USB Wi-Fi Adapter
	▪ Memory Card
	▪ Android Device
• Software
	▪ Face Recognition API – Kairos API was used along with OpenCV Face Recognizer
	▪ Voice Synthesizer API – Google Text-to-Speech API was used
	▪ Android Studio – For the development of android application
	▪ SQLite Database – For keeping track of user and corresponding distance

System Setup - Raspberry Pi is the central piece in this authentication system. Webcam, distance sensor and speakers are connected to the Raspberry Pi. An instance of AWS EC2 server needs to be invoked. The Android device needs to have the application installed.

Lessons Learnt - Learned both aspects of development i.e. server side and client side. Also, gained insights on networking, using image processing in real time and dealing with an integrated system.
