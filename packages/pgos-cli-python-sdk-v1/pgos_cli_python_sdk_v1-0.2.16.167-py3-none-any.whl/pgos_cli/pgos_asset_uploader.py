# -*- coding=utf-8
# cos wrapper

from math import fabs

import sys, os
import logging
import json
import threading
import time

import pgos_cli.pgos_cmdline as pgos_cmdline
import pgos_cli.pgos_backend_apis as pgos_backend_apis
from pgos_cli.pgos_cli_config import *
import pgos_cli.pgos_uploader_impl_cos as pgos_uploader_impl_cos
import pgos_cli.pgos_uploader_impl_s3 as pgos_uploader_impl_s3

# Step.1 Upload resource files to cloud cos
# Stpe.2 Fill back resource files' cos path to option's data
def PrepareResourceToUpload(command):
    def GetUploadFileOption(command_):
        if not isinstance(command_, pgos_cmdline.Command):
            return None
        for c in command_.options:
            if isinstance(c, pgos_cmdline.StructDataOption) and c.option == pgos_cmdline.kOptionUploadFiles:
                return c
        return None
    _option = GetUploadFileOption(command)
    # data of a upload-file-option must be a list
    if _option == None or not isinstance( _option.data, list):
        return command
    
    new_sig_api = True
    # if command.command.find("v2") != -1:
    #     new_sig_api = True

    for res_info in _option.data:
        bucket_key = ''
        if GetConfig('title-region').find('aws') != -1:
            bucket_key = pgos_uploader_impl_s3.UploadAsset(
                command.command,
                res_info['region'] if not new_sig_api else "", 
                res_info['path'], 
                new_sig_api,
                command.options[0].data)
        else:
            bucket_key = pgos_uploader_impl_cos.UploadAsset(
                command.command, 
                res_info['region'] if not new_sig_api else "", 
                res_info['path'], 
                new_sig_api,
                command.options[0].data)
            
        if len(bucket_key) > 0:
            res_info['cos_path'] = bucket_key
        else:
            print('err: upload resource file failed', flush=True)
            sys.exit(-1)
    return command