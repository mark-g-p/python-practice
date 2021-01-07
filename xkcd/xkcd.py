import urllib.request
import json
from datetime import datetime
from flask import Blueprint, request, jsonify, abort

bp = Blueprint("xkcd", __name__)


@bp.route("/comics/current", methods=["GET"])
def current_comic():
    current_comic_url = "http://xkcd.com/info.0.json"
    return comic_by_url(current_comic_url)


@bp.route("/comics/<int:comic_id>", methods=["GET"])
def comic_by_id(comic_id):
    return comic_by_url(create_url_from_id(comic_id))


@bp.route("/comics/many", methods=["GET"])
def many_comics():
    # we are assuming we don't want repetition and comics are sorted from smallest to largest id
    comics_ids = set(request.args.to_dict(flat=False).get("comic_ids"))
    if all(id.isdigit() for id in comics_ids):
        comics_ids = sorted(map(int, comics_ids))
        return jsonify(
            [comic_by_url(create_url_from_id(comic_id)) for comic_id in comics_ids]
        )
    else:
        abort(400)


@bp.route("/comics/<string:_>")
def wrong_url(_):
    abort(400)


def create_url_from_id(comic_id):
    return f"http://xkcd.com/{comic_id}/info.0.json"


def comic_by_url(comic_url):
    data = get_comic_meta(comic_url)
    release_date = datetime.strptime(
        data["year"] + data["month"] + data["day"], "%Y%m%d"
    )
    meta = {
        "id": data["num"],
        "description": data["transcript"],
        "date": release_date.strftime("%y-%m-%d"),
        "title": data["title"].lower(),
        "url": data["img"],
    }
    return meta


def get_comic_meta(comic_url):
    try:
        with urllib.request.urlopen(comic_url) as url:
            return json.loads(url.read().decode())
    except urllib.error.HTTPError as error:
        abort(error.code)
