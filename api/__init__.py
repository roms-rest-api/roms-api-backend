import yaml
import os
import magic
import shutil

from fastapi import FastAPI
from github import Github
from loguru import logger

from api.helpers.configs.devices import DevicesConfig
from api.helpers.firebase.firebase import FirebaseDatabase

app = FastAPI()
config: dict = None
devices = DevicesConfig()
tmp_path = f"{os.getcwd()}/api/tmp/"
mime = magic.Magic(mime=True)
with open("config.yaml", "r") as config_file:
    config = yaml.load(config_file.read(), Loader=yaml.FullLoader)

github_instance = Github(config["core"]["github_token"])
drive_id = config["core"]["drive_id"]
firebase_cert = config["core"]["firebase_cred_file"]
firebase_project_id = config["core"]["firebase_project_id"]
firebase_collection_user = config["core"]["firebase_collection_user"]
firebase_collection_admin = config["core"]["firebase_collection_admin"]
firebase_rldb = config["core"]["firebase_rldb"]
rldb_builds = config["core"]["firebase_rldb_builds_db"]

firebase = FirebaseDatabase(
    firebase_cert=firebase_cert,
    project_id=firebase_project_id,
    firebase_rldb=firebase_rldb,
    rldb_builds=rldb_builds,
)

logger.add("backend.log", rotation="1 week")
logger.info("Cleaning up directories")
if os.path.isdir("api/tmp"):
    shutil.rmtree("api/tmp")
os.mkdir("api/tmp")


from api.main import main  # noqa: E402

main()
