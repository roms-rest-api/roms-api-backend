import firebase_admin

from firebase_admin import credentials, firestore, db
from loguru import logger


class FirebaseDatabase:
    def __init__(self, firebase_cert, project_id, firebase_rldb, rldb_builds, firebase_rldb_commits_db):
        """ initialize authenticated GDrive Object """
        cred = credentials.Certificate(firebase_cert)
        firebase_admin.initialize_app(cred, {"projectId": project_id})
        self.__db = firestore.client()
        self.__db_rldb = db.reference(url=firebase_rldb)
        self.__db_rldb_builds = rldb_builds
        self.__db_rldb_commits = firebase_rldb_commits_db

    def create_user(self, collection, username, data):
        """
        Creates an user as a document of the collection user
        collection: collection name
        username: username
        data: document as dict
        """
        self.__db.collection(collection).document(username).set(data)
        logger.info(f"Adding {collection} {username} as a maintainer")

    def get_user(self, username, collection):
        return self.__db.collection(collection).document(username).get()

    def delete_user(self, username, collection):
        return self.__db.collection(collection).document(username).delete()

    def get_rldb(self):
        return self.__db_rldb

    def get_builds_rldb(self):

        rldb = self.get_rldb()
        return rldb.child(self.__db_rldb_builds)

    def add_build(
        self,
        file_id: str,
        time: float,
        username: str,
        version: str,
        codename: str,
        changelog: str,
    ):
        device_ref = self.get_builds_rldb().child(codename).child(version)

        new_build_ref = device_ref.push()
        new_build_ref.set(
            {
                "gdrive_file_id": file_id,
                "timestamp": time,
                "uploader_username": username,
                "changelog": changelog,
            }
        )

    def get_commits_rldb(self):
        rldb = self.get_rldb()
        return rldb.child(self.__db_rldb_commits)

    def add_latest_commits(self, commit, codename):
        device_ref = self.__db_rldb.get_commits_rldb().child(codename)
        new_build_ref = device_ref.push()

        new_build_ref.set(
            {
                "changelog": commit,
            }
        )
