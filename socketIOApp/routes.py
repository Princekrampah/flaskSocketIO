from socketIOApp import app, socketIO
from flask import render_template, request, url_for, session, redirect
from flask_socketio import join_room, leave_room, emit


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/join", methods=["GET", "POST"])
def join():
    # check for a post method
    if (request.method == "POST"):
        print("post method")
        # get form data
        username: str = request.form["username"]
        room_name: str = request.form["roomName"]

        # store user data in session
        session["username"] = username
        session["room_name"] = room_name

        # return template(chatRoom template)
        return render_template("chatRoom.html", session=session)
    else:
        # handle logged in user page refresh
        if (session.get("username") is not None):
            return render_template("chatRoom.html", session=session)
        else:
            # user in not logged in/ does not have a session
            # need to join a room
            return redirect(url_for("index"))


# namespace is the end point where we want to socket to run on
@socketIO.on("join", namespace="/join")
def join(message):
    roomName = session.get("room_name")
    username = session.get("username")
    join_room(room=roomName)
    emit("status", {
         "msg": f"{username} has joined the chat room!!"}, room=roomName)

# handle texting of messages


@socketIO.on("text", namespace="/join")
def text(message):
    roomName = session.get("room_name")
    username = session.get("username")
    emit("message", {"msg": f"{username} : {message['msg']} "}, room=roomName)


# handle user leaving room
@socketIO.on("left", namespace="/join")
def left(message):
    roomName = session.get("room_name")
    username = session.get("username")
    leave_room(room=roomName)
    session.clear()
    emit("status", {"msg": f"{username} has Left the chat room"}, room=roomName)
