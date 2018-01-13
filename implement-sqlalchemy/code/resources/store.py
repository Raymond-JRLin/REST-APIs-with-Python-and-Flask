from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        pass

    def post(self, name):
        pass

    def delete(self, name):
        pass


class StoreList(Resource):
