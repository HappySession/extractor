import numpy as npimport
import pygrib as pygrib
import urllib.request
import json
import logging
import happy.util.gribindex
import happy.util.database
from datetime import datetime

epoch = datetime.utcfromtimestamp(0)


def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0


def happypy_api_version():
    return "0.0.0"


def run(offset):
    logging.info('start ww3 extraction')

    current = datetime.now()
    d = current.replace(hour=6, minute=0, second=0, microsecond=0)
    epoch = (d - datetime(1970, 1, 1)).total_seconds()
    print(d.strftime("%Y-%m-%d %H:%M%S.%f"), epoch)
    mydate = d.strftime("%Y%m%d")
    r = 0.25
    tz = "00"
    count = 0
    db = happy.util.database.connect()
    while count < 121:
        tmp = str(count).zfill(3)
        count = count + 1
        url = "http://nomads.ncep.noaa.gov/pub/data/nccf/com/wave/prod/multi_1." + mydate + \
            "/multi_1.glo_30m.t" + tz + "z.f" + "{0:0=3d}".format(offset) + ".grib2"
        print("DL inventory of " + url)
        urllib.request.urlretrieve(url, "tmp.ww3.grib2")
        grbs = pygrib.open("tmp.ww3.grib2")
        for grb in grbs:
            print(grb)

        grb = grbs[1]  # 1:Wind speed:m s**-1
        # extract data and get lat/lon values for a subset over France
        # caution negative longitude are not allowed
        #temps, lats, lons = grb.data(lat1=41, lat2=52, lon1=0, lon2=10)
        windSpeeds, lats, lons = grb.data(lat1=41, lat2=52, lon1=355, lon2=360)

        grb = grbs[2]  # Wind direction:Degree true
        windDirections, lats, lons = grb.data(
            lat1=41, lat2=52, lon1=355, lon2=360)

        grb = grbs[3]  # uwind
        uwinds, lats, lons = grb.data(lat1=41, lat2=52, lon1=355, lon2=360)

        grb = grbs[4]  # uwind
        vwinds, lats, lons = grb.data(lat1=41, lat2=52, lon1=355, lon2=360)

        # 5 Significant height of combined wind waves and swell:m
        grb = grbs[5]
        combinedWaveHeights, lats, lons = grb.data(
            lat1=41, lat2=52, lon1=355, lon2=360)

        # 6:Primary wave mean period:s
        grb = grbs[6]
        primaryWaveMeanPeriods, lats, lons = grb.data(
            lat1=41, lat2=52, lon1=355, lon2=360)

        # 7:Primary wave direction:Degree
        grb = grbs[7]
        primaryWaveMeanDirections, lats, lons = grb.data(
            lat1=41, lat2=52, lon1=355, lon2=360)

        # 8:Significant height of wind waves:m
        grb = grbs[8]
        windWaveHeights, lats, lons = grb.data(
            lat1=41, lat2=52, lon1=355, lon2=360)

        # 9:Significant height of swell waves:m
        grb = grbs[9]
        significantWaveHeights, lats, lons = grb.data(
            lat1=41, lat2=52, lon1=355, lon2=360)

        # json data

        i = 0
        while i < len(lats):
            j = 0
            while j < len(lats[1]):
                _id = str(epoch) + "-" + str(lats[i][j]) + "-" + str(
                    lons[i][j])
                db.ww3.update({
                    "_id": _id
                }, {
                    "_id": _id,
                    "index_lat": lats[i][j],
                    "index_lon": lons[i][j] - 360,
                    "location": {
                        "type": "Point",
                        "coordinates": [lons[i][j], lats[i][j]]
                    },
                    "uwind": uwinds[i][j].item(),
                    "vwind": vwinds[i][j].item(),
                    "wind_speed": windSpeeds[i][j].item(),
                    "wind_direction": windDirections[i][j].item()
                },
                              upsert=True)

                j += 1
            i += 1
        offset = offset + 1
    return