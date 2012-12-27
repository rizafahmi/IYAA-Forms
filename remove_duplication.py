import pymongo
conn = pymongo.Connection(host="mongo.iyaa.com", port=5858)
db = conn.iyaa

for data in db['musicbank_early'].find():
    if db['musicbank_early'].find({'email': data['email']}).count() > 1:
        db['musicbank_early'].remove({'email': data['email']})
