from werkzeug.security import generate_password_hash, check_password_hash
from secrets import token_hex


class UserStatus:
    ingame = "ingame"           # пользователь находится в комнате
    outgame = "outgame"         # пользователя вышел из комнаты


class User:
    def __init__(self, id:int, nickname:str, password:str):
        self.id = id
        self.nickname = nickname.lower()
        self.password = generate_password_hash(password)
        self.token = token_hex(6)

    def __str__(self):
        return str(self.to_json())

    def check_password(self, password:str):
        return check_password_hash(self.password, password)

    def to_json(self):
        return {"id": self.id, "nickname": self.nickname, "token": self.token}
