# LSB Steganography

Using LSB method to encrypt and decrypt text on image with format .png or .jpg

### Installation

Make sure python 3xx is installed on your system, me only provide configuration for windows user (for linux and mac should be similar):

First, move into dir where do you want to put the cloning git, for example E:
```sh
$ git clone [git-repo-url]ldpc-img.git
$ cd ldpc-img
```
set virtual environment for django project on E:/lsb/, so it won't bother your machine.
then activate it like this.
```sh
$ python -m venv myenv
$ myenv/Scripts/activate.bat
```
after its activated, download django into your virtual environment.
```sh
$ (myvenv) ~$ pip install django
```
or
```sh
$ (myvenv) ~$ python -m pip install django
```
install dependencies - use pip to install all dependecies (make sure pip is installed on your virtual environment)
```sh
$ (myvenv) ~$ pip install -r requirements.txt 
```
Runserver - find file manage.py then run it like so
```sh
$ (myvenv) ~$ python manage.py runserver 
```
