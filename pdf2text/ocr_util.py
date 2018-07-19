# -*- coding: utf-8 -*-
from wand.image import Image
from PIL import Image as PI
import pytesseract
import io
import os
import os.path
import redis_util
import log_util


class OCRUTIL:
    rootdir = ''
    target_path = ''
    log_filename = 'orc_log'
    log_filepath = './'
    l = log_util.Log(log_filename,log_filepath)

    def __init__(self, rootdir, target_path):
        self.rootdir = rootdir
        self.target_path = target_path

    #内部函数
    #src_path:pdf的存储路径
    #orc_name:pdf的名字
    #target_path:转换成的txt存储路径
    def single_ocr2txt__(self, src_path, ocr_name, target_path):
        req_image = []
        final_text = []

        image_pdf = Image(filename=src_path,
                          resolution=300)
        image_jpeg = image_pdf.convert('jpeg')
        for img in image_jpeg.sequence:
            # 将pdf分割成图片
            img_page = Image(image=img)
            req_image.append(img_page.make_blob('jpeg'))
        for img in req_image:
            # 将图片提取出文本
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
            #存储文本
            for text in final_text:
                f.write(text)

    #不具备重复检查
    def ocr2txt(self):
        try:
            for parent,dirnames,filenames in os.walk(self.rootdir):
                for filename in filenames:
                    #filename包含文件后缀
                    ocr_path = self.rootdir + "//" + filename
                    self.single_ocr2txt__(ocr_path, filename, self.target_path)
        except Exception as e:
            self.l.print_log(e)

    #配合redis使用，redis会存储已解析的文件的路径，不会重复解析
    def ocr2txt_redis(self):
        try:
            for parent,dirnames,filenames in os.walk(self.rootdir):
                for filename in filenames:
                    #filename包含文件后缀
                    ocr_path = self.rootdir + "//" + filename
                    redis_db = 0
                    redis = redis_util.Redis(redis_db)
                    if redis.__isexist__(filename):
                        continue
                    else:
                        self.__ocr2txt__(ocr_path, filename, self.target_path)
                        redis.__store_item__(filename)
        except Exception as e:
            self.l.print_log(e)
