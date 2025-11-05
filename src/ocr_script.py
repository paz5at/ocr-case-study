# sources used: https://www.analyticsvidhya.com/blog/2024/04/ocr-libraries-in-python/
import easyocr
import re
import cv2

# create ocr reader using easyocr (might switch to doctr later)
reader = easyocr.Reader(['en'], gpu=False)

def preprocess_image(image_path: str):
    # read image using cv2
    image = cv2.imread(image_path)

    # convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # remove noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # apply thresholding to get binary image
    thresh = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 21, 10
    )

    # save preprocessed image temporarily
    preprocessed_path = "preprocessed_temp.png"
    cv2.imwrite(preprocessed_path, thresh)

    return preprocessed_path

def extract_text(image_path: str):
    preprocess_path = preprocess_image(image_path)
    results = []
    ocr_result = reader.readtext(image_path)

    # formatting
    for bbox, text, conf in ocr_result:
        cleaned = text.strip().capitalize()
        results.append((cleaned, round(float(conf), 2)))

    return results
