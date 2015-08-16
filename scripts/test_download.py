#!/usr/bin/python2.7

from merra.merra_mgr import *
mt = merra_tool()
mt.download()
mt.disconnect()
