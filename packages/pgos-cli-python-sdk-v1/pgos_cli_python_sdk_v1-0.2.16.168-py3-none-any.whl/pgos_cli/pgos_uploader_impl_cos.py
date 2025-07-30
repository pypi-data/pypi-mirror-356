# -*- coding=utf-8

from xmlrpc.client import boolean
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

import sys, os
import logging
import json
import threading
import time

import pgos_cli.pgos_cmdline as pgos_cmdline
import pgos_cli.pgos_backend_apis as pgos_backend_apis
from pgos_cli.pgos_cli_config import *
import pgos_cli.pgos_tools as pgos_tools

# const variables
kCosPartySize = 1    # MB
kCosMaxThread = 10
kCosProgressTag = "params=:"
kCosPartNumberTag = "\"partNumber\":"
kCosSigUpdateInternal = 15 * 60     # cos sig period: 15min

# global variables, may be changed
gProgressPerPart = 1.0 # Percentage of progress per part 
gTotalParts = 1
gCompletedParts = set()
gUploadRsp = ""
gUploadEnd = False

# --------------------------------------------------------------------------------------------
# Customized stream class
# parse upload progress from log info as below:
# INFO:qcloud_cos.cos_client:upload part,
#  url=:https://pgos-1300342678.cos.ap-guangzhou.myqcloud.com/test.txt,
#  headers=:{'x-cos-traffic-limit': None},
#  params=:{'uploadId': b'1607401619f5271fb7569496868f6419668fcd25ef5156dc898f630f0c1b4235f085e177a2', 'partNumber': 25}
# --------------------------------------------------------------------------------------------
class CustomPrint():
    def __init__(self):
        self.last_pro = 0
        # self.old_stdout=sys.stdout #save stdout

    def write(self, text):
        global gCompletedParts

        if text == "" or text == "\n":
            return

        # sys.stdout = self.old_stdout #restore normal stdout and print
        if text.find(kCosProgressTag) == -1:
            print("\n" + text, flush=True)
            return
        data = text[text.find(kCosProgressTag) + len(kCosProgressTag):]
        data = data.replace("'", '"')
        if data.find(kCosPartNumberTag) == -1:
            print("\n" + data, flush=True)
            return
        data = data[data.find(kCosPartNumberTag) + len(kCosPartNumberTag):]
        if data.find(',') == -1:
            part_number = data[:data.find('}')]
        else:
            part_number = data[:data.find(',')]
        part_number = part_number.strip()
        part_n = int(part_number)
        gCompletedParts.add(part_n)

        if len(gCompletedParts) == gTotalParts or part_n == gTotalParts:
            # progress_info = 'build uploading... progress \033[1;33m[100 / 100]\033[0m     '
            # print('\r', progress_info, flush=True)
            progress_info = 'build uploading progress: [100 / 100]'
            pgos_tools.LogT(progress_info)
        else:
            # similar pro
            similar_pro = float(gProgressPerPart * len(gCompletedParts))            
            if int(similar_pro) > self.last_pro:
                self.last_pro = int(similar_pro)
            
                # if int(similar_pro) == 100:
                #     similar_pro = 100.00
                # progress_info = 'build uploading... progress \033[1;33m[%.2f / 100]\033[0m     ' % similar_pro
                # print('\r', progress_info, end='', flush=True)
                progress_info = 'build uploading progress: [%d / 100]' % self.last_pro                
                if self.last_pro % 5 == 0:
                    pgos_tools.LogT(progress_info)
                else:
                    pgos_tools.LogT(progress_info, True)

def upload_percentage(consumed_bytes, total_bytes):
    """进度条回调函数，计算当前上传的百分比
    :param consumed_bytes: 已经上传的数据量
    :param total_bytes: 总数据量
    """
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        progress_info = 'build uploading progress: [%d / 100]' % rate                
        if rate % 5 == 0:
            pgos_tools.LogT(progress_info)
        else:
            pgos_tools.LogT(progress_info, True)


