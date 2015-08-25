# You can use this software for your purpose provided you include below two lines.
# This file is part of merra_data_analyzer, a high-level ftp-protocol big size recursive file downloader and merra file analyser.
# Copyright : Mantosh Kumar @ TUM, Germany

from merra.merra_constants import *

# NOTE: By default every field is assigned values, you can change a/o your need

MEERA_ANALYZER_CFG = {  
                         # Use below setting only&only if you want to use an already downloaded specific HDF file, \ 
                         # otherside always set this to None (No connection with internet is needed for this case) \
                         # If want to enable it, Enter the Parent directory name of the downloaded files, it will- \
                         #    - find all the hdf files stored in subdirectory also
                         # Note: If you enable this setting then all other settings will automatically become idle.
                         YOUR_DOWNLOADED_HDFFILE_DIR_PATH: None, # '../hdf_data',



                         # Two General settings
                         MERRA_DATA_DOWNLOAD_DIR  : './merra_downloaded_data',
                         SAVE_DOWNLOADED_DATA     : False, # Set to True if you want to store downloaded files


                         # In case of network failure, number of maximum tries to reconnect with network
                         MAX_ATTEMPTS_TO_DOWNLOAD  : 11,

                         # If the connection dies, wait this long(seconds) before reconnecting
                         RETRY_TIMEOUT :  15,


                         # Technically advanced five settings
                         USER_EMAIL_ADDR : 'demo@tum.de', # NASA uses email as password for login (even dummy email will work)

                         HOST_ADDR : 'goldsmr3.sci.gsfc.nasa.gov', # '169.154.132.64'

                         FTP_DEBUG_LEVEL : 0, # 0 = none, 1 = some output, 2 = max debugging output \
                                              # Use this setting to observe interacton of this tool with ftp server

                         HOME_DIR  : ["data"],    # Home directory over ftp server
                         FILE_TYPE : '.hdf',     # Type of downloading file
                      
                         
}



