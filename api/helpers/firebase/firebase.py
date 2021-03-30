import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore
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
