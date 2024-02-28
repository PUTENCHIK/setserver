class Exception(BaseException):
    def __init__(self, message:str):
        self.message = message

    def __str__(self):
        return str(self.to_json())

    def to_json(self):
        return {"message": self.message}