from flask import Flask, request, jsonify
import urllib.request, json
from datetime import datetime

app = Flask(__name__)

@app.route('/comics/current')
def current_comic():
    with urllib.request.urlopen("http://xkcd.com/info.0.json") as url:
        data = json.loads(url.read().decode())
        release_date = datetime.strptime(data['year']+data['month']+data['day'], "%Y%m%d")        
        meta = {
            "id": data['num'],
            "description": data['transcript'],
            "date": release_date.strftime('%y-%m-%d'),
            "title": data['title'].lower(),
            "url": data['img'],
            }
        return meta, 200
 

@app.route('/comics/<int:comic_id>')
def get_comic_by_id(comic_id):
    return comic_by_id(comic_id), 200

 
@app.route('/comics/many/')
def query_com():
    all_comics = []
    for comic_id in request.args.to_dict(flat=False).get("comic_ids"):
        all_comics.append(comic_by_id(comic_id))
    return jsonify(all_comics)
       
def comic_by_id(comic_id):
    with urllib.request.urlopen(f"http://xkcd.com/{comic_id}/info.0.json") as url:
        data = json.loads(url.read().decode())
        release_date = datetime.strptime(data['year']+data['month']+data['day'], "%Y%m%d")        
        meta = {
            "id": data['num'],
            "description": data['transcript'],
            "date": release_date.strftime('%y-%m-%d'),
            "title": data['title'].lower(),
            "url": data['img'],
            }
        return (meta)