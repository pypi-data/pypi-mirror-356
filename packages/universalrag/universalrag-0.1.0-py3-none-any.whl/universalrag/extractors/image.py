# universalrag/extractors/image_extractor.py
import easyocr

reader = easyocr.Reader(['en'], gpu=False)

def extract_text_from_image(image_path):
    result = reader.readtext(image_path)
    return "\n".join([line[1] for line in result])
