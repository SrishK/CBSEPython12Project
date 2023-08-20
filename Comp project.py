import face_recognition #Uses logistics regression
import cv2 #To use computer vision
import numpy as np # To work with arrays
from datetime import datetime #Contains information of both date and time
from PIL import ImageGrab #For image processing
video_capture = cv2.VideoCapture(0) #0 because input from default webcam


sachin_image = face_recognition.load_image_file(r"C:\Users\91960\AppData\Local\Programs\Python\Python39\Sachin.jpeg")
#It will load my jpeg file into a numpy array/grid of homogeneous values.

sachin_encoding = face_recognition.face_encodings(sachin_image)[0]
#Returns a 128 dimension face encoding with 128 nodes for each loaded image.

harshini_image = face_recognition.load_image_file(r"C:\Users\91960\AppData\Local\Programs\Python\Python39\Harshini.jpeg")
harshini_encoding = face_recognition.face_encodings(harshini_image)[0]
adwait_image = face_recognition.load_image_file(r"C:\Users\91960\AppData\Local\Programs\Python\Python39\Adwait.jpeg")
adwait_encoding = face_recognition.face_encodings(adwait_image)[0]

srishti_image = face_recognition.load_image_file(r"C:\Users\91960\AppData\Local\Programs\Python\Python39\Srishti.jpeg")
srishti_encoding = face_recognition.face_encodings(srishti_image)[0]
known_face_encoding = [sachin_encoding,harshini_encoding,adwait_encoding,srishti_encoding]
known_face_names = ["Sachin","Harshini","Adwait","Srishti"]

students = known_face_names.copy()#Hard copy of names of students present in the database
face_locations = []
face_encoding = []
face_names = []
s = True

def Exit():
   video_capture.release()
   cv2.destroyAllWindows()
   quit()

now=datetime.now()#current_date= now.strftime("%Y-%m-%d")

while True:
  _,frame = video_capture.read()
  small_frame = cv2.resize(frame,(128,128),fx = 0.25, fy=0.25)
  #The image pixel size we are taking is 128*128 on x and y axis. TO conevrt BGR color (which OpenCV uses) to RGB color (which face_recognition uses).
 
  rgb_small_frame = small_frame[:,:,::-1]
  #Slicing to process only alternate nodes.
 
  if s:
      #Find all the faces and face encodings in the current frame of video
     
      face_locations= face_recognition.face_locations(rgb_small_frame)
      #If a face is present in the frame
     
      face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
      #Store face data of coming frame
     
      face_names = []
      for face_encoding in face_encodings:
          matches = face_recognition.compare_faces(known_face_encoding, face_encoding)
          ##Compare a list of face encodings against a candidate encoding to see if they match.
         
          name = ''
         
          face_distance = face_recognition.face_distance(known_face_encoding, face_encoding)
          '''Given a list of face encodings, compare them to a known face encoding and get a euclidean distance for each comparison face. The distance tells you how similar the faces are.'''
         
          best_match_index = np.argmin(face_distance)
          #Returns the indices of the minimum values along an axis.
         
          if matches[best_match_index]:
              name = known_face_names[best_match_index]
        
          face_names.append(name)
          if name in known_face_names:
              if name in students:
                  students.remove(name)
                  print("Present student:",name)
                  current_time = now.strftime("%H-%M-%S")
                  current_date= now.strftime("%Y-%m-%d")
                  f=open("Attendance.txt","a")
                  f.writelines([name," ",current_time," ",current_date,"\n"])
                  f.close()
 
  if input("Type q to quit")=="q":
   Exit()
