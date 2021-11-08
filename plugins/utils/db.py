import pymongo as md
import configparser
import os
import sys


class DataBase():
    def __init__(self):
        config_path = os.path.join(sys.path[0], 'config.ini')
        config = configparser.ConfigParser()
        config.read(config_path)
        db_url = config.get("pyrogram", "db_url")
        db_name = config.get("db", "db_name")
        self._DB = md.MongoClient(db_url)[db_name]
    
    def set(self, module: str, variable: str, value):
        modcollection = self._DB[module] 
        doc = modcollection.find_one({'var': variable})
        if doc is None:
            modcollection.insert_one({'var': variable, 'val': value})
        else:
            modcollection.replace_one(doc, {'var': variable, 'val': value})
        return True
    
    def get(self, module: str, variable: str, expected_value = None):
        modcollection = self._DB[module]
        doc = modcollection.find_one({'var': variable})
        if doc is None:
            return expected_value
        else:
            return doc['val']
    
    def get_collection(self, module: str):
        modcollection = self._DB[module] 
        cons = []
        for _ in modcollection.find():
            cons.append({_["var"]: _["val"]})
        return cons

    def remove(self, module: str, variable: str):
        modcollection = self._DB[module] 
        doc = modcollection.find_one({'var': variable})
        if doc != None:
            modcollection.delete_one(doc)
            return True
        else:
            return False

db = DataBase()

