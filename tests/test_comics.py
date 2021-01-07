import pytest

from flask import abort
from xkcd import xkcd
from xkcd import create_app


@pytest.fixture(scope="module", name="testing_client")
def fixture_testing_client():
    app = create_app()
    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client  # this is where the testing happens!


EXPECTED_COMIC_META = {
    1: {
        "date": "06-01-01",
        "description": "[[A boy sits in a barrel which is floating in an ocean.]]\nBoy: I wonder where I'll float next?\n[[The barrel drifts into the distance. Nothing else can be seen.]]\n{{Alt: Don't we all.}}",
        "id": 1,
        "title": "barrel - part 1",
        "url": "https://imgs.xkcd.com/comics/barrel_cropped_(1).jpg",
    },
    "multiple": [
        {
            "date": "06-01-01",
            "description": "[[A boy sits in a barrel which is floating in an ocean.]]\nBoy: I wonder where I'll float next?\n[[The barrel drifts into the distance. Nothing else can be seen.]]\n{{Alt: Don't we all.}}",
            "id": 1,
            "title": "barrel - part 1",
            "url": "https://imgs.xkcd.com/comics/barrel_cropped_(1).jpg",
        },
        {
            "date": "06-01-01",
            "description": "[[A sketch of a landscape with sun on the horizon]]\n{{Alt: There's a river flowing through the ocean}}",
            "id": 4,
            "title": "landscape (sketch)",
            "url": "https://imgs.xkcd.com/comics/landscape_cropped_(1).jpg",
        },
        {
            "date": "09-07-24",
            "description": "[[A man with a beret and a woman are standing on a boardwalk, leaning on a handrail.]]\nMan: A woodpecker!\n<<Pop pop pop>>\nWoman: Yup.\n\n[[The woodpecker is banging its head against a tree.]]\nWoman: He hatched about this time last year.\n<<Pop pop pop pop>>\n\n[[The woman walks away.  The man is still standing at the handrail.]]\n\nMan: ... woodpecker?\nMan: It's your birthday!\n\nMan: Did you know?\n\nMan: Did... did nobody tell you?\n\n[[The man stands, looking.]]\n\n[[The man walks away.]]\n\n[[There is a tree.]]\n\n[[The man approaches the tree with a present in a box, tied up with ribbon.]]\n\n[[The man sets the present down at the base of the tree and looks up.]]\n\n[[The man walks away.]]\n\n[[The present is sitting at the bottom of the tree.]]\n\n[[The woodpecker looks down at the present.]]\n\n[[The woodpecker sits on the present.]]\n\n[[The woodpecker pulls on the ribbon tying the present closed.]]\n\n((full width panel))\n[[The woodpecker is flying, with an electric drill dangling from its feet, held by the cord.]]\n\n{{Title text: If you don't have an extension cord I can get that too.  Because we're friends!  Right?}}",
            "id": 614,
            "title": "woodpecker",
            "url": "https://imgs.xkcd.com/comics/woodpecker.png",
        },
    ],
}
FULL_COMIC_META = {
    "http://xkcd.com/1/info.0.json": {
        "month": "1",
        "num": 1,
        "link": "",
        "year": "2006",
        "news": "",
        "safe_title": "Barrel - Part 1",
        "transcript": "[[A boy sits in a barrel which is floating in an ocean.]]\nBoy: I wonder where I'll float next?\n[[The barrel drifts into the distance. Nothing else can be seen.]]\n{{Alt: Don't we all.}}",
        "alt": "Don't we all.",
        "img": "https://imgs.xkcd.com/comics/barrel_cropped_(1).jpg",
        "title": "Barrel - Part 1",
        "day": "1",
    },
    "http://xkcd.com/4/info.0.json": {
        "month": "1",
        "num": 4,
        "link": "",
        "year": "2006",
        "news": "",
        "safe_title": "Landscape (sketch)",
        "transcript": "[[A sketch of a landscape with sun on the horizon]]\n{{Alt: There's a river flowing through the ocean}}",
        "alt": "There's a river flowing through the ocean",
        "img": "https://imgs.xkcd.com/comics/landscape_cropped_(1).jpg",
        "title": "Landscape (sketch)",
        "day": "1",
    },
    "http://xkcd.com/614/info.0.json": {
        "month": "7",
        "num": 614,
        "link": "",
        "year": "2009",
        "news": "",
        "safe_title": "Woodpecker",
        "transcript": "[[A man with a beret and a woman are standing on a boardwalk, leaning on a handrail.]]\nMan: A woodpecker!\n<<Pop pop pop>>\nWoman: Yup.\n\n[[The woodpecker is banging its head against a tree.]]\nWoman: He hatched about this time last year.\n<<Pop pop pop pop>>\n\n[[The woman walks away.  The man is still standing at the handrail.]]\n\nMan: ... woodpecker?\nMan: It's your birthday!\n\nMan: Did you know?\n\nMan: Did... did nobody tell you?\n\n[[The man stands, looking.]]\n\n[[The man walks away.]]\n\n[[There is a tree.]]\n\n[[The man approaches the tree with a present in a box, tied up with ribbon.]]\n\n[[The man sets the present down at the base of the tree and looks up.]]\n\n[[The man walks away.]]\n\n[[The present is sitting at the bottom of the tree.]]\n\n[[The woodpecker looks down at the present.]]\n\n[[The woodpecker sits on the present.]]\n\n[[The woodpecker pulls on the ribbon tying the present closed.]]\n\n((full width panel))\n[[The woodpecker is flying, with an electric drill dangling from its feet, held by the cord.]]\n\n{{Title text: If you don't have an extension cord I can get that too.  Because we're friends!  Right?}}",
        "alt": "If you don't have an extension cord I can get that too.  Because we're friends!  Right?",
        "img": "https://imgs.xkcd.com/comics/woodpecker.png",
        "title": "Woodpecker",
        "day": "24",
    },
    "http://xkcd.com/info.0.json": {
        "month": "1",
        "num": 1,
        "link": "",
        "year": "2006",
        "news": "",
        "safe_title": "Barrel - Part 1",
        "transcript": "[[A boy sits in a barrel which is floating in an ocean.]]\nBoy: I wonder where I'll float next?\n[[The barrel drifts into the distance. Nothing else can be seen.]]\n{{Alt: Don't we all.}}",
        "alt": "Don't we all.",
        "img": "https://imgs.xkcd.com/comics/barrel_cropped_(1).jpg",
        "title": "Barrel - Part 1",
        "day": "1",
    },
}


