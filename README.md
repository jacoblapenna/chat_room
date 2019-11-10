# chat_room
This is the code for a LAN chat room.

### To git it on your machine:

`$ mkdir path/to/your/project/directory/git_clone` to make a folder called `git_clone` within at the directory of your choosing.

`$ cd path/to/your/project/directory/git_clone`

`$ git clone https://github.com/jacoblapenna/chat_room`

You should now have a directory in `path/to/your/project/directory/git_clone/` called `chat_room` containing all the relevant code locally on your machine, as well as a folder called `.git` for taking to the git server.

## Hacking on the code:

### To use it on your machine/LAN:

Best practice is to make a python virutal environment to run, test, and hack on the code. This will install symbolic links to python within your development directory. Also, when this program is ran, it will create a database in its local directory holding all the chat logs from chats you've hosted. In order to prevent these files from being committed and pushed to the master repository, you should make a development directory for hacking on the code. Then replace the changed files back in your `git_clone` directory for committing and pushing to the master repo on github. (An alternative would be to specifically call out these files to .gitignore, but this may cause inadvertant uploads should you miss something (like the pycache file).)

From within `path/to/your/project/directory/`:

`$ mkdir chat_room_dev`

`$ cp -a /git_clone/chat_room/. /chat_room_dev/` to put all the code files in your development directory.

`$ cd chat_room_dev`

Now you can start hacking on the code, but first, make a python environment form within `path/to/your/project/directory/chat_room_dev`:

`$ python3 -m venv chat_env` to make your chat python environment

`$ source chat_env/bin/activate` to activate your python environment

`(chat_env) $ python --version` to enure `python` command maps to the python version installed in your environment

`(chat_env) $ pip -r install requirements.txt` to install needed dependencies

`(chat_env) $ python irc.py` to start the chat program

Open your browser, navigate to the ip and port printed in the console after starting the chat program. Note that the function serving the app auto-detects changes made to irc.py, landing.html, and index.html. This means that any changes made to these files while the program is running will be auto-detected once saved and re-served with the changes. Note that css styles are cached in the browser. In order to update any changes made to css since the previous page load, you must have the borwser development tools open, go to the "network" tab, and check the "Disable cache" box.

### If you change the python dependencies:

`(chat_env) $ pip freeze > requirements.txt` to update the requirements document before commiting

### After making an awesome contribution:

Overwrite the files you changed within `path/to/your/project/directory/git_clone/chat_room/` with the desired changes.

`git add .` to add all changes to the upload queue

Sometime you have to associate the user making the change push with your git server, if so:

`git config --global user.email "your email address"`

`git config --global user.name "your name"`

Commit the changes:

`git commit -m "These are the notes describing what you changes and why you changed it. MAKE SURE THEY'RE GOOD!!!"`

Push the changes:

`git push origin your-branch-name-here`