def UploadBuildFile(build_path, bucket_key, bucket_name, secret_id, secret_key, token, region):
    global gProgressPerPart
    global gTotalParts
    global gCompletedParts
    global gUploadRsp
    global gUploadEnd

    gCompletedParts.clear()

    logging.basicConfig(level=logging.INFO, stream=CustomPrint())
    # use accelerate as region when upload file to cos
    config = CosConfig(Region='accelerate', SecretId=secret_id, SecretKey=secret_key, Token=token)
    # config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token)
    client = CosS3Client(config, retry=6) # retry 3 time for each piece of data
    # client.update_conf(config)

    # build_size = os.path.getsize(build_path)
    # gTotalParts = int(build_size / 1024 / 1024 / 8)
    # if build_size % (1024 * 1024) != 0:
    #     gTotalParts = gTotalParts + 1
    # gProgressPerPart = ( "%.5f" % (100.0 / gTotalParts) )
    # gProgressPerPart = float(gProgressPerPart)

    # cos_sig_update_t = threading.Thread(target=ThreadFuncUpdateCosSig, args=(client, region, build_path, ))
    # cos_sig_update_t.start()

    success = False
    gUploadRsp = client.upload_file(
        Bucket = bucket_name,
        LocalFilePath = build_path,
        Key = bucket_key,
        PartSize = 8,
        MAXThread = 4,
        progress_callback = upload_percentage
    )
    gUploadEnd = True

    # wait 5 sec for cos_sig_update_t to exit
    # cos_sig_update_t.join(5)
    
    # if "ETag" not in gUploadRsp or "Key" not in gUploadRsp:
    #     return success, bucket_key
    # bucket_key = gUploadRsp["Key"]
    # success = True
    # return success, bucket_key

    if "ETag" not in gUploadRsp:
        return success, bucket_key
    success = True
    return success, bucket_key

def UploadAsset(command_name, region, res_path, new:bool, cmd_params:dict):
    sig_api_list = [
        "request-build-upload-auth",    # [0]: 旧版
        "request-build-upload-auth-v2"  # [1]: 新版
    ]
    sig_api_2023_09_15 = "request-file-upload-auth"

    root_path, file_name = os.path.split(res_path)
    timestamp = time.time()

    # bucket_key = "%s_%s/%s_%s" % (GetTitleId(), GetConfig('title-region'), str(int(timestamp)), file_name)
    # bucket_keys = [
    #     "%s_%s/%s_%s" % (GetTitleId(), GetConfig('title-region'), str(int(timestamp)), file_name), # [0]: 旧版
    #     "build/%s/%s_%s" % (GetConfig('title-region'), str(int(timestamp)), file_name)             # [1]: 新版
    # ]
    
    ret_bk = ""
    
    success = True
    remain_try_cnt = 4

    while True:
        exc_msg = ''
        try:
            cosAuth = pgos_backend_apis.RequestCosSig(sig_api_2023_09_15, region, res_path, command_name, cmd_params)
            assetCredentials = cosAuth['BuildCredentials']
            cosBucketName = cosAuth['BucketName']
            bucketKey20230915 = cosAuth['BucketKey']
            cosSecretId = assetCredentials['TmpSecretId']
            cosSecretKey = assetCredentials['TmpSecretKey']
            cosToken = assetCredentials["Token"]
            region = cosAuth["IDC"]
                
            pgos_tools.LogT('<< --- upload asset with cos --- >>')
            pgos_tools.LogT('asset path: ' + res_path)
            pgos_tools.LogT('bucket name: ' + cosBucketName)
            pgos_tools.LogT('bucket key: ' + bucketKey20230915)
            pgos_tools.LogT('region: ' + region)
            success, ret_bk = UploadBuildFile(res_path, bucketKey20230915, cosBucketName, cosSecretId, cosSecretKey, cosToken, region)
        except Exception as e:
            exc_msg = str(e.args)
            success = False
        if success:
            break
        else:
            remain_try_cnt = remain_try_cnt - 1
            pgos_tools.LogT('cos upload not complete, msg=' + exc_msg)
            if remain_try_cnt > 0:
                # retry with same bucket_key
                pgos_tools.LogT('retry [' + str(3-remain_try_cnt) + '] in 3 sec...')
                time.sleep(3)
                continue
            else:
                pgos_tools.LogT('try my best, but still failed to upload.')
                break

    if success:
        return ret_bk
    else:
        return ''