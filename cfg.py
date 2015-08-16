# You can use this software for your purpose provided you include below two lines.
# This file is part of merra_data_analyzer, a high-level ftp-protocol big size recursive file downloader and merra file analyser.
# Copyright : Mantosh Kumar @ TUM, Germany

from merra.merra_constants import *

MEERA_ANALYZER_CFG = {   
                         USER_EMAIL_ADDR : 'demo@tum.de',
                         MERRA_DATA_DOWNLOAD_PATH  : './merra_downloaded_data',
                         STORE_DOWNLOADED_DATA : True, # Set to True if you want to store downloaded files
                         
                         FTP_DEBUG_LEVEL : 1, # 0 = none, 1 = some output, 2 = max debugging output
                         
                         HOST_ADDR : '169.154.132.64', # 'goldsmr3.sci.gsfc.nasa.gov'
                         #DIR_NAME  : "data/s4pa/MERRA_MONTHLY/MATMNXFLX.5.2.0/2015",    #Scope of improvement
                         HOME_DIR  : "data",    #Scope of improvement
                         FILE_TYPE : '*.hdf',
                         
}


