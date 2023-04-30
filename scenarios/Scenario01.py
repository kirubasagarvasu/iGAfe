import keras_ocr
import cv2
# image = cv2.imread("D:\Data\Official\Solutions\Poco\AirtestScripts\Others\Total_Bet.png")
image = cv2.imread(r"D:\data\professional\airtestTesting\hillClimber\image_02.png")
pipeline = keras_ocr.pipeline.Pipeline()
# pipeline = keras_ocr.pipeline.Pipeline(preprocess_params={}) #to avoid conversion of lowercase and pre-processed parameters
#pipeline = keras_ocr.pipeline.Pipeline(preprocess_params={'apply_image': False})
# pip install --upgrade keras-ocr for params to work
predictions = pipeline.recognize([image]) #passing the image as list
text = ''
for prediction in predictions[0]:
    text += prediction[0] + ' '
print(text)
words = text.split()
#Sample output = 1511400 deal buy 12 31 5 2 30 bonus line 23 124 s00 pays total bet win spin 100000 32000 hold for auto features
# if "total" in words and "bet" in words:
if "casino" in words:
    print("Total bet found!")
else:
    print("Total bet not found.")