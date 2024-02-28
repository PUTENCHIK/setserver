class Card:
    def __init__(self, id:int, color:int, shape:int, fill:int, count:int):
        self.id = id            # id from 1 to 81
        self.color = color      # 1: red, 2: green, 3: blue
        self.shape = shape      # 1: rhombus, 2: rectangle, 3: wave
        self.fill = fill        # 1: empty, 2: striped, 3: filled
        self.count = count

    def __str__(self):
        return str(self.to_json())

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def to_json(self):
        return { "id": self.id, "color": self.color, "shape": self.shape, "fill": self.fill, "count": self.count, }