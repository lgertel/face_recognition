import face_recognition
import cv2
import os
import requests
import time

welcome = requests.post('https://adtwelcome.mybluemix.net/welcome')
video_capture = cv2.VideoCapture(0)
# time.sleep(2)
video_capture = cv2.VideoCapture(0)
ret, frame = video_capture.read()

picture_path = "unknown_pictures/Unknown.png"
cv2.imwrite(picture_path,frame)

unknown_image = face_recognition.load_image_file(picture_path)

try:
    know_faces_files = os.listdir("pictures_of_people_i_know")
    images = []
    known_face_encodings = []

    current_image = 0
    known_face_names = []
    for f in know_faces_files:
        image_path = "./pictures_of_people_i_know/" + f
        images.append(face_recognition.load_image_file(image_path))
        known_face_encodings.append(face_recognition.face_encodings(images[current_image])[0])
        known_face_names.append(f.split(".")[0])
        current_image += 1

    unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
except IndexError:
    print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
    quit()


# results is an array of True/False telling if the unknown face matched anyone in the known_faces array
results = face_recognition.compare_faces(known_face_encodings, unknown_face_encoding)

name = "Unknown"
if True in results:
    first_match_index = results.index(True)
    name = known_face_names[first_match_index]

r = requests.post('https://adtwelcome.mybluemix.net/find_face', data = {'_id':name})

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
