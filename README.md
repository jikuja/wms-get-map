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
wms_get_map --output=foo.png -a taalaritie1+espoo

wms_get_map --url="http://kartat.espoo.fi/TeklaOgcWeb/WMS.ashx" --service="" --layer=Opaskartta  --output=foo.png 368673.5409250181 6676813.173829354

wms_get_map --output=foo.pdf --pdf --size-output=210x210 --scale=10000 -a taalaritie1+espoo

wms_get_map -h


Extras
------
extras/OWSLib-setup.py.diff: patch for OWSLib to partially support python3

This repository contains 2to3 converted version of OWSLib. WebMapService 
works other classes are untested!!!
