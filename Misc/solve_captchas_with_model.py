from keras.models import load_model
from helpers import resize_to_fit
from imutils import paths
import numpy as np
import imutils
import cv2
import pickle
import os


LETTER_MODEL_FILENAME = "captcha_model.hdf5"
LETTER_MODEL_LABELS_FILENAME = "model_labels.dat"
LENGHT_MODEL_FILENAME = "captcha_model_len.hdf5"
LENGHT_MODEL_LABELS_FILENAME = "model_labels_len.dat"
CAPTCHA_IMAGE_FOLDER = "dataSet"


# Load up the model labels (so we can translate model predictions to actual letters)
with open(LETTER_MODEL_LABELS_FILENAME, "rb") as f:
    lb_letter = pickle.load(f)

with open(LENGHT_MODEL_LABELS_FILENAME, "rb") as f:
    lb_lenght = pickle.load(f)

# Load the trained neural network
letter_model = load_model(LETTER_MODEL_FILENAME)

lenght_model = load_model(LENGHT_MODEL_FILENAME)

# Grab some random CAPTCHA images to test against.
# In the real world, you'd replace this section with code to grab a real
# CAPTCHA image from a live website.
captcha_image_files = list(paths.list_images(CAPTCHA_IMAGE_FOLDER))
#captcha_image_files = np.random.choice(captcha_image_files, size=(10,), replace=False)

def predictLenght(image):

    newW = 400
    (h, w) = image.shape[:2]

    paddingWL = (newW - w) / 2
    paddingWR = int(paddingWL)
    if paddingWL != int(paddingWL):
        paddingWL += 1

    image = cv2.copyMakeBorder(image, top=0, bottom=0, left=int(paddingWL), right=paddingWR, borderType=cv2.BORDER_REPLICATE)
    image = np.expand_dims(image, axis=2)
    image = np.expand_dims(image, axis=0)

    prediction = lenght_model.predict(image)
    lenght = lb_lenght.inverse_transform(prediction)[0]

    return lenght

