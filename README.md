# Grib data extractor

Python 3 application for GRIB data extraction

You can use in a local mode with the **docker-compose** file.

You can share data volume with the **apy** project for locally test

    volumes:
      - SHARED_DIRECTORY/data:/data/db

To startup and test locally

    docker-compose up -d --build
    #and
    docker-compose up

# locally build

## vitualenv

    init virtualenv
    virtualenv venv

choose python 3 interpreter

    virtualenv -p /Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6 venv

source

    source venv/bin/activate
    which python

check

python --version

desactive current virtualenv

    deactivate

## install app

    pip install numpy
    pip install pymongo
    pip install schedule

#### pygrib

    git clone https://github.com/jswhit/pygrib.git
    cd pygrib
    pip install Cython
    pip install pyproj

from MacOS

python setup.py build
python setup.py install

# TODO

- finish GFS feature
- finish scheduler feature
