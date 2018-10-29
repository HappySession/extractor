import math


def latitude_as_grib_index(resolution, lat):
    # lat(0,25°)
    if (resolution == "SMALL"):
        return math.floor((90 - lat) * 4)

        # lat(0,5°)
    elif (resolution == "MEDIUM"):
        return math.floor((90 - lat) * 2)

        # lat(1°)
    elif (resolution == "LARGE"):
        return math.floor(90 - lat)

    # lat(2.5°)∑
    elif (resolution == "EXTRALARGE"):
        return math.floor(36 - lat / 2.5)


def longitude_as_grib_index(resolution, lon):
    # lat(0,25°)
    if (resolution == "SMALL"):
        if (lon >= 0):
            return math.floor(lon * 4)
        else:
            return math.ceil((360 + lon) * 4)
