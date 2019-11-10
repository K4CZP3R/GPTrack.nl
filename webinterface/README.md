# Webinterface GPTrack.nl

## How install it

#### Windows

1. Download [Python 3.6.5](https://www.python.org/ftp/python/3.6.5/python-3.6.5-amd64-webinstall.exe) or another version 3.x and install it (add python to PATH).
2. Download [MongoDB server](https://fastdl.mongodb.org/win32/mongodb-win32-x86_64-2012plus-4.2.1-signed.msi) and install it (don't install it as a service).

#### Linux

1. `sudo apt-get update && sudo apt-get upgrade`
2. `sudo apt-get install python3 python3-dev python3-setuptools python3-pip`
3. Follow [this]( https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/ ) tutorial for MongoDB server installation steps.

## How to setup env. (First time use)

#### Windows

1. Create `virualenv` (do it in `proftaak/venv` , otherwise it won't be ignored when pushing)
   1. cd intro root of the repo
   2. `python -m venv venv`
   3. `venv\Scripts\activate.bat`  (type it, don't go there)
   4. `cd webinterface` 
   5. `pip install pyopenssl`
   6. `pip install -r requirements.txt` (Install all dependencies)

#### Linux

1. Create `virtualenv` (do it in `proftaak/venv`, otherwise it won't be ignored when pushing)
   1. cd intro root of the repo
   2. `sudo apt install python3-venv`
   3. `python3.6 -m venv venv`
   4. `source venv/bin/activate`
   5. `cd webinterface`
   6. `pip install wheel pyopenssl` 
   7. `pip install -r requirements.txt`

## How to run it?

#### Windows

1. Start `mongod.exe` (It is in the default install path of MongoDB [`C:\Program Files\MongoDB\Server\4.2\bin`])
2. Activate virtual environment: `venv\Scripts\activate.bat` (You need to be in the root of repo)
3. Go to `webinterface dir` using the same command prompt and execute: `python app.py`
4. Server will start and you can start using it!

#### Linux

1. Activate virtual environment: `source venv/bin/activate` (You need to be in the root of repo)
2. Go to `webinterface dir` and execute `python3 app.py`
3. Server will start and you can start using it!

You can configure this server by editing `app_config.py`