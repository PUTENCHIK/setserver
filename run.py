# import requests, json
# from system.Exception import Exception
#
# def register(nick, password):
#     try:
#         x = requests.post(ip + "/user/register", json={"nickname": nick, "password": password})
#         print("Register request:", x.json())
#         token = x.json()["accessToken"]
#         return token
#     except Exception as ex:
#         print(ex.to_json())
#     except KeyError as er:
#         print("Register user key error:", er.args)
#
# def create_room(token):
#     try:
#         x = requests.post(ip + "/set/room/create", json={"accessToken": token})
#         print("Create room request:", x.json())
#         return x.json()["gameId"]
#     except Exception as ex:
#         print(ex.to_json())
#     except KeyError as er:
#         print("Create room key error:", er.args)
#
# def games(token):
#     try:
#         x = requests.post(ip + "/set/room/list", json={"accessToken": token})
#         pretty = json.dumps(x.json(), indent=4)
#         print("List of games request:", pretty)
#     except Exception as ex:
#         print(ex.to_json())
#
# def users():
#     try:
#         x = requests.get(ip + "/user/list")
#         pretty = json.dumps(x.json(), indent=4)
#         print("List of users request:", pretty)
#     except Exception as ex:
#         print(ex.to_json())
#
# def enter_game(token, id):
#     try:
#         x = requests.post(ip+"/set/room/enter", json={"accessToken": token, "gameId": id})
#         print("Enter room request:", x.json())
#     except Exception as ex:
#         print(ex.to_json())
#
# def field(token):
#     try:
#         x = requests.post(ip+"/set/field", json={"accessToken": token})
#         pretty = json.dumps(x.json(), indent=4)
#         print("Field request:", pretty)
#     except Exception as ex:
#         print("Error:", ex.to_json())
#
# ip = "http://192.168.1.7:5000"
#
# # token1 = register("Danny", "123")
# # token2 = register("Maxy", "1234")
# # token3 = register("Glebby", "1234")
# # token4 = register("Vanny", "1234")
# # token5 = register("Micky", "1234")
# # users()
# # id_game = create_room(token1)
# # enter_game(token1, id_game)
# # enter_game(token2, id_game)
# # enter_game(token3, id_game)
# # enter_game(token4, id_game)
#
# # games(token1)
#
# # field(token5)