import sys
sys.path.insert(0, './src')
sys.path.insert(0, '../src')

# import form pip package
import pgos_cli
from pgos_cli import PgosCliClient

import os
import json

pgos_cli_client = PgosCliClient()
pgos_cli_client.SetSecretKey("7FI5-GXYM-H3A0-M1Y8-L2HS")
pgos_cli_client.SetTitleID("5")
pgos_cli_client.SetVerifyType("UserAccount")
# pgos_cli_client.SetTitleRegion("your_title_region_id")
pgos_cli_client.SetPortalUser("will")
pgos_cli_client.SetPortalPsw("will")

def GenParamsJsonPath(command_name):
    # params_file_name = command_name + '.json'
    # root = os.path.dirname(os.path.abspath(__file__))
    # path = os.path.join(root, 'json_params_demo')
    # path = os.path.join(path, params_file_name)
    # return path

    params_file_name = command_name + '.json'
    root = os.path.dirname(os.path.abspath(__file__))
    # root = ""
    path = os.path.join(root, 'json_params_demo')
    path = os.path.join(path, params_file_name)
    print("[path]:" + path)
    return path

def GenUploadFilesJsonPath():
    root = os.path.dirname(os.path.abspath(__file__))
    upload_file_params_path = os.path.join(os.path.join(root, 'json_params_demo'), 'upload-files.json')
    return upload_file_params_path

def TestCommand(command_name, upload_files = False):
    if upload_files:
        ret = pgos_cli_client.ExecuteCommand(command_name, GenParamsJsonPath(command_name), GenUploadFilesJsonPath())
        if 'data' in ret:    
            print(json.dumps(ret['data'], indent=4))
        else:
            print( 'OOPS, command execute failed, pgosrid:[%s], errno:[%d], errmsg:%s' % (ret['pgosrid'], ret['errno'], ret['errmsg']) )
    else:
        ret = pgos_cli_client.ExecuteCommand(command_name, GenParamsJsonPath(command_name))
        if 'data' in ret:    
            print(json.dumps(ret['data'], indent=4))
        else:
            print( 'OOPS, command execute failed, pgosrid:[%s], errno:[%d], errmsg:%s' % (ret['pgosrid'], ret['errno'], ret['errmsg']) )

# ****************************************
# *             Test commands            *
# ****************************************

# print(pgos_cli_client.GetConfig())

pgos_help_root = pgos_cli_client.Help()
print(json.dumps(pgos_help_root, indent=4))

# avaliable_commands = pgos_help_root['data']['available_commands']
# for command in avaliable_commands:
#     help_ = json.dumps(pgos_cli_client.Help(command)['data'], indent=4)
#     print('\r', help_, end='', flush=True)

# print(json.dumps(pgos_cli_client.Help('list-build')['data'], indent=4))

# Noto: use this command to query available cloud resource 'Region':
# "Regions": [
#     "ap-guangzhou",
#     "ap-shanghai",
#     "eu-frankfurt",
#     "na-siliconvalley"
# ]
# TestCommand('list-cloud-resource-regions')

# TestCommand('list-build')

# TestCommand('build-systems')

# TestCommand('create-build', True)

# TestCommand('describe-build')

# TestCommand('delete-build')

# TestCommand('list-cvm-instance-type')

# TestCommand('create-fleet')

# TestCommand('delete-fleet')

# TestCommand('list-fleet')

# TestCommand('fleet-attributes')

# TestCommand('fleet-capacity')

# TestCommand('fleet-utilization')

# TestCommand('fleet-runtime-configuration')

# TestCommand('fleet-port-settings')

# TestCommand('fleet-scaling-policies')

# TestCommand('fleet-events')

# TestCommand('fleet-cvm-extend')

# TestCommand('update-fleet-attributes')

# TestCommand('update-fleet-capacity')

# TestCommand('set-fleet-scaling-auto')

# TestCommand('set-fleet-scaling-manual')

# TestCommand('update-fleet-runtime-configuration')

# TestCommand('update-fleet-port-settings')

# TestCommand('create-queue')

# TestCommand('update-queue')

# TestCommand('delete-queue')

# TestCommand('list-queue')

# TestCommand('get-quotas')

# TestCommand('describe-fleet-related-resources')
