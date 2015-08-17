# You can use this software for your purpose provided you include below two lines.
# This file is part of merra_data_analyzer, a high-level ftp-protocol big size recursive file downloader and merra file analyser.
# Copyright : Mantosh Kumar @ TUM, Germany

from merra.merra_constants import *

# NOTE: By default every field is assigned values, you can change a/o your need

MEERA_ANALYZER_CFG = {  
                         # General two settings
                         MERRA_DATA_DOWNLOAD_PATH  : './merra_downloaded_data',
                         SAVE_DOWNLOADED_DATA : True, # Set to True if you want to store downloaded files

                         
                        
                         # Use below setting only&only if you want to use a specific already downloaded HDF file, \ 
                         # otherside always set this to None
                         YOUR_HDF_FILE_FULLPATH : None, # '/home/mantosh/Desktop/xyz.hdf'


                         # In case of network failure, number of maximum tries to reconnect with network
                         MAX_ATTEMPTS_TO_DOWNLOAD  : 11,

                         # If the connection dies, wait this long(seconds) before reconnecting
                         RETRY_TIMEOUT :  15,


                         # Technically advanced four settings
                         USER_EMAIL_ADDR : 'demo@tum.de', # NASA uses email as password for login (even dummy email will work)

                         HOST_ADDR : 'goldsmr3.sci.gsfc.nasa.gov', # '169.154.132.64'

                         FTP_DEBUG_LEVEL : 0, # 0 = none, 1 = some output, 2 = max debugging output \
                                              # Use this setting to observe interacton of this tool with ftp server

                         HOME_DIR  : ["data"],    # Home directory over ftp server
                         FILE_TYPE : '*.hdf', # Type of downloading file
                      

                         
}



