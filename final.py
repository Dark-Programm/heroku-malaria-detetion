import json

import cv2
import joblib
import numpy as np

im = cv2.imread("images/44.png", 0)
im = cv2.resize(im, (900, 720))
im = 255 - im

finalImage = None
finalResult = None

model = joblib.load("MalariaClassifier")

thresh1 = 190
thresh2 = 255

var = 700

clen = 0

if var < 600:
    width = np.asarray(im).shape[1] // 3
    height = np.asarray(im).shape[0] // 3

    imCropped = []

    for i in range(3):
        for j in range(3):
            imCropped.append(im[height * i:height * (i + 1), width * j:width * (j + 1)])

    count = 0

    for i in range(9):
        imCropped[i] = cv2.resize(imCropped[i], (400, 400))

        ret, thresh = cv2.threshold(imCropped[i], 190, 255, 0)
        contours, _ = cv2.findContours(thresh, 1, 2)

        clen += len(contours)

        imCropped[i] = cv2.cvtColor(imCropped[i], cv2.COLOR_GRAY2BGR)
        cv2.drawContours(imCropped[i], contours, -1, (0, 255, 0), 1)

        # Display individual image 1 by 1(optional)
        cv2.imshow("Window", imCropped[i])
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        area = []

        for j in range(5):
            try:
                area.append(cv2.contourArea(contours[j]))
            except:
                area.append(0.0)

        if area[0] == 0:
            area[0] = 15000
        area = np.asarray(area).reshape(1, -1)

        result = model.predict(area)

        if result == 'Parasitized':
            count += 1
            print("malaria at img no:", count + 1)

    if count > 0:
        finalResult = "Malaria Detected"
    else:
        finalResult = "No Malaria Detected"

    # print("Images Parasitized = ", count + 1)

    h1 = np.concatenate((imCropped[0], imCropped[1], imCropped[2]), axis=1)
    h2 = np.concatenate((imCropped[3], imCropped[4], imCropped[5]), axis=1)
    h3 = np.concatenate((imCropped[6], imCropped[7], imCropped[8]), axis=1)

    img = np.concatenate((h1, h2), axis=0)
    img = np.concatenate((img, h3), axis=0)

    finalImage = img

else:
    ret, thresh = cv2.threshold(im, 190, 255, 0)
    contours, _ = cv2.findContours(thresh, 1, 2)

    clen += len(contours)

    im = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(im, contours, -1, (0, 255, 0), 1)

    # print(contours)

    # Display Image (optional)
    # cv2.imshow("Image", im)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    area = []

    for j in range(5):
        try:
            area.append(cv2.contourArea(contours[j]))
        except:
            area.append(0.0)

    if area[0] == 0:
        area[0] = 15000

    area = np.asarray(area).reshape(1, -1)

    model = joblib.load("MalariaClassifier")

    result = model.predict(area)

    if result == 'Parasitized':
        finalResult = "Malaria Detected"
    else:
        finalResult = "No Malaria Detected"

    finalImage = im

# Final Image generated from one of the above 2 procedures
if finalImage is not None:
    cv2.imwrite("jsonDir/output.png", finalImage)

    cv2.imshow("Final Image", finalImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Final Result of the model
print(finalResult)

# No. of contors found
print("No. of contors found is:", clen)

# Writing to Json file
finalDictionary = {
    "Image": "jsonDir/output.png",
    "Result": finalResult
}

json_object = json.dumps(finalDictionary, indent=4)

with open("jsonDir/output.json", "w") as jsonOutFile:
    json.dump(finalDictionary, jsonOutFile)
