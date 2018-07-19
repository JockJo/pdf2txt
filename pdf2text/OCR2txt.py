from wand.image import Image
from PIL import Image as PI
import pytesseract
import io
import os
import os.path
import re

rootdir = r"E:/document/patent/patent_pdf"


def ocr2txt(src_path, ocr_name, target_path):
    req_image = []
    final_text = []

    image_pdf = Image(filename=src_path,
                      resolution=300)
    image_jpeg = image_pdf.convert('jpeg')
    for img in image_jpeg.sequence:
        img_page = Image(image=img)
        req_image.append(img_page.make_blob('jpeg'))
    for img in req_image:
        txt = pytesseract.image_to_string(
            PI.open(io.BytesIO(img)),
            lang ='eng')
        final_text.append(txt)

    upperdirs = os.path.dirname(target_path)
    if upperdirs and not os.path.exists(upperdirs):
        # Create directories that are not part of the archive with
        # default permissions.
        os.makedirs(upperdirs)

    ocr_name = ocr_name.replace('.pdf', '.txt')
    file_path =  os.path.join(target_path,ocr_name)
    with open(file_path, 'a', encoding='utf-8') as f:
        for text in final_text:
            f.write(text)



for parent,dirnames,filenames in os.walk(rootdir):
    target_path = r"E:/document/patent/patent_txt"
    for filename in filenames:
        ocr_path = rootdir + "//" + filename
        ocr2txt(ocr_path, filename, target_path)



