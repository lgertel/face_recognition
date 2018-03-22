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
                    r = requests.post('http://192.168.1.101:1880/find-face', data = {'_id':name})
                    print("call done")
            else:
                r = requests.post('http://192.168.1.101:1880/no-face')


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
