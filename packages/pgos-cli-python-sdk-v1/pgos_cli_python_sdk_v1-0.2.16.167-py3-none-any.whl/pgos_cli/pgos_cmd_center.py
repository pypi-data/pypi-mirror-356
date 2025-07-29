# -*- coding=utf-8
# command center

import os
import sys
import requests
import json
from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum, auto
import time

import pgos_cli.pgos_cli_config as pgos_cli_config

# @dataclass
class Environment(Enum):
    Dummy = auto()
    Release = auto()
    Dev = auto()
    Test = auto()

@dataclass
class Configuration:
    index_commands: List[str]
    console_commands: List[str]
    index_path: str
    index_host_map: Dict[str, str]
    console_path: str
    console_host_map: Dict[str, str]

config = None  # Declare global variable
cache_folder = os.path.join(os.path.expanduser("~"), ".pgoscli", "Cache")  # Cache folder path
cache_file = os.path.join(cache_folder, "config.json")  # Cache file path
cache_expiration = timedelta(hours=1)  # Cache expiration time is 1 hour

def is_cache_valid() -> bool:
    return False
    # try:
    #     # Check if cache file exists
    #     with open(cache_file, "r") as file:
    #         data = json.load(file)

    #     # Check cache file expiration
    #     modified_time = datetime.fromtimestamp(data.get("timestamp", 0))
    #     current_time = datetime.now()
    #     if current_time - modified_time <= cache_expiration:
    #         return True

    # except (FileNotFoundError, json.JSONDecodeError):
    #     pass

    # return False

def save_to_cache(data: Dict):
    data["timestamp"] = datetime.now().timestamp()
    with open(cache_file, "w") as file:
        json.dump(data, file)

def download_json(env: Environment) -> Configuration:
    global config  # Declare global variable

    if is_cache_valid():
        # Read data from cache file
        with open(cache_file, "r") as file:
            data = json.load(file)
    else:
        # Define URLs for different environments
        env_urls = {
            Environment.Release: "https://cdn.pgos.intlgame.cn/ClientToolConfiguration_v1.json",
            Environment.Dev: "https://cdn.d-pgos.intlgame.cn/ClientToolConfiguration_v1.json",
            Environment.Test: "https://cdn.t-pgos.intlgame.cn/ClientToolConfiguration_v1.json"
        }

        # Select URL based on the environment
        url = env_urls.get(env)
        timestamp = int(time.time())
        url = f"{url}?t={timestamp}"

        try:
            # Send network request and get JSON data
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful
            data = response.json()

            # Create cache folder if it doesn't exist
            os.makedirs(cache_folder, exist_ok=True)

            # Save data to cache file
            save_to_cache(data)

        except requests.exceptions.RequestException as e:
            print("Request error:", e, flush=True)
            return {}
        except json.JSONDecodeError as e:
            print("JSON parsing error:", e, flush=True)
            return {}
        except Exception as e:
            print("An error occurred:", e, flush=True)
            return {}

    # Create Configuration object and store data
    config = Configuration(
        data["index_commands"],
        data["console_commands"],
        data["index_path"],
        data["index_host_map"],
        data["console_path"],
        data["console_host_map"]
    )

    return config

# @in command name
# @out full url
def ConstructCmdURL(cmd:str) -> str:
    envStr = pgos_cli_config.GetEnvStr()
    env = Environment.Dummy
    if envStr in ["release" , "r", "Release", "RELEASE"]:
        env = Environment.Release
    elif envStr in ["d", "dev", "Dev", "DEV"]:
        env = Environment.Dev
    elif envStr in ["t", "test", "Test", "TEST"]:
        env = Environment.Test
    else:
        # Default env
        env = Environment.Release

    cmd_ictionary = download_json(env)
    host = ""
    path = ""
    local_code = pgos_cli_config.GetLocalCode()
    if cmd in cmd_ictionary.index_commands:
        if env == Environment.Release:
            host = cmd_ictionary.index_host_map["default"]
        elif env == Environment.Test:
            host = cmd_ictionary.index_host_map["t"]
        elif env == Environment.Dev:
            host = cmd_ictionary.index_host_map["d"]
        path = cmd_ictionary.index_path
    elif cmd in cmd_ictionary.console_commands:
        if env == Environment.Test:
            host = cmd_ictionary.console_host_map["t"]
        elif env == Environment.Dev:
            host = cmd_ictionary.console_host_map["d"]
        elif env == Environment.Release:
            host = cmd_ictionary.console_host_map[local_code]
        path = cmd_ictionary.console_path
    else:
        print(f"invalid command: {cmd}", flush=True)
        os._exit(0)

    return f"https://{host}{path}"

# Test function
# env = "Release"  # Modify the environment as needed
# json_data = download_json(Environment.Dev)

# # Print the stored data
# if config:
#     print("index_commands:", config.index_commands)
#     print("console_commands:", config.console_commands)
#     print("index_path:", config.index_path)
#     print("index_host_map:", config.index_host_map)
#     print("console_path:", config.console_path)
#     print("console_host_map:", config.console_host_map)