import pymongo
from pymongo import MongoClient
import datetime
from bson.objectid import ObjectId
from bson.json_util import  dumps
import json
from datetime import datetime
#from PIL import Image
import os
import io

client = MongoClient('mongodb+srv://author:lbvjy0305@cluster0.0dm4c.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
data = client['dancing']
articles = data['articles']
landings = data['landings']
users = data['users']
comments = data['comments']
playlists = data['playlists']
track = data['track']
festivals = data['festivals']
storyteller = data['storyteller']


class Article(object):

    def __init__(self):
        self.collection = articles

    def create(self, title, img, text):
        r = self.collection.insert_one({"title": title, "preview_photo": img, "preview_text": text, "post_id": len(self.listen())+1, "create_date": datetime.now()})
        return r.inserted_id
    
    def listen(self):
        return json.loads(dumps(self.collection.find()))
    
    def find_one_post(self, post_id):
        return json.loads(dumps(self.collection.find_one({"post_id": int(post_id)})))

class Landing(object):

    def __init__(self):
        self.collection = landings

    def create(self, article_id, text, image):
        self.collection.insert_one({"article_id": article_id, "text": text, "image": image})

    def get_post(self, article_id):
        return json.loads(dumps(self.collection.find({"article_id": ObjectId(article_id)})))


class User(object):

    def __init__(self):
            self.collection = users
    
    def create(self, username, password, email):
        return self.collection.insert_one({"account_id": len(self.listen())+1, "username": username, "password": password, "email": email, "email_check": False, "creation_date": datetime.now()})

    def listen(self):
        return json.loads(dumps(self.collection.find()))
    
    def find_one_user(self, username):
        return json.loads(dumps(self.collection.find_one({"username": username})))
    
    def find_one_user_by_id(self, id):
        return self.collection.find_one({'_id': ObjectId(id)})


class Comments(object):
    def __init__(self):
        self.collection = comments

    def find_all_by_article(self, id):
        return json.loads(dumps(self.collection.find_one({'_id': ObjectId(id)})))

class Playlist(object):

    def __init__(self):
        self.collection = playlists

    def create(self, title, img, img_url, text):
        r = self.collection.insert_one({"title": title, 
        "preview_photo": img, "preview_text": text, "img_url":img_url,
         "playlist_id": len(self.listen())+1, "create_date": datetime.now()})
        return r.inserted_id
    
    def listen(self):
        return json.loads(dumps(self.collection.find()))

    def find_one_playlist(self, playlist_id):
        return json.loads(dumps(self.collection.find_one({"playlist_id": int(playlist_id)})))

class Track(object):

    def __init__(self):
        self.collection = track

    def create(self, playlist_id, soundcloud_track):
        self.collection.insert_one({"playlist_id": playlist_id, "soundcloud_track":soundcloud_track})

    def listen(self):
        return json.loads(dumps(self.collection.find()))

    def get_track(self, playlist_id):
        return json.loads(dumps(self.collection.find({"playlist_id": ObjectId(playlist_id)})))


class Festival(object):
    def __init__(self):
        self.collection = festivals

    def create(self, title, preview_photo, description, img_url,
     start_date, address, place, lan, lat, lineup, status):
        r = self.collection.insert_one({
            "festival_id": len(self.listen())+1,
            "title": title,
            "preview_photo": preview_photo,
            "description":  description,
            "img_url": img_url,
            "start_date":  datetime.strptime(start_date, "%d-%M-%Y"),
            "address": address,
            "place": place,
            "lan": lan,
            "lat": lat,
            "lineup": lineup,
            "status": status

        })

        return r.inserted_id

    def listen(self):
        return json.loads(dumps(self.collection.find()))

    def find_one_festival(self, festival_id):
        return json.loads(dumps(self.collection.find_one({"festival_id": int(festival_id)})))

class Storyteller(object):

    def __init__(self):
        self.collection = storyteller

    def create(self, festival_id, text, image):
        self.collection.insert_one({"festival_id": festival_id, "text": text, "image": image})

    def get_storyteller(self, festival_id):
        return json.loads(dumps(self.collection.find({"festival_id": ObjectId(festival_id)})))

    
    

# fest = Festival()

# img = Image.open(os.path.dirname(__file__)+"/festival1.jpg")
# imgByteArr = io.BytesIO()
# img.save(imgByteArr, format='JPEG')
# imgByteArr = imgByteArr.getvalue()

# fest_id = fest.create(
#     'Ultra Music Festival 2022. Каким он получился',
#     imgByteArr,
#     "Наконец-то дошли руки, чтобы расказать вам о недавно \
#     прошедшом ежегодном фестивале электронной музыки. Он получился как всегда жарким. \
#     Подготовили небольшое резюме. Скорее читайте",
#     'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ4_Uvc4V6FDQ6l1T5kj7mPcdHJeKRayGfnyg&usqp=CAU',
#     "25-03-2022",
#     "Майами, Флорида, США",
#     "FPL Solar Amphitheater at Bayfront Park",
#     25.775505,
#     -80.186281,
#     ["David Guetta", "Armin Van Buuren", "Krewella", "Oliver Tree"],
#     False
# )

# storyteller = Storyteller()

# img = Image.open(os.path.dirname(__file__)+"/storyteller.jpeg")
# imgByteArr = io.BytesIO()
# img.save(imgByteArr, format='JPEG')
# imgByteArr = imgByteArr.getvalue()
# storyteller.create(fest_id, 'Вот таким получился фестиваль.', imgByteArr)

# img = Image.open(os.path.dirname(__file__)+"/storyteller1.jpeg")
# imgByteArr = io.BytesIO()
# img.save(imgByteArr, format='JPEG')
# imgByteArr = imgByteArr.getvalue()
# storyteller.create(fest_id, None, imgByteArr)

# img = Image.open(os.path.dirname(__file__)+"/storyteller2.jpg")
# imgByteArr = io.BytesIO()
# img.save(imgByteArr, format='JPEG')
# imgByteArr = imgByteArr.getvalue()
# storyteller.create(fest_id, None, imgByteArr)

# img = Image.open(os.path.dirname(__file__)+"/storyteller3.jpg")
# imgByteArr = io.BytesIO()
# img.save(imgByteArr, format='JPEG')
# imgByteArr = imgByteArr.getvalue()
# storyteller.create(fest_id, None, imgByteArr)
    

#1261618552

#787656487

#1167142630

    
# p = Playlist()
# img = Image.open(os.path.dirname(__file__)+"/playlist1.jpeg")
# title = 'Первый плейлист'
# text = 'Послушайте первый плейлист'

# imgByteArr = io.BytesIO()
# img.save(imgByteArr, format='JPEG')
# imgByteArr = imgByteArr.getvalue()


# play = p.create(title, imgByteArr, '', text)


# t = Track()
# t.create(ObjectId(play), 1261618552)

# t.create(ObjectId(play), 787656487)

# t.create(ObjectId(play), 1167142630)


#s = User()
#c = s.create("nikkiharmon", 'lbvjy0305')
#print(s.find_one_user_by_id('61ec57645b02b3906265be5b'))
#a = Article()
#img = Image.open(os.path.dirname(__file__)+"/art12.jpeg")
#imgByteArr = io.BytesIO()
#img.save(imgByteArr, format='JPEG')
#imgByteArr = imgByteArr.getvalue()
#a.create('Alle Farben - Out of Space', imgByteArr)
#print(a.listen())
#r = a.find_one_post(4)
#b = Landing()


#img = Image.open(os.path.dirname(__file__)+"/art12.jpeg")
#imgByteArr = io.BytesIO()
#img.save(imgByteArr, format='JPEG')
#imgByteArr = imgByteArr.getvalue()
#b.create(ObjectId(r['_id']['$oid']), None, imgByteArr)
#print(ObjectId(r))
#print(os.path.dirname(__file__)+"/test.jpg")