# chat_room
This is the code for a LAN chat room.

To git it on your machine:
`$ mkdir path/to/your/project/directory/`
`$ cd path/to/your/project/directory/`
`$ git clone https://github.com/jacoblapenna/chat_room`

To use it on your machine/LAN:
`$ python3 -m venv chat_env` to make your chat python environment
`$ source chat_env/bin/activate` to activate your python environment
`(chat_env) $ python --version` to enure `python` command maps to the python version installed in your environment
`(chat_env) $ pip -r install requirements.txt` to install needed dependencies
`(chat_env) $ python irc.py` to start the chat program

Open your browser, navigate to the ip and port printed in the console after starting the chat program. Note that the function serving the app auto-detects changes made to irc.py, landing.html, and index.html. This means that any changes made to these files while the program is running will be auto-detected once saved and re-served with the changes. Note that css styles are cached in the browser. In order to update any changes made to css since the previous page load, you must have the borwser development tools open, go to the "network" tab, and check the "Disable cache" box.
