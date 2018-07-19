#!/usr/bin/env/python3
# -*- coding: utf-8 -*-

import tarfile
import re


class TARUTIL:
    def parse_tar_file(tar_path, target_path):
        #target_path = "E:\\document\patent\patent_pdf"
        try:
            with tarfile.open(tar_path, "r:") as tar:
                file_names = tar.getnames()
                for file_name in file_names:
                    fname_str = ''+file_name
                    fname_str = re.search(r'[0-9a-zA-Z]*.pdf', fname_str)
                    if fname_str:
                        fname_str = fname_str.group()
                        member = tar.getmember(file_name)
                        member.name = fname_str         #因为库中根据这个参数创建存储路径，此处修改为自定义想存储的路径
                        tar.extract(member,target_path)
                        #print(file_name)
        except Exception as e:
            print(e)

#if __name__ == '__main__':
#    parse_tar_file(r'E:\document\patent\grant_pdf_20180102.tar')