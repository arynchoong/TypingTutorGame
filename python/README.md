# Typing Tutor Game for Python
## Versions developed on
Python : 3.7.4.  
PyGame : 2.0.0.dev3  
SDL : 2.0.9  
OSX : macOS Mojave Version 10.14.6  

## To run game
### Install pygame

You need to have pygame version >= 2.0,  
since the codes developed is dependent on new features in version 2 that is not officially released at of writing this.

#### Virtual Environment
Run on terminal (or command line):
````console
$ python3 -m virtualenv venv
````

Activate the virtual environment.

For MacOS:
````console
$ source venv/bin/activate
````
#### MacOS only
Pre-install step for MacOS:

(The following is for MacOS only). 
venvdotapp helps the python be a mac 'app'. So that the pygame window can get focus.
````console
(venv)$ pip3 install venvdotapp
````

#### pip install

Install pygame:
````console
(venv)$ pip3 install pygame==2.0.0.dev6
````

### Play!
Run from src folder:
````console
(venv)$ python game.py
````