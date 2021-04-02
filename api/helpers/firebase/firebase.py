import firebase_admin

from firebase_admin import credentials, firestore, db
from loguru import logger


class FirebaseDatabase:
    def __init__(self, firebase_cert, project_id):
        """ initialize authenticated GDrive Object """
        cred = credentials.Certificate(firebase_cert)
        firebase_admin.initialize_app(cred, {"projectId": project_id})
        self.__db = firestore.client()

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
        from api import config

        return db.reference(url=config['core']['firebase_rldb'])

    def get_builds_rldb(self):
        from api import config

        rldb = self.get_rldb()
        return rldb.child(config['core']['firebase_rldb_builds_db'])

    def add_build(
        self,
        file_id: str,
        time: float,
        username: str,
        version: str,
        codename: str,
        changelog: str
    ):
        device_ref = self.get_builds_rldb().child(codename).child(version)

        new_build_ref = device_ref.push()
        new_build_ref.set({
            'gdrive_file_id': file_id,
            'timestamp': time,
            'uploader_username': username,
            'changelog': changelog
        })
