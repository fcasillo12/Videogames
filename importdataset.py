from pymongo import MongoClient
import pandas as pd
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client.videogame
vg = db.vg
df = pd.read_csv("vgsales.csv")
records_ = df.to_dict(orient = 'records')
result = db.vg.insert_many(records_)
print('Record inseriti con successo!')