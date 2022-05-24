from fastapi import FastAPI, Response, status
from pymongo import MongoClient
import os

app = FastAPI()

def get_bucket():
    USER = os.getenv('MONGO_USER')
    PASSWORD = os.getenv('MONGO_PASSWORD')
    MONGO_URL = 'mongodb://{}:{}@192.168.1.21:27017'.format(USER,PASSWORD)
    client = MongoClient(MONGO_URL)
    db = client.quran_fr
    return db

@app.get("/", tags=["Root"])
async def root():
    return {"message" : "Welcome to QuranAPI"}

@app.get("/surah/", tags=["Quran"], status_code=200)
async def retrieve_surah(id : int):
    db = get_bucket()
    document = db.summary.find_one({'number' : id})
    collection_name = document['translation']
    surah = db.get_collection(collection_name).find({})
    json = []
    for result in surah:
        json.append({'aya_number' : result['aya_number'], 'verse' : result['translation']})
    return json
    
@app.get("/surah/verse/", tags=["Quran"], status_code=200)
async def retrieve_surah_verse(id : int, number : int, response: Response):
    db = get_bucket()
    document = db.summary.find_one({'number' : id})
    collection_name = document['translation']
    surah = db.get_collection(collection_name).find({})
    json = []
    for result in surah:
        if result['aya_number'] == number:
            answer = {'aya_number' : result['aya_number'], 'verse' : result['translation']}
    if answer == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        answer = "This verse does not exist"

    return answer
        
    