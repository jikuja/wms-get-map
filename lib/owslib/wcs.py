# -*- coding: ISO-8859-15 -*-
# =============================================================================
# Copyright (c) 2004, 2006 Sean C. Gillies
# Copyright (c) 2007 STFC <http://www.stfc.ac.uk>
#
# Authors : 
#          Dominic Lowe <d.lowe@rl.ac.uk>
#
# Contact email: d.lowe@rl.ac.uk
# =============================================================================

"""
Web Coverage Server (WCS) methods and metadata. Factory function.
"""


import urllib.request, urllib.error, urllib.parse
from . import etree
from .coverage import wcs100, wcs110, wcsBase

def WebCoverageService(url, version=None, xml=None, cookies=None):
    ''' wcs factory function, returns a version specific WebCoverageService object '''
    
    if version is None:
        if xml is None:
            reader = wcsBase.WCSCapabilitiesReader()
            request = reader.capabilities_url(url)
            if cookies is None:
                xml = urllib.request.urlopen(request).read()
            else:
                req = urllib.request.Request(request)
                req.add_header('Cookie', cookies)   
                xml=urllib.request.urlopen(req)
        capabilities = etree.etree.fromstring(xml)
        version = capabilities.get('version')
        del capabilities
        
    if version == '1.0.0':
        return wcs100.WebCoverageService_1_0_0.__new__(wcs100.WebCoverageService_1_0_0, url, xml, cookies)
    elif version == '1.1.0':
        return wcs110.WebCoverageService_1_1_0.__new__(wcs110.WebCoverageService_1_1_0,url, xml, cookies)
