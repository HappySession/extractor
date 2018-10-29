#Base image
FROM python:3.6

#Labels and Credits
LABEL \
    name="extractor" \
    author="Happy Session <happy@happysession.org>" \
    maintainer="Happy Session <happy@happysession.org>" \
    description="Dockerize Python application for forecasts grib data extraction"

USER root

#Install Python 3
RUN \
    apt-get update -y && apt install -y git \
    libgrib-api-dev libgrib-api0  python-gribapi

RUN \
    pip install numpy pyproj pymongo schedule

WORKDIR core
RUN git clone https://github.com/jswhit/pygrib.git
WORKDIR pygrib
COPY setup.cfg .
RUN python setup.py build
RUN python setup.py install 


# create happy user
RUN useradd -r happy
WORKDIR /core
ADD happy.py .
COPY happy happy
RUN pwd

CMD [ "python", "happy.py" ]