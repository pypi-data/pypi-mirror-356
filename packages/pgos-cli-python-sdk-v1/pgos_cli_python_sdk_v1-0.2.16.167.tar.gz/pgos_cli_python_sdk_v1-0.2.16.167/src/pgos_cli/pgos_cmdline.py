# -*- coding=utf-8
# cmd line parser
import sys, os
import getopt
import configparser
import json

from dataclasses import dataclass, field
import pgos_cli.pgos_cli_config as pgos_cli_config

kOptionLoadJson = '--cli-load-json'
kOptionUploadFiles = '--cli-upload-files'
kOptionSetConfigFile = '--set-config-file'

kCmdHelp = 'help'
kCmdsUpdateCfg = [
    'set-title-id',
    'set-secret-key',
    'set-title-region',
    'set-env',
    'set-verify-type', # SecretKey, UserAccount
    'set-portal-user',
    'set-portal-pwd']

kCmdsConfigs = ['configs', 'config', 'configuration', 'cfg']
kGlobalHostCommands = ['help', 'list-cloud-resource-regions'] 


kTestWords = { 'test':1, 't':1 }

KDebugWords = { 'dev':1, 'debug':1, 'd':1 }

kVerboseWords = { '--v':1, '--verbose':1 }

gApiProtocol = 'https://'
gApiPrefix = 'p'
gApiDomain = 'gos.intlgame.com'
gApiDomainDev = 'gos.intlgame.cn'

gVerboseLog = False

gCmdline = []

@dataclass
class RawDataOption:
    option:str
    data:str

@dataclass
class StructDataOption:
    option:str
    data:dict

@dataclass
class Command:
    command:str
    options:list = field(default_factory=list)

#  run a command with test HTTP domain
def InitCmdline():
    global gApiProtocol
    global gApiPrefix
    global gApiDomain
    global gCmdline
    global gVerboseLog
    gCmdline = sys.argv
    print("------", flush=True)
    print(">> Original cmd: [" + " ".join(gCmdline) + "]", flush=True)
    for word in kVerboseWords:
        if word in gCmdline:
            gVerboseLog = True
            gCmdline.remove(word)

    if kOptionSetConfigFile in gCmdline:
        config_file_idx = gCmdline.index(kOptionSetConfigFile)
        pgos_cli_config.SetCustomCfgFile(gCmdline[config_file_idx + 1])
        del gCmdline[config_file_idx + 1]
        del gCmdline[config_file_idx]
    print(">> Pruned cmd: [" + " ".join(gCmdline) + "]", flush=True)


def GetApiProtocol():
    global gApiProtocol
    return gApiProtocol

def GetApiDomain():
    global gApiPrefix
    global gApiDomain
    return f'{gApiPrefix}{gApiDomain}'

def VerboseLog():
    global gVerboseLog
    return gVerboseLog

# help for command
def FillHelp():
    _command = Command('', [ StructDataOption('', {}) ])
    
    idx = 0
    for param in gCmdline:
        if param == 'help':
            _command.command = 'help'
            break
        idx += 1
    
    if idx > 1:
        _command.options[0].option = kOptionLoadJson
        _command.options[0].data['help_command'] = gCmdline[idx - 1]

    if _command.command != '' and len(_command.options[0].data) == 0:
        _command.options[0].option = kOptionLoadJson
        _command.options[0].data['help_command'] = 'pgos_cli'
    return _command

# def IsEvnTest():
#     global gEvnTest
#     return gEvnTest

# return options and params in format: --option-name param
def FillOptions():
    cmd = ""
    options_and_params = {}

    # first param will be regarded as a 'Command'
    if len(gCmdline) == 1:
        # no avaliable input, return help for pgos_cli
        c = Command('help', [ StructDataOption(kOptionLoadJson, {'help_command': 'pgos_cli'}) ])
        return c

    _command = Command(gCmdline[1])
    if len(gCmdline) == 2:
        return _command

    # handle configurtaion commands
    if _command.command in kCmdsUpdateCfg:
        _command.options.append(RawDataOption('', gCmdline[2]))
        return _command

    pure_argv = gCmdline[2:]

    idx = 0
    jump = False
    org_json_inputs = {} # json input source
    for obj in pure_argv:
        if jump:
            idx += 1
            jump = False
            continue
        if obj == kOptionLoadJson or obj == kOptionUploadFiles:
            org_json_inputs[obj] = pure_argv[idx + 1]
            jump = True
            idx += 1
        # if obj == kOptionSetConfigFile:
        #     pgos_cli_config.SetCustomCfgFile(pure_argv[idx + 1])

    for option in org_json_inputs:
        _command.options.append( StructDataOption(option, ParseCliJsonString(org_json_inputs[option])) )

    return _command


def IsOption(str):
    return str.startswith(u'--')

def ParseCliJsonString(data_res):
    print("------", flush=True)
    json_params = {}
    done = False
    try:
        json_params = json.loads(s = data_res)
        done = True
    except Exception as e:
        print(u'warnning: parsing ' + data_res + u' as JSON string failed: ' + str(e.args), flush=True)
    
    if done:
        return json_params
    
    root_dir = sys.path[0]
    joined_dir = os.path.normpath(os.path.join(root_dir, data_res))
    print(f'root dir:{root_dir}, json file dir:{joined_dir}', flush=True)
    
    try:
        f_content = open(joined_dir, encoding="utf-8").read()
        print(u'try: parsing ' + joined_dir + u' as local JSON file', flush=True)
        json_params = json.loads(s = f_content)
        done = True
    except Exception as e:
        print( u'warnning: parsing ' + joined_dir + ' as JSON file failed: ' + str(e.args), flush=True)

    if not done:
        print(u'err: when parsing data for ' + data_res, flush=True)
        os._exit(-1)

    return json_params

def MergeCommandParams(command):
    params = {}
    _command = command
    for option in _command.options:  # Preparing request params
        if option.option == kOptionLoadJson:
            params.update(option.data)
        if option.option == kOptionUploadFiles:
            if not isinstance(option.data, list):
                print('!!!! Oops, upload files params format error', flush=True)
                sys.exit(-1)
            for file_info in option.data:
                if not u'label' in file_info or not u'cos_path' in file_info:
                    # todo print error, abstruct 'function:FatalError()'
                    print('!!!! Oops, missing key of file_info of upload files', flush=True)
                    sys.exit(-1)
                params[ file_info['label'] ] = file_info[u'cos_path']
    return params