from itertools import product
from random import choice

from models.Card import Card
from system.Exception import Exception
from models.User import User, UserStatus

MAX_USERS_IN_GAME = 4


class GameStatus:
    ongoing = "ongoing"
    ended = "ended"


class Game:
    def __init__(self, id:int):
        self.id = id
        self.users = {}                             # id: {"user": User, "scores": int, "status": GameStatus}
        self.deck = self.create_deck()              # ещё незадействованные карты из колоды
        # self.deck = []
        self.field = []                             # карты на столе
        self.status = GameStatus.ongoing            # статус изначально - ongoing

        self.lay_out_cards(12)

    def __str__(self):
        return str(self.to_json())

    # проверка на нахождение игрока в комнате
    def is_user_in_game(self, user:User):
        return user.id in self.users and self.users[user.id]["status"] == UserStatus.ingame

    # заполнена ли комната (4 игрока со статусом ingame)
    def is_game_full(self):
        return sum([user["status"] == UserStatus.ingame for user in self.users.values()]) >= MAX_USERS_IN_GAME

    # получить очки игрока
    def get_user_score(self, user:User):
        return self.users[user.id]["score"]

    # список карт, лежещих на столе
    def get_field(self):
        return [card.to_json() for card in self.field]

    # прибавить к очкам игрока переданное значение
    def change_score(self, user_id:int, diff:int):
        self.users[user_id]["score"] += diff
        if self.users[user_id]["score"] < 0:
            self.users[user_id]["score"] = 0

    # добавить игрока в комнату
    def add_user(self, user:User):
        self.users[user.id] = {"user": user, "score": 0, "status": UserStatus.ingame}

    # поставить переданному игроку статус outgame, или удалить из списка пользователей, если у него нет очков в игре
    def remove_user(self, user:User):
        if user.id not in self.users.keys() or self.users[user.id] == UserStatus.outgame:
            raise Exception(f"User with id='{user.id}' isn't in game in id='{self.id}'.")
        if self.users[user.id]["score"] != 0:
            self.users[user.id]["status"] = UserStatus.outgame
        else:
            del self.users[user.id]

    # создать все карты и добавить их в колоду
    def create_deck(self):
        count = 1
        cards = []
        for x in product("123", repeat=4):
            s = ''.join(x)
            cards += [Card(count, int(s[0]), int(s[1]), int(s[2]), int(s[3]))]
            count += 1
        return cards

    # выложить заданное кол-во карт из колоды на стол
    def lay_out_cards(self, count:int):
        if count > len(self.deck):
            raise Exception("You tried lay out too many cards.")

        for i in range(count):
            card = choice(self.deck)
            self.field += [card]
            self.deck.remove(card)

    # возвращает список id карт, которые являются сетом. Если такого нет на столе, возвращается None
    def find_set(self):
        for i in range(len(self.field)-1):
            for j in range(i+1, len(self.field)):
                properties = []
                first, second = self.field[i].to_json(), self.field[j].to_json()
                for property in ["color", "shape", "fill", "count"]:
                    properties += [first[property]
                                   if first[property] == second[property]
                                   else 6 - first[property] - second[property]]
                third = Card(int(''.join([str(p-1) for p in properties]), 3)+1, *properties)
                for card in self.field:
                    if card != self.field[i] and card != self.field[j] and card == third:
                        return [first["id"], second["id"], third.id]
        return None

    # проверка трёх карт на сет
    @staticmethod
    def is_set(cards:list):
        for property in ("count", "color", "shape", "fill"):
            values = list(set([cards[0][property], cards[1][property], cards[2][property]]))
            if len(values) == 2:
                return False
        return True

    # выбрать три карты и проверить их на сет (если сет, то карты заменяются)
    def pick_cards(self, user:User, id_cards:list):
        if len(id_cards) != 3 or len(set(id_cards)) != 3:
            raise Exception("Wrong amount of cards.")
        cards = [card for card in self.field if card.id in id_cards]
        if len(cards) != 3:
            raise Exception("Specified cards aren't on field.")
        result = Game.is_set([card.to_json() for card in cards])
        self.change_score(user.id, 3 if result else -1)
        if result:
            for card in cards:
                self.field.remove(card)
            if len(self.deck) >= 3:
                self.lay_out_cards(3)
        return result

    # выложить из колоды ещё 3 карты (если это возможно)
    def add_cards(self, user:User):
        if len(self.deck) < 3:
            raise Exception("There aren't enough cards in the deck.")
        if len(self.field) >= 21:
            raise Exception("There is no need to add cards. Set is on the field.")
        if self.find_set() is not None:
            self.change_score(user.id, -1)
        self.lay_out_cards(3)

    # массив объектов с никами и очками игроков комнаты
    def get_score(self):
        return [{"name": user_dict["user"].nickname,
                 "score": user_dict["score"]} for user_dict in self.users.values()]

    def to_json(self):
        users = {}
        for id_user in self.users:
            users[id_user] = {"user": self.users[id_user]["user"].to_json(),
                              "score": self.users[id_user]["score"],
                              "status": self.users[id_user]["status"]}
        return {
            "id": self.id,
            "users": users,
            "deck": [card.to_json() for card in self.deck],
            "field": [card.to_json() for card in self.field],
        }