def predict(image, letter_image_regions, output):
    # loop over the letters
    predictions = []
    for letter_bounding_box in letter_image_regions:
        # Grab the coordinates of the letter in the image
        x, y, w, h = letter_bounding_box

        # Extract the letter from the original image with a 2-pixel margin around the edge
        letter_image = image[y - 2:y + h + 2, x - 2:x + w + 2]

        # Re-size the letter image to 20x20 pixels to match training data
        letter_image = resize_to_fit(letter_image, 20, 20)

        # Turn the single image into a 4d list of images to make Keras happy
        letter_image = np.expand_dims(letter_image, axis=2)
        letter_image = np.expand_dims(letter_image, axis=0)

        # Ask the neural network to make a prediction
        prediction = letter_model.predict(letter_image)

        # Convert the one-hot-encoded prediction back to a normal letter
        letter = lb_letter.inverse_transform(prediction)[0]
        predictions.append(letter)

        cv2.rectangle(output, (x - 2, y - 2), (x + w + 4, y + h + 4), (0, 255, 0), 1)
        cv2.putText(output, letter, (x - 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)

    return "".join(predictions)

def conturesToRegions(contours, split=True, ratio=1.3):
    letter_image_regions = []

    # Now we can loop through each of the four contours and extract the letter
    # inside of each one
    for contour in contours:
        # Get the rectangle that contains the contour
        (x, y, w, h) = cv2.boundingRect(contour)

        if w < 9 and h < 9:
            continue

        # Compare the width and height of the contour to detect letters that
        # are conjoined into one chunk
        if split:
            if w / h > ratio:
                # This contour is too wide to be a single letter!
                # Split it in half into two letter regions!
                half_width = int(w / 2)
                letter_image_regions.append((x, y, half_width, h))
                letter_image_regions.append((x + half_width, y, half_width, h))
            else:
                # This is a normal letter by itself
                letter_image_regions.append((x, y, w, h))
        else:
            letter_image_regions.append((x, y, w, h))

    return letter_image_regions

thresholdVal = 0

def solveCaptchas(image_file):
    global thresholdVal
    # Load the image and convert it to grayscale
    filename = os.path.basename(image_file)

    image = cv2.imread(image_file)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    lenght = len(filename[:-4])#int(predictLenght(image))
    # Add some extra padding around the image
    image_b = cv2.copyMakeBorder(image, 20, 20, 20, 20, cv2.BORDER_REPLICATE)

    regions = 0
    thresholdVal = 5
    while regions != lenght:

        if thresholdVal > 127:
            break
        # threshold the image (convert it to pure black and white)
        thresh = cv2.threshold(image_b, thresholdVal, 255, cv2.THRESH_BINARY_INV)[1]# | cv2.THRESH_OTSU)[1]

        # find the contours (continuous blobs of pixels) the image
        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

        dec = 0
        for i, contour in enumerate(contours):
            (x, y, w, h) = cv2.boundingRect(contour)

            if w < 9 and h < 9:
                dec += 1

        thresholdVal += 2
        regions = len(contours) - dec

    letter_image_regions = conturesToRegions(contours, split=False)
    letter_image_regions = sorted(letter_image_regions, key=lambda x: x[0])

    output = cv2.merge([image_b] * 3)

    captcha_text_split = predict(image_b, letter_image_regions, output)

    #letter_image_regions = conturesToRegions(contours, split=False)
    #letter_image_regions = sorted(letter_image_regions, key=lambda x: x[0])

    #captcha_text_nosplit = predict(image_b, letter_image_regions, output)
    return captcha_text_split
    result = ""


'''
image_file = "dataSet/00G6BGV583.png"
filename = os.path.basename(image_file)

image = cv2.imread(image_file)
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

image_b = cv2.copyMakeBorder(image, 20, 20, 20, 20, cv2.BORDER_REPLICATE)
thresh = cv2.threshold(image_b, 10, 255, cv2.THRESH_BINARY_INV)[1]# | cv2.THRESH_OTSU)[1]

contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
letter_image_regions = conturesToRegions(contours, split=False)

print(len(letter_image_regions))

for box in letter_image_regions:
    x, y, w, h = box
    cv2.rectangle(thresh, (x, y), (x + w, y + h), (255, 255, 255), 1)

cv2.imwrite("test.png", thresh)

'''
if not os.path.exists("debug"):
        os.makedirs("debug")

n = 0
m = 0
for image_file in captcha_image_files:
    # Load the image and convert it to grayscale
    answer = solveCaptchas(image_file)

    filename = os.path.basename(image_file)

    if answer != filename[:-4]:

        print("CAPTCHA text is: {}".format(filename))
        #print("CAPTCHA predicted lenght is: {}".format(lenght))
        #print("CAPTCHA prediction split is: {}".format(captcha_text_split))
        #print("CAPTCHA prediction no split is: {}".format(captcha_text_nosplit))
        print("CAPTCHA final prediction is: {}".format(answer))

        filename = os.path.basename(image_file)

        image = cv2.imread(image_file)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        image_b = cv2.copyMakeBorder(image, 20, 20, 20, 20, cv2.BORDER_REPLICATE)
        thresh = cv2.threshold(image_b, thresholdVal, 255, cv2.THRESH_BINARY_INV)[1]# | cv2.THRESH_OTSU)[1]

        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        letter_image_regions = conturesToRegions(contours, split=False)

        for box in letter_image_regions:
            x, y, w, h = box
            cv2.rectangle(image_b, (x - 2, y - 2), (x + w + 2, y + h + 2), (0, 255, 0), 1)

        cv2.imwrite("debug/" + filename, image_b)


        #os._exit(1)

        m += 1
    n += 1
    if n % 100 == 0:
        print(n)

print(m)
print(n)
print(1 - (m/n))
    #p = "test/" + filename
    #if not os.path.exists("test"):
            #os.makedirs("test")
    #cv2.imwrite(p, output)
