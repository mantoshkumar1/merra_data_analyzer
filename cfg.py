# You can use this software for your purpose provided you include below two lines.
# This file is part of merra_data_analyzer, a high-level ftp-protocol big size recursive file downloader and merra file analyser.
# Copyright : Mantosh Kumar @ TUM, Germany

from merra.merra_constants import *

# NOTE: By default every field is assigned values, you can change a/o your need

MEERA_ANALYZER_CFG = {  
                         # Use below setting only&only if you want to use already downloaded HDF files. \ 
                         # Otherside always set it to None (No connection with internet is needed for this case) \
                         # If you want to enable this setting, Enter the parent directory path of the downloaded files, \
                         #    - it will find all the hdf files stored inside this directory & its subdirectories \
                         # Note: If you enable this setting then below all other settings will automatically become idle \
                         #       - except PROCESSING_FILE_TYPE

                         YOUR_DOWNLOADED_HDFFILE_DIR_PATH: None, # '../my_hdf_data',



                         # Two General settings
                         ########################################################################################################

                         # 1. Directory where you want to download HDF files
                         MERRA_DATA_DOWNLOAD_DIR_PATH  : './merra_downloaded_data',

                         # 2. Set to True if you want to store downloaded files
                         SAVE_DOWNLOADED_DATA  : False,

                         ########################################################################################################



                         # Two network failure settings
                         ########################################################################################################

                         # In case of network failure, number of maximum tries to reconnect with network
                         MAX_ATTEMPTS_TO_DOWNLOAD : 11,

                         # If the connection dies, wait this long(seconds) before reconnecting
                         RETRY_TIMEOUT :  15,

                         ########################################################################################################


                         # Technically advanced five settings
                         ########################################################################################################
                         
                         USER_EMAIL_ADDR : 'demo@tum.de', # NASA uses email as password for login (even dummy email will work)

                         FTP_HOST_ADDR   : 'goldsmr3.sci.gsfc.nasa.gov', # '169.154.132.64'

                         FTP_DEBUG_LEVEL : 0, # 0 = none, 1 = some output, 2 = max debugging output \
                                              # Use this setting to observe interacton of this tool with ftp server

                         FTP_HOME_DIR         : ["data"],    # Home directory over ftp server
                         PROCESSING_FILE_TYPE : '.hdf',     # Type of downloading/processing file

                         ########################################################################################################
                      
                         
}



