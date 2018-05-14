# import gevent
#
# def foo():
#     print('Running in foo')
#     gevent.sleep(0)
#     print('Explicit context switch to foo again')
#
# def bar():
#     print('Explicit context to bar')
#     gevent.sleep(0)
#     print('Implicit context switch back to bar')
#
# gevent.joinall([
#     gevent.spawn(foo),
#     gevent.spawn(bar),
# ])

# import gevent
# from gevent.queue import Queue
# from gevent import Greenlet
# class Actor(gevent.Greenlet):
#
#     def __init__(self):
#         self.inbox = Queue()
#         Greenlet.__init__(self)
#
#     def receive(self, message):
#         """
#         Define in your subclass.
#         """
#         raise NotImplemented()
#
#     def _run(self):
#         self.running = True
#
#         while self.running:
#             message = self.inbox.get()
#             self.receive(message)
#
# class Pinger(Actor):
#     def receive(self, message):
#         print(message)
#         pong.inbox.put('ping')
#         gevent.sleep(0)
#
# class Ponger(Actor):
#     def receive(self, message):
#         print(message)
#         ping.inbox.put('pong')
#         gevent.sleep(0)
#
# ping = Pinger()
# pong = Ponger()
#
# ping.start()
# pong.start()
#
# ping.inbox.put('start')
# gevent.joinall([ping, pong])
from flask import Flask, render_template, request

from gevent import queue
from gevent.pywsgi import WSGIServer

import json

app = Flask(__name__)
app.debug = True



users = {}

class Room(object):

    def __init__(self):
        self.users = set()
        self.messages = []

    def backlog(self, size=25):
        return self.messages[-size:]

    def subscribe(self, user):
        self.users.add(user)

    def add(self, message):
        for user in self.users:
            print(user)
            user.queue.put_nowait(message)
        self.messages.append(message)
rooms = {
    'topic1': Room(),
    'topic2': Room(),
}
class User(object):

    def __init__(self):
        self.queue = queue.Queue()

@app.route('/')
def choose_name():
    return render_template('choose.html')

@app.route('/<uid>')
def main(uid):
    return render_template('main.html',
        uid=uid,
        rooms=rooms.keys()
    )

@app.route('/<room>/<uid>')
def join(room, uid):
    user = users.get(uid, None)

    if not user:
        users[uid] = user = User()

    active_room = rooms[room]
    active_room.subscribe(user)
    print('subscribe %s %s' % (active_room, user))

    messages = active_room.backlog()

    return render_template('room.html',
        room=room, uid=uid, messages=messages)

@app.route("/put/<room>/<uid>", methods=["POST"])
def put(room, uid):
    user = users[uid]
    room = rooms[room]

    message = request.form['message']
    room.add(':'.join([uid, message]))

    return ''

@app.route("/poll/<uid>", methods=["POST"])
def poll(uid):
    try:
        msg = users[uid].queue.get(timeout=10)
    except queue.Empty:
        msg = []
    return json.dumps(msg)

if __name__ == "__main__":
    http = WSGIServer(('', 5000), app)
    http.serve_forever()