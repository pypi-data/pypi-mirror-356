import os
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

class AIAWH40KRepository:
  aiaDB: None

  def __init__(self, connectionString):
    connectiondmr = MongoClient(connectionString)
    self.aiaDB = connectiondmr["wh40k-db"]

  
  def insertWh40kFaction(self, wh40kFaction: any):
      _id = self.aiaDB["wh40kFaction"].insert_one(wh40kFaction)
      return _id.inserted_id
  
  def findWH40KUnit(self, code: str, faction: str, edition: str):
      unit = self.aiaDB["wh40kUnit"].find_one(
         {"$and": [
            { "code": code },
            { "faction": faction },
            { "edition": edition }
         ]
      })
      unit_image = None
      if (unit is not None) and (unit["_id"] is not None):
        unit_image = self.aiaDB["wh40kUnitImages"].find_one(
            {"$and": [
                { "unit_id": unit["_id"] }
            ]
        })
      return unit, unit_image

  def insertUnitImage(self, unitImage: any):
      _id = self.aiaDB["wh40kUnitImages"].insert_one(unitImage)
      return _id.inserted_id

  def insertWh40kUnit(self, wh40kUnit: any):
      _id = self.aiaDB["wh40kUnit"].insert_one(wh40kUnit)
      return _id.inserted_id

  def findWh40kFaction(self, faction: str, edition: str):
      _id = self.aiaDB["wh40kFaction"].find_one(
         {"$and": [
            { "faction": faction },
            { "edition": edition }
         ]
      })
      return _id