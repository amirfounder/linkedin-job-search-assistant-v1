from flask import Flask
from flask_cors import CORS


class Server:
    def __init__(self):
        self.app = Flask(__name__)
        self.port = 8080
        CORS(self.app)

    def run(self):
        self.app.run(port=self.port)

    def