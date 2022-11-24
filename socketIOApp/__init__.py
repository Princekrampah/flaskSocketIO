from flask import Flask
from flask_session import Session
from flask_socketio import SocketIO

app = Flask(__name__)

# secret key to maintain sessions
app.config["SECRET"] = ""
app.config["SESSION_TYPE"] = "filesystem"

Session(app)
# manage_session is false so flask session is used
# not the one of socketIO
socketIO = SocketIO(app, manage_session=False)


from socketIOApp import routes