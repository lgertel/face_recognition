import sys
import time
import os
import requests
import face_recognition

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

import knn

class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.jpeg", "*.jpeg"]

    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        # the file will be processed there
        print(event.src_path, event.event_type)  # print now only for degug
        if (event.event_type == "modified"):
            picture_path = "./knn/test/Unknown.jpeg"

            # full_file_path = os.path.join("knn/test", picture_path)
            # print(full_file_path)

            print("Looking for faces in {}".format(picture_path))

            # Find all people in the image using a trained classifier model
            # Note: You can pass in either a classifier file name or a classifier model instance
            predictions = knn.predict(picture_path, model_path="trained_knn_model.clf")

            if len(predictions) > 0:
                # Print results on the console
                for name, (top, right, bottom, left) in predictions:
                    print("- Found {} at ({}, {})".format(name, left, top))
                    r = requests.post('http://10.10.10.168:1880/find-face', data = {'_id':name})
                    print("call done")
            else:
                r = requests.post('http://10.10.10.168:1880/no-face')

            # unknown_image = face_recognition.load_image_file(picture_path)
            #
            # try:
            #     know_faces_files = os.listdir("pictures_of_people_i_know")
            #     images = []
            #     known_face_encodings = []
            #
            #     current_image = 0
            #     known_face_names = []
            #     for f in know_faces_files:
            #         image_path = "./pictures_of_people_i_know/" + f
            #         images.append(face_recognition.load_image_file(image_path))
            #         known_face_encodings.append(face_recognition.face_encodings(images[current_image])[0])
            #         known_face_names.append(f.split(".")[0])
            #         current_image += 1
            #
            #     unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
            #
            #     # results is an array of True/False telling if the unknown face matched anyone in the known_faces array
            #     results = face_recognition.compare_faces(known_face_encodings, unknown_face_encoding)
            #
            #     name = "Unknown"
            #     if True in results:
            #         first_match_index = results.index(True)
            #         name = known_face_names[first_match_index]


            # except IndexError:
            #     r = requests.post('http://10.10.10.168:1880/no-face')


    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)


if __name__ == '__main__':
    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(MyHandler(), path=args[0] if args else '.')
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
