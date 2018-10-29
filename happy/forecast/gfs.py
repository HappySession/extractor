import numpy as npimport 
import pygrib as pygrib
import urllib.request
from pymongo import MongoClient
import json
from datetime import datetime
import happy.util.gribindex

epoch = datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

def happypy_api_version():
    return "0.0.0"

def run(offset, p):
    # mongo connect
    db = client.happy

    current = datetime.now()
    d = current.replace(hour=6, minute=0, second=0, microsecond=0)
    epoch = (d-datetime(1970, 1, 1)).total_seconds()
    print(d.strftime("%Y-%m-%d %H:%M%S.%f"), epoch)
    mydate = d.strftime("%Y%m%d")
    p = "25"
    tmp = "003"    
    r = 0.25
    tz = "00"    
    count = 3
    while count < 121:        
        tmp = str(count).zfill(3)
        count = count+1
        url = "http://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs." + mydate+offset + \
            "/gfs.t" + tz + "z.pgrb2.0p" + p + ".f" + tmp
        print("DL inventory of "+url)
        urllib.request.urlretrieve(url, "tmp.gfs.grib2")
        grbs = pygrib.open("tmp.gfs.grib2")
        for grb in grbs:
            print(grb)

        grb = grbs[250]  # temperature
        # extract data and get lat/lon values for a subset over France
        # caution negative longitude are not allowed
          #temps, lats, lons = grb.data(lat1=41, lat2=52, lon1=0, lon2=10)
        temps, lats, lons = grb.data(lat1=41, lat2=52, lon1=355, lon2=360)

        grb = grbs[5]  # gust
        gusts, lats, lons = grb.data(lat1=41, lat2=52, lon1=355, lon2=360)

        grb = grbs[2]  # uwind
        uwinds, lats, lons = grb.data(lat1=41, lat2=52, lon1=355, lon2=360)

        grb = grbs[3]  # uwind
        vwinds, lats, lons = grb.data(lat1=41, lat2=52, lon1=355, lon2=360)

        # 292:Precipitation rate:kg m**-2 s**-1 (avg):regular_ll:surface:level 0:fcst time 6-10 hrs (avg):from 201808100000
        grb = grbs[292]
        precipitationsRate, lats, lons = grb.data(
            lat1=41, lat2=52, lon1=355, lon2=360)

        # 293:Total Precipitation:kg m**-2 (accum):regular_ll:surface:level 0:fcst time 6-10 hrs (accum):from 201808100000
        grb = grbs[293]
        precipitations, lats, lons = grb.data(
            lat1=41, lat2=52, lon1=355, lon2=360)

        # 317:Total Cloud Cover:% (avg):regular_ll:unknown:level 0 214:fcst time 6-10 hrs (avg):from 201808100000
        grb = grbs[317]
        total_cloud_covers, lats, lons = grb.data(
            lat1=41, lat2=52, lon1=355, lon2=360)

        # 318:Total Cloud Cover Midlle:% (avg):regular_ll:unknown:level 0 224:fcst time 6-10 hrs (avg):from 201808100000
        grb = grbs[318]
        total_cloud_covers_middle, lats, lons = grb.data(
            lat1=41, lat2=52, lon1=355, lon2=360)

        # 319:Total Cloud Cover High:% (avg):regular_ll:unknown:level 0 234:fcst time 6-10 hrs (avg):from 201808100000
        grb = grbs[319]
        total_cloud_covers_high, lats, lons = grb.data(
            lat1=41, lat2=52, lon1=355, lon2=360)

        # 320:Total Cloud Cover Low:% (avg):regular_ll:unknown:level 0 10:fcst time 6-10 hrs (avg):from 201808100000
        grb = grbs[320]
        total_cloud_covers_low, lats, lons = grb.data(
            lat1=41, lat2=52, lon1=355, lon2=360)
        # 415:Pressure reduced to MSL:Pa (instant):regular_ll:meanSea:level 0:fcst time 10 hrs:from 201808100000
        grb = grbs[265]
        pressures, lats, lons = grb.data(lat1=41, lat2=52, lon1=355, lon2=360)



        # json data
        i = 0
        while i < len(lats):
            j = 0
            while j < len(lats[1]):
                _id = str(epoch)+"-"+str(lats[i][j])+"-"+str(lons[i][j])
                db.Gfs.update({"_id": _id}, {"_id": _id, "lat": lats[i][j], "lon": lons[i][j]-360, "location": {"type": "Point", "coordinates": [lons[i][j], lats[i][j]]}, "resolution": p,
                                             "uwind": uwinds[i][j].item(), "vwind": vwinds[i][j].item(),
                                             "temp": temps[i][j].item(), "gust": gusts[i][j].item(),
                                             "pressure": pressures[i][j].item(),
                                             "precipitation": precipitations[i][j].item(),
                                             "cloudTotal": total_cloud_covers[i][j].item(), "cloudLow": total_cloud_covers_low[i][j].item(), "cloudMiddle": total_cloud_covers_middle[i][j].item(), "cloudHigh": total_cloud_covers_high[i][j].item()}, upsert=True)

                j += 1
            i += 1

    return