import requests
from lxml import etree
from io import StringIO
import base64
import codecs
from keras.models import load_model
from helpers import resize_to_fit
from imutils import paths
import numpy as np
import imutils
import cv2
import pickle
import os
import glob
import time
try:
    import Image
except ImportError:
    from PIL import Image
from subprocess import check_output
import Solver

LETTER_MODEL_FILENAME = "captcha_model.hdf5"
LETTER_MODEL_LABELS_FILENAME = "model_labels.dat"

# folder to temporaliy save images
TEMP_CAPTCHA = "TEMP"
URL = "http://hax1.allesctf.net:9200/captcha/"

# init parser
parser = etree.HTMLParser()

# load labels for model
with open(LETTER_MODEL_LABELS_FILENAME, "rb") as f:
    LETTER_MODEL_LABELS = pickle.load(f)

# load the model
LETTER_MODEL = load_model(LETTER_MODEL_FILENAME)

# function to clear all temporaliy stored captchas
def clearFiles():
    files = glob.glob(TEMP_CAPTCHA + "/*")
    for f in files:
        os.remove(f)

# parse the html, decode base-64 images and then save them
def extractCaptchas(html):
    # turn into tree using html parser as spezifed above
    tree = etree.parse(StringIO(html), parser=parser)
    root = tree.getroot()

    try:
        # part of the DOM hirachy the contains the captchas
        captchas = root[1][1][1][1][1]
    except IndexError:
        return False

    # get all images and ecode and save
    # because ever captcha has a button below it only every second element is a image
    print("found " + str((len(captchas) - 1) // 2) + " captchas")

    for i in range(0, len(captchas) - 1, 2):
        img = captchas[i][0].attrib['src'][22:]

        # files name: 0-<num captchas>
        fileName = TEMP_CAPTCHA + "/{}.png".format(i//2)
        fh = open(fileName, "wb")

        imgData = img.encode('ASCII')
        fh.write(codecs.decode(imgData, encoding='base64'))
        fh.close()

    return True

# send the asnwers for a spezific stage with a session and store new captchas
def sendAnswers(session, stage, answers):
    print("seding answers")
    for key in answers:
        print(key + " : " + answers[key])

    # send as post requests with our answers
    response = session.post(URL+ str(stage), data=answers)

    # if we completed the last stage(3) save the flag and exit
    if not("fail" in response.url) and stage == 3:
        f = open("flag.html", "w")
        f.write(response.content.decode("utf-8"))
        f.close()
        print("flag found!!!")
        os._exit(0)

    # extract the images from the response
    return extractCaptchas(response.content.decode("utf-8"))

# use Solver.py to get the answers for every image in the temp folder and return a dict for a post requests
def getAllAnswers():
    # dict to hold all answers
    answers = {}
    # iterate over every file in temp folder
    for image_file in list(paths.list_images(TEMP_CAPTCHA)):

        filename = os.path.basename(image_file)

        # get answer as string from cv2 image
        image = cv2.imread(image_file)
        answer = Solver.solve(image)

        # save the answer as the filename
        answers[filename[:-4]] = answer

    return answers

# loop and solve captchas untill we got the flag
def main():
    # create temp folder if it doesn't exist
    if not os.path.exists(TEMP_CAPTCHA):
        os.makedirs(TEMP_CAPTCHA)

    # create a requests session to make all requests (using the same session cookie)
    requstSession = requests.Session()
    requstSession.headers['User-Agent'] = 'Mozilla/5'

    while True:
        time.sleep(0.5)
        # empy temp folder
        clearFiles()

        # get the first set of captchas for the start
        response = requstSession.get(URL + "0")
        extractCaptchas(response.content.decode("utf-8"))

        # complete baby stage
        asnwersS0 = getAllAnswers()
        if(not sendAnswers(requstSession, 0, asnwersS0)): continue

        # complete human stage
        asnwersS1 = getAllAnswers()
        if(not sendAnswers(requstSession, 1, asnwersS1)): continue

        # complete tool assisted stage
        asnwersS2 = getAllAnswers()
        if(not sendAnswers(requstSession, 2, asnwersS2)): continue

        # complete bot stage and get flag
        asnwersS3 = getAllAnswers()
        sendAnswers(requstSession, 3, asnwersS3)


if __name__ == "__main__":
    main()
