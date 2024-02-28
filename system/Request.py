from flask import request

class Request:
    def __init__(self, options:dict):
        self.options = options

    @staticmethod
    def get_flask_request():
        r = request.get_json()
        # print("Request Class:", r)
        return Request(r)