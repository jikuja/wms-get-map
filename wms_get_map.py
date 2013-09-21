#!/usr/bin/python
import os
import sys
import argparse
import logging as log
import requests


PYPROJ_DISABLED = False
GEOPY_DISABLED = False

try:
    import pyproj
except:
    PYPROJ_DISABLED = True

try:
    import geopy.geocoders
except ImportError:
    GEOPY_DISABLED = True

if sys.version_info >= (3,):
    try:
        import owslib.wms
    except ImportError:
        sys.path.append(os.path.join("", "lib"))
        import owslib.wms
else:
    import owslib.wms

if not PYPROJ_DISABLED:
    WGS84 = pyproj.Proj("+init=EPSG:4326")
    TM35FIN = pyproj.Proj("+proj=utm +zone=35 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs")
    KKJ = pyproj.Proj("+proj=tmerc +lat_0=0 +lon_0=27 +k=1 +x_0=3500000 +y_0=0 +ellps=intl +towgs84=-96.062,-82.428,-121.753,4.801,0.345,-1.376,1.496 +units=m +no_defs")

def fetch_pdf(coordinates, size, scale):
    payload = { 'E': coordinates[0], 'N': coordinates[1], 'leveys': size[0], 'korkeus': size[1], 'mittakaava': scale }
    r = requests.get("http://pikakartta.kapsi.fi/kartta.php", params=payload)
    #TODO: check for errors!
    return r.content


def fetch_tile(wms, coordinates, size_in, size_out, layer):
    img = wms.getmap(
            layers=[layer],
            srs='EPSG:3067',
            bbox=(coordinates[0], coordinates[1], 
                coordinates[0]+size_in[0], coordinates[1]+size_in[1]),
            size=(size_out[0], size_out[1]),
            format='image/png'
            )
    return img

def convert_coordinate(system_from, system_to, coordinates):
    if isinstance(system_from, str):
        system_from = pyproj.Proj(system_from)
    if isinstance(system_to, str):
        system_to = pyproj.Proj(system_to)
    converted = pyproj.transform(system_from, system_to, coordinates[0], coordinates[1])
    return [converted[0], converted[1]]

def wgs84_to_tm35(coordinates):
    converted = pyproj.transform(WGS84, TM35FIN, coordinates[0], coordinates[1])
    log.info("ETRS-TM35: " + str( [converted[0], converted[1]]))
    return [converted[0], converted[1]]

def kkj_to_tm35(coordinates):
    converted = pyproj.transform(KKJ, TM35FIN, coordinates[0], coordinates[1])
    log.info("ETRS-TM35: " + str( [converted[0], converted[1]]))
    return [converted[0], converted[1]]

def get_coordinates(geo, address):
    if geo == "google":
        log.debug("Using GoogleV3 geocoder")
        try:
            coder = geopy.geocoders.GoogleV3()
        except AttributeError:
            log.error("Exiting: Geopy doesn't have GoogleV3. Maybe too old version of geopy.")
            sys.exit()
        place, (lat, lon) = coder.geocode(address, sensor=False)
        log.debug("Geocoded place: " + place)
        log.info("WGS 84: " + str([lon, lat]))
        return [lon, lat]

def parse_geometry(s, reason):
    try:
        width,  height = s.split("x")
    except ValueError:
        log.error("Separator missing or too many separators while parsing " + reason)
        sys.exit()
    try:
        width = int(width)
        height = int(height)
    except ValueError:
        log.error("Integer required when parsing " + reason)
        sys.exit()
    return [width, height]

def init_logger(verbose):
    if verbose == 0:
        log.basicConfig(format="%(levelname)s: %(message)s")
    elif verbose == 1:
        log.basicConfig(format="%(levelname)s: %(message)s", level=log.INFO)
        log.info("Verbose output.")
    else:
        log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
        log.info("Verbose output.")

def check_packages():
    if GEOPY_DISABLED:
        log.error("geopy disabled: can't use geocoder(--address)!")
    if PYPROJ_DISABLED:
        log.error("pyproj disabled: can't convert coordinates! Can't use GoogleV3 geocoder!")

def can_use_geocoder():
    return GEOPY_DISABLED != True and PYPROJ_DISABLED != True

def use_given_coordinates(args):
    if args.wgs_84:
        wgs84_coordinates = [args.x, args.y]
        log.debug("Coordinates are given in WGS84: " + str(wgs84_coordinates))
        tm35_coordinates = wgs84_to_tm35(wgs84_coordinates)
    elif args.kkj:
        kkj_coordinates = [args.x, args.y]
        log.debug("Coordinates are given in KKJ: " + str(kkj_coordinates))
        tm35_coordinates = kkj_to_tm35(kkj_coordinates)
    elif args.srs != "":
        weird_coordinates = [args.x, args.y]
        log.debug("Coordinates are given in " + args.srs + ": " + str(weird_coordinates))
        tm35_coordinates = convert_coordinate(args.srs, TM35FIN, weird_coordinates)
    elif args.tm35fin:
        log.debug("Coordinates are given in ETRS-TM35FIN")
        tm35_coordinates = [args.x, args.y]
    else:
        log.debug("ERROR!!! ASSERT LOL! APUA")

    log.info("ETRS-TM35: " + str(tm35_coordinates))
    return tm35_coordinates

def check_arguments(args):
    if args.address == None or GEOPY_DISABLED == True or PYPROJ_DISABLED == True:
        if args.x != None and args.y != None:
            try:
                args.x = float(args.x)
                args.y = float(args.y)
            except ValueError:
                log.error("both x and y must be floats")
                sys.exit()
        else:
            log.error(":error: -1 or x and y are required")
            sys.exit()

    try:
        if args.size_input != None:
            args.size_input = parse_geometry(args.size_input, "output size")
    except AttributeError:
        pass
    try:
        if args.size_output != None:
            args.size_output = parse_geometry(args.size_output, "input size")
    except AttributeError:
        pass

if __name__ == "__main__":
    pass
