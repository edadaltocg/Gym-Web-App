import gym
import json
import datetime
from bson.objectid import ObjectId
from bson.json_util import dumps
from flask import jsonify, request
from flask import Flask, Blueprint, render_template, Response
from flask_pymongo import PyMongo
from database.db import mongo
import appmodules.gym_manager as gm
import numpy as np
import cv2
from PIL import Image
from database.models import JSONEncoder

# Blueprint
functions_blueprint = Blueprint('database/functions', __name__, template_folder='templates')

GAME_ENTRY_TEMPLATE = {
        "game_id": "$#ID#$",
        "name": "$#TITLE#$",
        "timestamp": "$#TIMESTAMP#$",
        "image": "$#BACKGROUNDIMAGE#$",
        "gif": "$#BACKGROUNDGIF#$",
        "agents": ["$#AVAILABLEAGENTS#$"],
    }

@functions_blueprint.route('/create_game_db_entry')
def create_game_db_entry():
    games = gm.Games()
    pack = games.dict_names()
    collection = mongo.db.games
    print('BEGIN')
    for key in pack:
        game_type = games.get_games_from_key(key)[0]

        game = gm.Game(game_type)
        flag, encodedImage = game.get_static_image()
        encodedImage = encodedImage.reshape(-1).tolist()
        collection.insert({
            "game_id": key,
            "name": pack[key].title(),
            "timestamp": datetime.datetime.now(),
            "image": encodedImage,
        })
    print('END')
    return 'Done creating game entries'

@functions_blueprint.route('/update_game_db_entry')
def update_game_db_entry():
    games = gm.Games()
    pack = games.dict_names()

    print('BEGIN')
    for key in pack:
        game_type = games.get_games_from_key(key)[0]

        game = gm.Game(game_type)
        flag, encodedImage = game.get_static_image()
        encodedImage = encodedImage.reshape(-1).tolist()
        mongo.db.games.update_one(
            {"game_id": key},
            {'$set':{
                "name": pack[key].title(),
                "timestamp": datetime.datetime.now(),
                "image": encodedImage,
            }
        })
    print('END')
    return 'Done updating game entries'

@functions_blueprint.route('/delete_game_db_entry')
def delete_game_db_entry():
    games = gm.Games()
    pack = games.dict_names()

    print('BEGIN')
    for key in pack:
        game_type = games.get_games_from_key(key)[0]

        game = gm.Game(game_type)
        flag, encodedImage = game.get_static_image()
        encodedImage = encodedImage.reshape(-1).tolist()
        mongo.db.games.delete_one(
            {"game_id": key})
    print('END')
    return 'Done updating game entries'

@functions_blueprint.route('/game_poster/<game_id>')
def game_poster(game_id):
    collection = mongo.db.games
    document = collection.find_one({"game_id": game_id})
    image = document["image"]

    decodedImage = np.array(image, dtype=np.uint8).reshape(-1,1)

    return Response(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                   bytearray(decodedImage) + b'\r\n',\
                    mimetype="multipart/x-mixed-replace; boundary=frame")

def update_game_db_agents():
    pass

def update_game_db_gif():
    pass

def save_game_posters_local():
    games = gm.Games()
    pack = games.dict_names()
    print('BEGIN')
    for key in pack:
        game_type = games.get_games_from_key(key)[0]
        game = gm.Game(game_type)
        frame = game.show_frame()

        filename = str(key)+".jpg"

        cv2.imwrite(\
            'C:/Users/user/Desktop/GitHub/Gym-Web-App/static/images/'+filename,\
            frame)
    print('END')
    return 'Done saving images'


