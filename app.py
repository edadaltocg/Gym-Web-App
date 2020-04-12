'''
    The entry & exit point to our application
'''
from flask import Flask, render_template, Response  # import flask
from database.db import MONGO_URI
from database.db import mongo
from database.models import models_blueprint
import appmodules.gym_manager as gm
from appmodules.webstreaming import generate

app = Flask(__name__)  # create an app instance
app.register_blueprint(models_blueprint)
'''
    Configurations
'''
app.config['MONGO_URI'] = MONGO_URI
mongo.init_app(app)
'''
    Routes
'''
@app.route("/")  # at the end point /
def home():  # call method hello
    games = gm.Games()
    pack = games.dict_names()

    return render_template("index.html", title="Cards", cards=pack)

@app.route("/games/<game_id>")
def game_view(game_id):
    games = gm.Games()
    list_of_game_types = games.get_games_from_key(game_id)
    # TODO: Get descriptions
    # TODO: JSON OBJECT WITH NAME AND DESCRIPTIONS
    json_object = list_of_game_types
    return render_template("game_menu.html", title=game_id.title(), game_id=game_id, games=json_object)

#TODO: choose agent page route
@app.route("/games/<game_id>/<game_type>")
def choose_agent_for_game(game_id, game_type):
    return "Agents"

@app.route("/games/<game_id>/<game_type>/<agent_id>")
def play_game_page(game_id, game_type, agent_id):
    return render_template("game.html", title=game_type, \
                           game_type=game_type, agent_id=agent_id)

# TEST
@app.route("/gamefeed/<game_type>/<agent_id>")
def game_feed(game_type, agent_id):
    # return the response generated along with the specific media
    # type (mime type)
    game = gm.Game(game_type, agent_id)
    return Response(game.play(),\
                    mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/about")  # at the end point /
def about():  # call method hello
    return render_template("about.html")  # which returns "hello world"

@app.route("/cards")
def cards():
    Cards = {
        [
            {
               "title": "title1"
            },
            {
                "title": "title2"
            }
        ]
    }
    return render_template("cards.html", title="Cards", cards=Cards)

@app.route("/db")
def show_db():
    mongo.db.agents.find({})
    return render_template()

# @app.route("/<name>")  # at the end point /<name>
# def hello_name(name):  # call method hello_name
#     return "Hello " + name  # which returns "hello + name


'''
    Run app
'''
if __name__ == "__main__":  # on running python app.py
    app.run(debug=True)  # run the flask app -
    # every modification will restart the server

# launch app:
# flask run
# activate virtual env:
# virtual\Scripts\activate
# list requirements:
# pip freeze > requirements.txt
# install from requirements:
# pip install -r virtual/requirements.txt