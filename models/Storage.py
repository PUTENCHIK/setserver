# from werkzeug.security import generate_password_hash, check_password_hash
from system.Exception import Exception
from models.User import User
from models.Game import Game

class Storage:
    def __init__(self):
        self.games = []
        self.users = []

    def get_nicknames(self):
        return [user.nickname for user in self.users]

    def get_user(self, id:int = None, nickname:str = None, token:str = None):
        for user in self.users:
            if user.id == id or user.nickname == nickname or user.token == token:
                return user
        text_ex = "No user with "
        if id is not None:
            text_ex += f"id={id}."
        elif nickname is not None:
            text_ex += f"nickname '{nickname}'."
        else:
            text_ex += f"token '{token}'."
        raise Exception(text_ex)

    def get_game(self, id:int = None, token:str = None):
        user = self.get_user(token=token) if token is not None else None
        for game in self.games:
            if game.id == id or user is not None and game.is_user_in_game(user):
                return game
        if id is not None:
            raise Exception(f"No game with id={id}")
        else:
            raise Exception(f"User with token='{token}' isn't in any game.")

    # список игр, в которых находился игрок с переданным токеном
    def get_games(self, token:str):
        user = self.get_user(token=token)
        json = [game.to_json() for game in self.games if game.is_user_in_game(user)]
        return [{"id": game["id"], "users": game["users"]} for game in json]

    # список зарегестрированных аккаунтов
    def get_users(self):
        return [user.to_json() for user in self.users]

    # найти в комнате игрока сет карт (если такой есть)
    def find_set(self, token:str):
        user = self.get_user(token=token)
        game = self.get_game(token=token)
        return game.find_set()

    # находится ли переданный игрок в какой либо комнате
    def is_user_in_game(self, user:User):
        for game in self.games:
            if game.is_user_in_game(user):
                return game.id
        return False

    # функция регистрации или входа в аккаунт по переданным логину и паролю
    def register_user(self, nickname:str, password:str):
        if not nickname or not password:
            raise Exception("Nickname or password is empty.")
        if nickname in self.get_nicknames():
            user = self.get_user(nickname=nickname)
            if not user.check_password(password):
                raise Exception(f"Password for nickname '{user.nickname}' is wrong.")
            else:
                return user
        else:
            user = User(len(self.users)+1, nickname, password)
            self.users += [user]
            return user

    # создание комнаты по токену игрока и дальнейшее его подключение к этой комнате
    def create_game(self, token:str):
        user = self.get_user(token=token)
        check_game = self.is_user_in_game(user)
        if check_game:
            raise Exception(f"User with token='{token}' already in game with id={check_game}")

        game = Game(len(self.games)+1)
        game.add_user(user)
        self.games += [game]
        return game

    # добавить игрока по токену в комнату
    def enter_game(self, token:str, id_game:int):
        user = self.get_user(token=token)
        game = self.get_game(id=id_game)
        if game.is_game_full():
            raise Exception(f"Game with id={id_game} is already full.")
        if game.is_user_in_game(user):
            raise Exception(f"User with token='{token}' already in this game with id={id_game}")
        game.add_user(user)
        return game

    # игрок покидает комнату, в которой находится
    def leave_game(self, token:str):
        user = self.get_user(token=token)
        game = self.get_game(token=token)
        game.remove_user(user)

    # карты на столе в комнате, в которой находится игрок
    def field(self, token:str):
        user = self.get_user(token=token)
        game = self.get_game(token=token)
        return game, game.users[user.id]["score"]

    # выбрать три карты по их id и проверить их на сет
    def pick_set(self, token:str, id_cards:list):
        user = self.get_user(token=token)
        game = self.get_game(token=token)
        isSet = game.pick_cards(user, id_cards)
        return isSet, game.get_user_score(user)

    # запрос игрока на добавление 3 карт на стол
    def add_cards(self, token:str):
        user = self.get_user(token=token)
        game = self.get_game(token=token)
        game.add_cards(user)

    # очки игроков в комнате токена
    def get_room_score(self, token:str):
        game = self.get_game(token=token)
        return game.get_score()
