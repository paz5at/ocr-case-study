# sources used: https://www.analyticsvidhya.com/blog/2024/04/ocr-libraries-in-python/
import easyocr
import re

# create ocr reader using easyocr (might switch to doctr later)
reader = easyocr.Reader(['en'], gpu=False)

def extract_text(image_path: str, conf_threshold: float = 0.6):
    results = []
    ocr_result = reader.readtext(image_path)

    # try to add cleaning later
    for bbox, text, conf in ocr_result:
        if conf >= conf_threshold:
            # minimal formatting
            cleaned = text.strip().capitalize()
            results.append((cleaned, round(float(conf), 2)))

    return results
