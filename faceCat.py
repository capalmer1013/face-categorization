"""
An Api for categorizing faces based off similarities
to eigenfaces

Notes:
    # cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    # NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
    # Crop from x, y, w, h -> 100, 200, 300, 400    img[200:400, 100:300]
"""
import os
import sys
import glob
import threading
import subprocess
import time
import cv2

face_cascade = cv2.CascadeClassifier('opencvData/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('opencvData/haarcascades/haarcascade_eye.xml')
outFileDir = "faces/"
inFileDir = "faces/samplefaces/"

class FuncThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)

    def run(self):
        self._target(*self._args)


def cropFacesThreaded(globString):
    activeThreads = []

    for filename in glob.glob(globString):
        tmp = FuncThread(cropFace, filename)
        tmp.start()
        activeThreads.append(tmp)

    for i in range(len(activeThreads)):  # wait for any remaining subrocesses
        activeThreads[i].join()



def cropFacesSubProcess(globString):
    childProcesses = []

    for filename in glob.glob(globString):
        childProcesses.append(subprocess.Popen(["python", "faceCat.py", filename]))

    for i in range(len(childProcesses)):  # wait for any remaining subprocesses
        childProcesses[i].wait()


def cropFaces(globString):
    activeThreads = []

    for filename in glob.glob(globString):
        cropFace(filename)


def cropFace(filename):
    img = cv2.imread(filename)
    name, file_extension = os.path.splitext(filename)
    name = name[name.rfind("/")+1:]

    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            crop_img = img[y:y+h, x:x+w]
            cv2.imwrite(outFileDir+name+"-cropped"+file_extension, crop_img)

    except Exception as e:
        print "exception", e


def getPicturesOfFaces(outDir):
    # this will be to use some external source to grab
    # pictures of peoples faces
    pass


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cropFace(sys.argv[1])
    else:
        startTime = time.time()
        cropFacesSubProcess(inFileDir)
        print time.time() - startTime