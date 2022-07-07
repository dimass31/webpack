from flask import Flask, jsonify, make_response, request, render_template, send_file
from flask_cors import CORS

import base64
from bson.objectid import ObjectId
import io

from db import Article
from db import Landing
from db import User
from db import Playlist
from db import Track
from db import Festival
from db import Storyteller

from sendMail import sendmail


app = Flask(__name__)
CORS(app)

@app.route('/<num>')
def index(num):
    articles = Article()
    art_list = articles.listen()[::-1]

    # len_post = len(art_list)

    # num = int(num)*5

    # if len_post<num:
    #     art_list = art_list[len(art_list)//5*5:]
    # else:
    #     art_list = art_list[num//5-1:num]
        
    # r = jsonify({"art_list": art_list, "len_post": len_post})
    #response = make_response(r)
    #response.headers["Referrer-Policy"] = 'no-referrer'
    return jsonify({"1": art_list[0]})

@app.route('/post/<id>')
def post(id):
    article = Article()
    post = article.find_one_post(id)
    post_id = post['_id']['$oid']
    landings = Landing()
    info = landings.get_post(post_id)
    info[0]['title'] = post['title']
    info[0]['img_url'] = post['img_url']
    #print(info[0].append(1))
    #print(jsonify(info)["article_id"])
    return jsonify(info)

@app.route('/comments/<id>')
def commens(id):
    if id == 4:
        return jsonify({"user": "nikki", "text": "Хорошая статья!"})
    return None


@app.route('/playlists/paginate/<num>')
def playlists(num):
    playlist = Playlist()
    playlist_list = playlist.listen()[::-1]

    len_playlist = len(playlist_list)

    num = int(num)*5

    if len_playlist<num:
        playlist_list = playlist_list[len(playlist_list)//5*5:]
    else:
        playlist_list = playlist_list[num//5-1:num]
        
    r = jsonify({"playlist_list": playlist_list, "len_playlist": len_playlist})
    response = make_response(r)
    response.headers["Referrer-Policy"] = 'no-referrer'
    return response

@app.route('/playlists/<id>')
def playlist(id):
    playlist = Playlist()
    playlist = playlist.find_one_playlist(id)
    playlist_id = playlist['_id']['$oid']

    track = Track()
    info = track.get_track(playlist_id)

    info[0]['title'] = playlist['title']
    info[0]['img_url'] = playlist['img_url']
    return jsonify(info)

@app.route('/festivals/paginate/<num>')
def festivals(num):
    festivals = Festival()
    festivals_list = festivals.listen()[::-1]

    len_festivals = len(festivals_list)

    num = int(num)*5

    if  len_festivals<num:
        festivals_list = festivals_list[len(festivals_list)//5*5:]
    else:
        festivals_list = festivals_list[num//5-1:num]
        
    r = jsonify({"festivals_list": festivals_list, "len_festivals":  len_festivals})
    response = make_response(r)
    response.headers["Referrer-Policy"] = 'no-referrer'
    return response

@app.route('/festivals/<id>')
def festivalpost(id):
    
    festival = Festival()
    festival = festival.find_one_festival(id)
    festival_id = festival['_id']['$oid']

    storyteller = Storyteller()
    info = storyteller.get_storyteller(festival_id)

    info[0]['title'] = festival['title']
    info[0]['img_url'] = festival['img_url']
    info[0]['description'] = festival['description']
    info[0]['start_date'] = festival['start_date']
    info[0]['address'] = festival['address']
    info[0]['place'] = festival['place']
    info[0]['lan'] = festival['lan']
    info[0]['lat'] = festival['lat']
    info[0]['lineup'] = festival['lineup']
   
    return jsonify(info)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try: 
            f = request.get_json()
            username = f['username']
            password = f['password']
            s = User()
            s = s.find_one_user(username)
            if s and s['password'] == password:
                return jsonify({"status": "succes", "user": username, "token": "token"})
            return jsonify({"status": "denid"})

        except:
            return jsonify({"status": "denid"})
    return jsonify({"1": 1})

@app.route('/register', methods =['POST'])
def register():
    try:
        f = request.get_json()
        email = f['email']
        print(f)
        s = User()
        new_user = s.create(f['name'], f['password'], f['email'])
        inserted_id = new_user.inserted_id
        new_create_email = s.find_one_user_by_id(inserted_id)
        print(new_create_email)
        txt = "acount_id=" + str(new_create_email['account_id']) + "&email="+str(email)
        #print(txt + str(new_create_email['account_id']))
        sendmail(email, txt)
        return jsonify({"status": "succes"})
    except:
        return jsonify({"status": "denid"})


@app.route('/verification', methods =['POST'])
def verification():
    f = request.get_json()
    print(f)
    return jsonify({"c": "yes"})

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        print(request.form)
        img = request.files["file"]
        title = request.form['title']
        description = request.form['description']
        landing = request.form['landing'] 

        data = img.read()             
        #data = base64.b64encode(data)  
        #data = data.decode() 
        
        #imgByteArr = io.BytesIO()
        #data.save(imgByteArr, format='JPEG')
        #imgByteArr = imgByteArr.getvalue()

        article = Article()
        art = article.create(title, data, description)

        b = Landing()
        b.create(ObjectId(art), landing, data)

        data = base64.b64encode(data)  
        data = data.decode() 
        return render_template('create.html', photo=data)
    return render_template('create.html')


# @app.route('/site', methods=['POST', 'GET'])
# def site():
#     return render_template('index.html')


@app.route('/postimage/<id>')
def get_image(id):
    id = str(id)[:-4]
    filename = f'static/img/post{id}.jpg'
    return send_file(filename, mimetype='image/gif')




@app.route('/')
def hello_world():
    return 'Hello World8!'