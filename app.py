from flask import Flask
from models.Storage import Storage
from system.Exception import Exception
from system.Response import Response
from system.Request import Request

app = Flask(__name__)
storage = Storage()

@app.get('/')
def main():
    text = "Welcome to start/test page of setserver - server of board game created by Olifirenko Maxim, 14221-ДБ."
    return f"<h1>{text}</h1>"

@app.post('/user/register')
def user_register():
    req = Request.get_flask_request()
    try:
        user = storage.register_user(req.options["nickname"].lower(), req.options["password"])
        return Response.register(user.token, user.nickname)
    except Exception as ex:
        return Response.exception(ex)
    except KeyError as er:
        return Response.key_error(er)

@app.post('/set/room/create')
def create_game():
    req = Request.get_flask_request()
    try:
        game = storage.create_game(req.options["accessToken"])
        return Response.game(game.id)
    except Exception as ex:
        return Response.exception(ex)
    except KeyError as er:
        return Response.key_error(er)

@app.post("/set/room/list")
def list_of_games():
    req = Request.get_flask_request()
    try:
        arr = storage.get_games(req.options["accessToken"])
        return Response.list_of_games(arr)
    except Exception as ex:
        return Response.exception(ex)
    except KeyError as er:
        return Response.key_error(er)

'''
@app.get("/set/answer")
def find_set():
    req = Request.get_flask_request()
    try:
        arr_id = storage.find_set(req.options["accessToken"])
        return Response.found_set(arr_id)
    except Exception as ex:
        return Response.exception(ex)
    except KeyError as er:
        return Response.key_error(er)
'''

@app.get("/user/list")
def list_of_users():
    try:
        arr = storage.get_users()
        return Response.list_of_users(arr)
    except Exception as ex:
        return Response.exception(ex)

@app.post("/set/room/enter")
def enter_game():
    req = Request.get_flask_request()
    try:
        game = storage.enter_game(req.options["accessToken"], req.options["gameId"])
        return Response.game(game.id)
    except Exception as ex:
        return Response.exception(ex)
    except KeyError as er:
        return Response.key_error(er)

@app.post("/set/field")
def field():
    req = Request.get_flask_request()
    try:
        game, score = storage.field(req.options["accessToken"])
        return Response.field(game.get_field(), game.status, score)
    except Exception as ex:
        return Response.exception(ex)
    except KeyError as er:
        return Response.key_error(er)

@app.post("/set/pick")
def pick_set():
    req = Request.get_flask_request()
    try:
        isSet, score = storage.pick_set(req.options["accessToken"], req.options["cards"])
        return Response.pick_set(isSet, score)
    except Exception as ex:
        return Response.exception(ex)
    except KeyError as er:
        return Response.key_error(er)

@app.post("/set/add")
def add_cards():
    req = Request.get_flask_request()
    try:
        storage.add_cards(req.options["accessToken"])
        return Response().to_json()
    except Exception as ex:
        return Response.exception(ex)
    except KeyError as er:
        return Response.key_error(er)

@app.post("/set/scores")
def room_score():
    req = Request.get_flask_request()
    try:
        users = storage.get_room_score(req.options["accessToken"])
        return Response.room_score(users)
    except Exception as ex:
        return Response.exception(ex)
    except KeyError as er:
        return Response.key_error(er)


@app.post("/set/room/leave")
def leave_game():
    req = Request.get_flask_request()
    try:
        storage.leave_game(req.options["accessToken"])
        return Response.leave_room()
    except Exception as ex:
        return Response.exception(ex)
    except KeyError as er:
        return Response.key_error(er)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
