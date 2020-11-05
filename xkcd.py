from flask import Flask, request, jsonify
import urllib.request, json
from datetime import datetime

app = Flask(__name__)

@app.route('/comics/current', methods=['GET'])
def current_comic():
    current_comic_url = "http://xkcd.com/info.0.json"
    return comic_by_url(current_comic_url)


@app.route('/comics/<int:comic_id>', methods=['GET'])
def comic_by_id(comic_id):
    return comic_by_url(create_url_from_id(comic_id)), 200

 
@app.route('/comics/many', methods=['GET'])
def many_comics():
    # we are assuming we don't want repetition and don't care about order of comics
    comics_ids = set(request.args.to_dict(flat=False).get("comic_ids"))
    return jsonify( [comic_by_url(create_url_from_id(comic_id)) for comic_id in comics_ids] )
       

def create_url_from_id(comic_id):
    return f"http://xkcd.com/{comic_id}/info.0.json"


def comic_by_url(comic_url):
    with urllib.request.urlopen(comic_url) as url:
        data = json.loads(url.read().decode())
        release_date = datetime.strptime(data['year']+data['month']+data['day'], "%Y%m%d")        
        
        meta = {
            "id": data['num'],
            "description": data['transcript'],
            "date": release_date.strftime('%y-%m-%d'),
            "title": data['title'].lower(),
            "url": data['img'],
            }
        return meta

