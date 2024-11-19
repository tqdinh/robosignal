import ssl
from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit, join_room
import json

app = Flask(__name__)
app.secret_key = "random secret key!"
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on("join")
def join(message):
    username = message["username"]
    room = message["room"]
    join_room(room)
    print("RoomEvent: {} has joined the room {}\n".format(username, room))
    emit("ready", {username: username}, to=room, skip_sid=request.sid)


@socketio.on("data")
def transfer_data(message):
    username = message["username"]
    room = message["room"]
    data = message["data"]
    print("DataEvent: {} has sent the data:\n {}\n".format(username, data))
    emit("data", data, to=room, skip_sid=request.sid)


@socketio.on_error_default
def default_error_handler(e):
    print("Error: {}".format(e))
    socketio.stop()


@app.route("/")
def index():
    return render_template("index.html")


def startapp():
    pass
    # ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # ssl_context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
    # socketio.run(
    #     app,
    #     host="0.0.0.0",
    #     port=5006,
    #     #    ssl_context=ssl_context,
    # )


if __name__ == "__main__":
    startapp()
    pass

    # startapp()
    # socketio.run(
    #     app,
    #     host="0.0.0.0",
    #     port=5006,
    #     #    ssl_context=ssl_context,
    # )