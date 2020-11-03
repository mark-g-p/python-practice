from flask import Flask
app = Flask(__name__)

@app.route('/comics/current')
def current_comic():
    pass

@app.route('/comics/<int:comic_id>')
def comic_by_id():
    pass 

