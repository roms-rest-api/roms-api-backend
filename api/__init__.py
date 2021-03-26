from api.helpers.configs.devices import DevicesConfig
from api.helpers.gdrive.gdrive import GoogleDriveTools

import yaml
import os
import magic
import shutil

from fastapi import FastAPI
from github import Github
from loguru import logger

app = FastAPI()
config: dict = None
devices = DevicesConfig()
gdrive = GoogleDriveTools()
tmp_path = f"{os.getcwd()}/api/tmp/"
mime = magic.Magic(mime=True)

with open("config.yaml", "r") as config_file:
    config = yaml.load(config_file.read(), Loader=yaml.FullLoader)

github_instance = Github(config['core']['github_token'])
folder_id = config['core']['folder_id']

logger.add("backend.log", rotation="1 week")
logger.info("Cleaning up directories")
if os.path.isdir("api/tmp"):
    shutil.rmtree("api/tmp")
os.mkdir("api/tmp")


from api.main import main

main()
