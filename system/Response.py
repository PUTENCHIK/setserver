from system.Exception import Exception

class Response:
    def __init__(self, success:bool=True, exception:Exception=None):
        self.success = success
        self.exception = exception

    def to_json(self):
        return {"success": self.success, "exception": None if self.exception is None else self.exception.to_json()}

    @staticmethod
    def register(token:str, nickname:str):
        return {"accessToken": token, "nickname": nickname}

    @staticmethod
    def game(id:int):
        return Response().to_json() | {"gameId": id}

    @staticmethod
    def list_of_games(arr:list):
        return {"games": arr}

    @staticmethod
    def list_of_users(arr:list):
        return {"users:": arr}

    @staticmethod
    def found_set(arr:list):
        return {"cards": arr}

    @staticmethod
    def field(cards:list, status:str, score:int):
        return {"cards": cards, "status": status, "score": score}

    @staticmethod
    def pick_set(isSet:bool, score:int):
        return {"isSet": isSet, "score":score}

    @staticmethod
    def room_score(users:list):
        return Response().to_json() | {"users": users}

    @staticmethod
    def leave_room():
        return Response().to_json()

    @staticmethod
    def exception(exception:Exception):
        return Response(False, exception).to_json()

    @staticmethod
    def key_error(error):
        ans = Response(False, Exception("No need option in request.")).to_json()
        ans["exception"]["need_option"] = error.args
        return ans