def mock_get_comic_meta(c_id):
    return FULL_COMIC_META.get(c_id)


def test_single_comic_url_creation():
    """ Should create proper URL based on comic_id"""
    comic_id = 1
    assert (
        xkcd.create_url_from_id(comic_id) == f"http://xkcd.com/{comic_id}/info.0.json"
    )


def test_malformed_url(testing_client):
    """ Should return Error 400 in case of malformed URL """
    response = testing_client.get("/comics/blah")
    assert response.status_code == 400


def test_nonexistant_url(testing_client):
    """ Should return Error 404 when resource doesn't exist """
    response = testing_client.get("/")
    assert response.status_code == 404


def test_one_id_invalid(testing_client):
    """ Should return Error 400 when one of the ids is not a number """
    response = testing_client.get("/comics/many?comic_ids=a&comic_ids=22&comic_ids=4")
    assert response.status_code == 400


# Needs mocking
def test_nonexistant_comic(testing_client, monkeypatch):
    """ Should return Error  when comic doesn't exist """
    monkeypatch.setattr(xkcd, "get_comic_meta", lambda _: abort(404))
    response = testing_client.get("/comics/0")
    assert response.status_code == 404


def test_getting_single_comic_data(testing_client, monkeypatch):
    """Should return single comic metadata given the comic_id
     {
       "id": <comic id>,
       "description": <description of the comic>,
       "date": <date of the comic publishment, in form: YY-MM-DD>,
       "title": <lowercase title of the comic>,
       "url": <url address of the image>
    }
    """
    c_id = 1
    monkeypatch.setattr(xkcd, "get_comic_meta", mock_get_comic_meta)
    response = testing_client.get(f"/comics/{c_id}")
    assert EXPECTED_COMIC_META.get(c_id) == response.get_json()


def test_getting_multiple_comics_data(testing_client, monkeypatch):
    """ Should return sorted list of comic metadata given multiple ids """
    monkeypatch.setattr(xkcd, "get_comic_meta", mock_get_comic_meta)
    response = testing_client.get("/comics/many?comic_ids=1&comic_ids=614&comic_ids=4")
    assert EXPECTED_COMIC_META.get("multiple") == response.get_json()


def test_current_comic(testing_client, monkeypatch):
    """ Should return comic data with recent comic id """
    monkeypatch.setattr(xkcd, "get_comic_meta", mock_get_comic_meta)
    response = testing_client.get("/comics/current")
    assert response.get_json()["id"] == 1
