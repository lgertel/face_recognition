import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys
import subprocess
import os
import requests
import face_recognition
import knn

old = 0
mainPath = os.getcwd()
class Watcher:
    DIRECTORY_TO_WATCH = sys.argv[1]
    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:  
                time.sleep(1)
                print(".")
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()

class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        global old
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            print("Received created event - %s." % event.src_path)
        elif event.event_type == 'modified':
            statbuf = os.stat('/home/pi/adtwelcome/knn/test/Unknown.jpeg')
            new = statbuf.st_mtime
            print(str(new) + " is new")
            print(str(old) + " is old")
            if (new - old) > 0.5:
                print("Received modified event - %s." % event.src_path)
                predictions = knn.predict("/home/pi/adtwelcome/knn/test/Unknown.jpeg", model_path="trained_knn_model.clf")
                if len(predictions) > 0:
                    for name, (top, right, bottom, left)  in predictions:
                        r = requests.post("http://192.168.1.101:1880/find-face", data = {"_id":name})
                else:
                    print("No face detected")
                    r =  requests.post("http://192.168.1.101:1880/no-face")


            old = new

if __name__ == '__main__':
    w = Watcher()
    w.run()
