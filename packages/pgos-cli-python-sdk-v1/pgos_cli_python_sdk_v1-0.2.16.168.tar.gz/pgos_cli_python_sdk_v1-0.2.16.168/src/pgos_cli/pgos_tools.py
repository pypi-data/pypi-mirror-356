# -*- coding=utf-8
# tool functions

import hashlib
import requests
import time
from datetime import datetime
import json

import json
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

import pgos_cli.pgos_cmdline as pgos_cmdline
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def format_secret_key(input_string):
    output_string = input_string.split('-', 1)[1]
    output_string = output_string.replace('-', '')
    return output_string.encode('utf-8')

def GenerateServerTicket(title_region_id, secret_key, title_id):
    sever_key_array = secret_key.split('-')
    data = {
        "title_id": title_id,
        "title_region_id": title_region_id,
        "secret_id": sever_key_array[0],
        "time": int(time.time()),
    }
    json_data = json.dumps(data).encode('utf-8')

    # aes key
    aes_key = format_secret_key(secret_key)

    # IV
    iv = b'$3,.\'/&^rgnjkl!#'

    cipher = AES.new(aes_key, AES.MODE_CBC, iv)

    padded_data = pad(json_data, AES.block_size, style='pkcs7')
    encrypted_data = cipher.encrypt(padded_data)

    server_ticket = base64.b64encode(encrypted_data).decode('utf-8')

    return server_ticket



def Pretty(dict):
    return json.dumps(dict, indent=4, ensure_ascii=False)

def HashDict(dick, extra):
    sorted_keys = sorted(dick.keys())
    plain_text = ''
    for key in sorted_keys:
        plain_text += str(dick[key])
    plain_text += extra
    cipher_text = hashlib.sha256(plain_text.encode('utf-8')).hexdigest()
    # print(plain_text)
    # print(cipher_text)
    return cipher_text

def HttpPost(req_url, req_body):
    s = json.dumps(req_body)
    LogT('<< --- call REST api --- >>')
    LogT('url: ' + req_url)
    LogT('req:', True)
    LogT(Pretty(req_body), True)
    r = requests.post(req_url, json = req_body, verify = False)

    rsp_body = {}
    try:
        rsp_body = json.loads(s = r.text)
        LogT('rsp:', True)
        LogT(Pretty(rsp_body), True)
    except:
        pass

    if len(rsp_body) == 0:
        rsp_body['errno'] = 40000
        rsp_body['errmsg'] = 'Server internal error. Contact PGOS team please.'
    return rsp_body

def HttpPostWithHeaders(req_url, req_body, headers):
    s = json.dumps(req_body)
    LogT('<< --- call REST api --- >>')
    LogT('url: ' + req_url)
    LogT('req:', True)
    LogT(Pretty(req_body), True)
    LogT(Pretty(headers), True)

    r = requests.post(req_url, headers = headers, json = req_body, verify = False)
    rsp_body = {}
    try:
        rsp_body = json.loads(s = r.text)
        LogT('rsp:', True)
        LogT(Pretty(rsp_body), True)
    except:
        pass

    if len(rsp_body) == 0:
        rsp_body['errno'] = 40000
        rsp_body['errmsg'] = 'Server internal error. Contact PGOS team please.'
    return rsp_body

def ErrorMsg(msg):
    print('\n\033[1;37;41m%s\033[0m' % msg, flush=True)

def WarnningMsg(msg):
    print('\n\033[1;33;41m%s\033[0m' % msg, flush=True)
    
def LogT(text, verbose = False):
    if verbose and not pgos_cmdline.VerboseLog():
        return
    stamp = time.time()
    time_array = time.localtime(stamp)
    time_str = time.strftime('%Y-%m-%d %H:%M:%S  ', time_array)
    print(time_str + text + '\n', flush=True)
