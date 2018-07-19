# -*- coding: utf-8 -*-
import tar_util
import ocr_util

if __name__ == '__main__':
    tar_rootdir = '/Volumes/data/tar'
    tar_target_path = '/Volumes/data/pdf'
    ocr_rootdir = '/Volumes/data/pdf'
    ocr_target_path = '/Volumes/data/txt'

    t = tar_util.TARUTIL(tar_rootdir,tar_target_path)
    ocr = ocr_util.OCRUTIL(ocr_rootdir,ocr_target_path)

    t.parse_tar_redis()
    ocr.ocr2txt_redis()