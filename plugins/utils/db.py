import motor.motor_asyncio as m
import configparser
import os
import sys

class DataBase():
    def __init__(self):
        config_path = os.path.join(sys.path[0], 'config.ini')
        config = configparser.ConfigParser()
        config.read(config_path)
        db_url = config.get("pyrogram", "db_url")
        self._DB = m.AsyncIOMotorClient(db_url).Dragon_Userbot
    
    async def set(self, module: str, variable: str, value):
        modcollection = self._DB[module] 
        doc = (await modcollection.find_one({'var': variable}))
        if doc == None:
            res = (await modcollection.insert_one({'var': variable, 'val': value}))
            doc = (await modcollection.find_one({'_id': res.inserted_id}))
        else:
            res = (await modcollection.replace_one(doc, {'var': variable, 'val': value}))
            doc = (await modcollection.find_one({'var':variable}))
        return {doc['var']: doc['val']}
    
    async def get(self, module: str, variable: str, expected_value = None):
        modcollection = self._DB[module]
        doc = (await modcollection.find_one({'var': variable}))
        if doc == None:
            return expected_value
        else:
            return doc['val']
    
    async def get_collection(self, module: str):
        modcollection = self._DB[module] 
        cons = []
        async for _ in modcollection.find():
            cons.append({_["var"]: _["val"]})
        return cons

db = DataBase()

