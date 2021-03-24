from api.helpers.configs.devices import DevicesConfig
import yaml

from fastapi import FastAPI
from github import Github

app = FastAPI()
config: dict = None
devices = DevicesConfig()

with open("config.yaml", "r") as config_file:
    config = yaml.load(config_file.read(), Loader=yaml.FullLoader)

github_instance = Github(config['core']['github_token'])

from api.main import main

main()
