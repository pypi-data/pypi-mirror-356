# -*- coding=utf-8
# sys
import sys, os
import logging
import json
import threading
import time

# s3
import boto3
from botocore.config import Config
from boto3.s3.transfer import TransferConfig

# pgos
import pgos_cli.pgos_cmdline as pgos_cmdline
import pgos_cli.pgos_backend_apis as pgos_backend_apis
from pgos_cli.pgos_cli_config import *
import pgos_cli.pgos_tools as pgos_tools

pKB = 1024
pMB = pKB * pKB


def SafeGetValue(dict, keys = []):
    for key in keys:    
        if key in dict:
            return dict[key]
    return ''


class ProgressPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()
        self.last_pro = 0

    def __call__(self, bytes_amount):
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            percentage = int(percentage)
            if percentage > self.last_pro:
                self.last_pro = percentage
                progress_info = 'build uploading progress: [%d / 100]' % self.last_pro
                if self.last_pro%10 == 0:
                    pgos_tools.LogT(progress_info)
                else:
                    pgos_tools.LogT(progress_info, True)
            # sys.stdout.write(
            #     "\r%s  %s / %s  (%.2f%%)" % (
            #         self._filename, self._seen_so_far, self._size,
            #         percentage))
            # sys.stdout.flush()
            
def MakeS3Config(region):
    return Config(
        region_name = region,
        # signature_version = 'v4',
        retries = {
            'max_attempts': 6,
            'mode': 'standard'
        },
        s3 = {
            'use_accelerate_endpoint': True
        }
    )
    
def MakeTransConfig():
    return TransferConfig(
        max_concurrency = 4,
        multipart_chunksize = 8 * pMB)
    

def UploadAsset(command_name, region, res_path, new:bool, cmd_params:dict):
    sig_api_list = [
        "request-build-upload-auth",     # [0]: 旧版
        "request-build-upload-auth-v2"   # [1]: 新版
    ]
    sig_api_2023_09_15 = "request-file-upload-auth"

    root_path, file_name = os.path.split(res_path)
    timestamp = time.time()

    # bucket_key = "cli/%s/%s/%s_%s" % (GetConfig('title-region'), command_name, str(int(timestamp)), file_name)
    # bucket_keys = [
    #     "%s_%s/%s_%s" % (GetTitleId(), GetConfig('title-region'), str(int(timestamp)), file_name), # [0]: 旧版
    #     "build/%s/%s_%s" % (GetConfig('title-region'), str(int(timestamp)), file_name)             # [1]: 新版
    # ]

    success = True    
    remain_try_cnt = 4

    while True:
        exc_msg = ''
        try:
            cosAuth = pgos_backend_apis.RequestCosSig(sig_api_2023_09_15, region, res_path, command_name, cmd_params)
            assetCredentials = SafeGetValue(cosAuth, ['BuildCredentials', 'AssetCredentials'])
            bucketName = SafeGetValue(cosAuth, ['BucketName'])
            bucketKey20230915 = SafeGetValue(cosAuth, ['BucketKey'])
            secretId = SafeGetValue(assetCredentials, ['TmpSecretId'])
            secretKey = SafeGetValue(assetCredentials, ['TmpSecretKey'])
            token = SafeGetValue(assetCredentials, ['Token'])
            region = cosAuth["IDC"]
            
            pgos_tools.LogT('\n<< --- upload asset with aws s3 --- >>')
            pgos_tools.LogT('asset path: ' + res_path)
            pgos_tools.LogT('bucket name: ' + bucketName)
            pgos_tools.LogT('bucket key: ' + bucketKey20230915)
            pgos_tools.LogT('region: ' + region)
            s3_client = boto3.client(
                's3',
                aws_access_key_id=secretId,
                aws_secret_access_key=secretKey,
                aws_session_token=token,
                config = MakeS3Config(region))

            s3_client.upload_file(
                res_path,
                bucketName,
                bucketKey20230915,
                Callback=ProgressPercentage(res_path),
                Config=MakeTransConfig())
        except Exception as e:
            exc_msg = str(e.args)
            success = False
        if success:
            break
        else:
            remain_try_cnt = remain_try_cnt - 1
            pgos_tools.LogT('s3 upload not complete, msg=' + exc_msg + '')
            if remain_try_cnt > 0:
                # retry with same bucket_key
                pgos_tools.LogT('retry [' + str(3-remain_try_cnt) + ']' + ' in 3 sec...')
                time.sleep(3)
                continue
            else:
                pgos_tools.LogT('try my best, but still failed to upload.')
                break
            
    if success:
        return bucketKey20230915
    else:
        return ''
    