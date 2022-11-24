from socketIOApp import app
from socketIOApp import socketIO

if __name__ == "__main__":
    socketIO.run(app, debug=True)
