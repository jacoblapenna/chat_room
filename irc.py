"""
this program is the workhorse of a website that mimics irc chat

Jacob Lapenna, 10/17/2019
"""

import time
import socket as sock
import sqlite3 as sql # may need to change to postgres if chat collisions
import multiprocessing as mp
from collections import deque
from flask_socketio import SocketIO
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)
socketio = SocketIO(app)
chat_members = {}

def get_ip_address():
    # get the server's IP on which to serve app
    # client can navigate to IP

    ip_address = '127.0.0.1'  # Default to localhost
    s = sock.socket(sock.AF_INET, sock.SOCK_DGRAM) # setup a socket object
    try:
        s.connect(('1.1.1.1', 1))  # does not have to be reachable
        ip_address = s.getsockname()[0]
    finally:
	    s.close()
    return ip_address

def make_table():
    # creates a new chat log table every time the app is launched
    # i.e. reluanch app to start a new chat session

    # we need the table of our chat session accessible throughout python
    global table_name

    # connect to the database
    conn = sql.connect('chat_logs.db')
    c = conn.cursor()

    # build a fairly unique table name
    time_stamp = str(round(time.time()))
    table_name = 'chat_log_' + time_stamp

    # create the table if no collision
    c.execute('CREATE TABLE IF NOT EXISTS ' +  table_name + \
                '(time real, ip text, nick text, input text)')

    # cleanup connection
    conn.commit()
    conn.close()

@app.route('/')
def serve_up_landing_page():
    # serve the landing page as root

    return render_template('landing.html') # render appropriate html

@app.route('/chat_room')
def serve_up_chat_page():
    # serve the chat room page whether they went through landing or not

    # obtain and process chat log
    conn = sql.connect('chat_logs.db') # connect to database
    c = conn.cursor() # create cursor object to navigate db
    formatted_log = [] # create array to store processed log entries
    # grab the whole log
    c.execute('SELECT * FROM ' + table_name)
    raw_chat_log = c.fetchall()
    if len(raw_chat_log): # if there are entries, process them
        for row in raw_chat_log:
            formatted_log.append(row[2] + ': ' + row[3])

    # cleanup db connection (nothing to commit)
    conn.close()

    # render appropriate html
    return render_template('index.html', chat_log=formatted_log)

@socketio.on('new_user')
def process_new_user(nick_input):
    # process the landing form input

    # get nick and associate with ip
    nick = nick_input
    ip_address = request.remote_addr

    # enter/update their credentials to global dict
    chat_members[ip_address] = nick

    # tell client to redirect to chat room
    client_sid = request.sid
    url = 'http://' + get_ip_address() + ':8080/chat_room'
    socketio.emit('redirect_to_chat_room', '/chat_room', room=client_sid)


@socketio.on('new_chat_input')
def process_chat_input(chat_input):
    # process chat input

    # get input and user specific information
    input_str = chat_input
    ip_address = request.remote_addr
    time_stamp = time.time()

    # associate user with their nick if any otherwise just use their ip
    if ip_address in chat_members.keys():
        nickname = chat_members[ip_address]
    else:
        nickname = ip_address

    # build dict/json of needed data
    new_entry = {
        'time' : time_stamp,
        'ip' : ip_address,
        'nick' : nickname,
        'input' : input_str
        }

    # update webpage with new entry
    socketio.emit('new_entry', new_entry, broadcast=True)

    # store entry to chat log
    conn = sql.connect('chat_logs.db') # connect to database
    c = conn.cursor() # create cursor object to navigate db
    # log the input
    c.execute("INSERT INTO " + table_name + " VALUES (?,?,?,?)",
              (time_stamp, ip_address, nickname, input_str))

    # cleanup connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    make_table()
    ip = get_ip_address()
    print("Attempting to serve page on %s:%d" % (ip, 8080))
    socketio.run(app,
                 host=ip,
                 port=8080,
                 use_reloader=True,
                 debug=False,
                 extra_files=['templates/index.html',
                              'templates/landing.html'])

"""
Things to do:
    1) SSL encryption
    2) Dockerize to sandboxed VM to protect machine hosting the code
    3) Add admininstrative controls to load an old chat log, list all available
       logs by date, etc
    4) Perhaps add text color to each user to better read long/dense logs
    5) Presently, sqlite is used for its ease of db storage, however, it does
       not support concurrent cursor operation. This means that if two users
       input a new entry simultaneously, the program could crash. To solve this,
       postgres should be used. However, postgres requires an sql server, which
       would have to be factored into the docker and VM when done. I think this
       would also require each user spooling up a unique python process when
       they create there handle. This process could create a new postgres user,
       which could have specific access rights given on creation. The process
       would live for as long as the chat session is live, and each entry is
       first attributed to the user, then handed off to that user's process for
       postgres write functions.
    6) Add functionality so that one cannot access the chat room without entering
       something in the landing page
    7) Given 6), the act of joining the room should announce a new user to
       everyone so that noone can lurk, particularly if we allow everyone on
       lan to join (high-permiscuity)
    8) CSS is always a work in progress for use across devices
        a. for example zoom back out to view whole log after input on an iphone
           as presently the screen zooms when in the input box, but its too
           zoomed in to see chat after hitting return
        b. could also present a custom keyboard on phones
        c. etc
"""
