wms-get-map
===========
Simple script to fetch maps from WMS.

Requirements
------------
TODO

Bugs
----
Script is mostly hardcoded to use ETRS-TM35FIN coordinate system in WMS requests.
Output format is hardcoded.


Examples
--------
get_wms_map --output=foo.png -a taalaritie1+espoo
Fetch map from WMS server using geopy's geocoder. Default geocoder is GoogleV3.

get:wms_map --output=foo.png --kkj 3368789.644 6679617.082
Fetch map from previous position but use KKJ3 coordinates instead of geocoder.

get_wms_map --url="http://kartat.espoo.fi/TeklaOgcWeb/WMS.ashx" --service="" --layer=Opaskartta  --output=foo.png 368673.5409250181 6676813.173829354
Fetch map from previous location but use different WMS server and use ETRS-TM35FIN coordinates.

get_pdf_map --output=foo.pdf --pdf --size-output=210x210 --scale=10000 -a taalaritie1+espoo
Download PDF map of previous location from http://pikakartta.kapsi.fi
--size-output is output size in mm and --scale defines scale of printed map.

Extras
------
extras/OWSLib-setup.py.diff: patch for OWSLib to partially support python3

This repository contains 2to3 converted version of OWSLib. WebMapService 
works other classes are untested!!!
