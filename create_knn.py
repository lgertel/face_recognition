import os, errno
import pathlib

directory = os.fsencode("/Users/lgertel/adtwelcome/pictures_of_people_i_know/")

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".jpeg"):
        dirname = filename.split(".")[0]
        try:
            print(dirname)
            pathlib.Path("/Users/lgertel/adtwelcome/knn/train/" + dirname).mkdir(parents=True, exist_ok=True)
            os.rename("/Users/lgertel/adtwelcome/pictures_of_people_i_know/" + filename, "/Users/lgertel/adtwelcome/knn/train/" + dirname + "/img01.jpeg")
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        continue
    else:
        continue
import os, errno

try:
    os.makedirs(directory)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
