import os
import os.path
import cv2
import glob
import imutils


CAPTCHA_IMAGE_FOLDER = "dataSet"
OUTPUT_FOLDER = "extractedLetterImages"


# Get a list of all the captcha images we need to process
captcha_image_files = glob.glob(os.path.join(CAPTCHA_IMAGE_FOLDER, "*"))
counts = {}

if not os.path.exists("debug2"):
        os.makedirs("debug2")

# loop over the image paths
for (i, captcha_image_file) in enumerate(captcha_image_files):
    print("[INFO] processing image {}/{}".format(i + 1, len(captcha_image_files)))

    # Since the filename contains the captcha text (i.e. "2A2X.png" has the text "2A2X"),
    # grab the base filename as the text
    filename = os.path.basename(captcha_image_file)
    captcha_correct_text = os.path.splitext(filename)[0]

    # Load the image and convert it to grayscale
    image = cv2.imread(captcha_image_file)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Add some extra padding around the image
    gray = cv2.copyMakeBorder(gray, 8, 8, 8, 8, cv2.BORDER_REPLICATE)

    regions = 0
    length = len(captcha_correct_text)
    thresholdVal = 5
    while regions != length:

        if thresholdVal > 127:
            break
        # threshold the image (convert it to pure black and white)
        thresh = cv2.threshold(gray, thresholdVal, 255, cv2.THRESH_BINARY_INV)[1]# | cv2.THRESH_OTSU)[1]
        #thresh = cv2.threshold(gray, thresholdVal, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        # find the contours (continuous blobs of pixels) the image
        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

        dec = 0
        for i, contour in enumerate(contours):
            (x, y, w, h) = cv2.boundingRect(contour)

            if w < 9 and h < 9:
                dec += 1

            #for box in contours:
                #(xb, yb, wb, hb) = cv2.boundingRect(box)
                #if xb >= x and yb <= y:
                    #dec -= 1

        thresholdVal += 2
        regions = len(contours) - dec

    letter_image_regions = []

    # Now we can loop through each of the four contours and extract the letter
    # inside of each one
    for contour in contours:
        # Get the rectangle that contains the contour
        (x, y, w, h) = cv2.boundingRect(contour)

        if w < 9 and h < 9:
            continue

        breaker = False
        for box in contours:
            (xb, yb, wb, hb) = cv2.boundingRect(box)
            if xb > x and yb < y:
                breaker = True
        if breaker:
            continue

        # Compare the width and height of the contour to detect letters that
        # are conjoined into one chunk
        #if w / h > 1.5:
            # This contour is too wide to be a single letter!
            # Split it in half into two letter regions!
            #half_width = int(w / 2)
            #letter_image_regions.append((x, y, half_width, h))
            #letter_image_regions.append((x + half_width, y, half_width, h))
        #else:
            # This is a normal letter by itself
        letter_image_regions.append((x, y-3, w, h+3))

    # If we found more or less than 4 letters in the captcha, our letter extraction
    # didn't work correcly. Skip the image instead of saving bad training data!


    # Sort the detected letter images based on the x coordinate to make sure
    # we are processing them from left-to-right so we match the right image
    # with the right letter
    letter_image_regions = sorted(letter_image_regions, key=lambda x: x[0])

    #if len(letter_image_regions) != len(captcha_correct_text):
        #for box in letter_image_regions:
            #x, y, w, h = box


    #if len(letter_image_regions) != len(captcha_correct_text):
        #print("discard image {}.png".format(captcha_correct_text))
        #continue

    path = "debug2/" + filename
    output = cv2.merge([gray])

    # Save out each letter as a single image
    for letter_bounding_box, letter_text in zip(letter_image_regions, captcha_correct_text):
        # Grab the coordinates of the letter in the image
        x, y, w, h = letter_bounding_box

        cv2.rectangle(output, (x - 2, y - 2), (x + w + 2, y + h + 2), (0, 255, 0), 1)

        # Extract the letter from the original image with a 2-pixel margin around the edge
        letter_image = gray[y - 2:y + h + 2, x - 2:x + w + 2]

        # Get the folder to save the image in
        save_path = os.path.join(OUTPUT_FOLDER, letter_text)

        # if the output directory does not exist, create it
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # write the letter image to a file
        count = counts.get(letter_text, 1)
        p = os.path.join(save_path, "{}.png".format(str(count).zfill(6)))
        cv2.imwrite(p, letter_image)

        # increment the count for the current key
        counts[letter_text] = count + 1

    cv2.imwrite(path, output)
