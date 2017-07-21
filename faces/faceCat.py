import glob
import cv2


def cropFaces(globString):
    # paralellize this for SPEED
    # if it shits the bed with threads
    # use processes (hint: this is gonna happen)
    for filename in glob.glob(globString):
        cropFace(filename)


def cropFace(filename):
    pass


def getPicturesOfFaces(outDir):
    pass


def main():
    pass


if __name__ == "__main__":
    main()