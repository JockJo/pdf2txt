# -*- coding: utf-8 -*-

import tarfile
import re
import os
import log_util
import redis_util

class TARUTIL:
    rootdir = ''
    target_path = ''
    log_filename = 'tar_log'
    log_filepath = './'
    l = log_util.Log(log_filename,log_filepath)

    def __init__(self, rootdir, target_path):
        self.rootdir = rootdir
        self.target_path = target_path

    #tar_path:tarc存储路径，包括tar的名字和.tar后缀
    #target_path:解压文件存储路径
    #此处解析出来的是pdf文件
    def parse_single_tar(self, tar_path, target_path):
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
                        print(file_name,tar_path)
        except Exception as e:
            self.l.print_log(e)

    def parse_tar(self):
        try:
            for parent,dirnames,filenames in os.walk(self.rootdir):
                for filename in filenames:
                    #filename包含文件后缀
                    tar_path = self.rootdir + "//" + filename
                    self.parse_single_tar(tar_path, self.target_path)
        except Exception as e:
            self.l.print_log(e)


    #配合redis使用，redis会存储已解析的文件的路径，不会重复解析
    def parse_tar_redis(self):
        try:
            for parent,dirnames,filenames in os.walk(self.rootdir):
                for filename in filenames:
                    #filename包含文件后缀
                    tar_path = self.rootdir + "//" + filename
                    redis_db = 1
                    redis = redis_util.Redis(redis_db)
                    if redis.__isexist__(filename):
                        continue
                    else:
                        self.parse_single_tar(tar_path, self.target_path)
                        redis.__store_item__(filename)
        except Exception as e:
            self.l.print_log(e)
