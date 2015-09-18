# You can use this software for your purpose provided you include below two lines.
# This file is part of merra_data_analyzer, a high-level ftp-protocol big size recursive file downloader and merra file analyser.
# Copyright : Mantosh Kumar @ TUM, Germany

from merra.merra_constants import *

# NOTE: By default every field is assigned values, you can change a/o your need

MEERA_ANALYZER_CFG = {  
                         # Use below setting only&only if you want to use already downloaded HDF files. \ 
                         # Otherside always set it to None (No connection with internet is needed in this case).
                         #
                         # If you want to enable this setting, Enter the parent directory path of the downloaded files, \
                         #    - it will find all the hdf files stored inside this directory & its subdirectories.
                         #
                         # Note: If you enable this setting then all below other settings related with FTP server will \
                         #       automatically become idle.
                         #YOUR_LOCAL_HDFFILE_DIR_PATH   :   None, #'/home/gaurav/Git_IDP/merra_data_analyzer/Gaurav_Stuff', 
                         YOUR_LOCAL_HDFFILE_DIR_PATH   :   '/home/mantosh/Desktop/hdf_data',



                         # Eight General settings
                         ########################################################################################################

                         # 1. Directory path where you want to download HDF files
                         MERRA_DATA_DOWNLOAD_DIR_PATH  :  './merra_downloaded_data',

                         # 2. Set to True if you want to store downloading files in above directory
                         #            False: it will be deleted once db gets populated
                         SAVE_DOWNLOADING_DATA         :  False,

                         # 3. NASA FTP server uses email as password for login (even dummy email will work)
                         USER_EMAIL_ADDR               :  'demo@tum.de',

                         # 4. Tool DB Name
                         MERRA_DB_NAME                 :  'merra',

                         # 5. Tool DB user name
                         MERRA_DB_LOGIN                :  'mantosh', #'postgres',

                         # 6. Tool DB password
                         MERRA_DB_PASSWORD             :  'password', #'gnusmas',
 
                         # 7. Tool DB host ip
                         MERRA_DB_HOST_IP              :  '127.0.0.1',

                         # 8. Toob DB port
                         MERRA_DB_PORT                 :  '5432',

                         ########################################################################################################



                         # Two network failure settings
                         ########################################################################################################

                         # 1. In case of network failure, number of maximum tries to reconnect with network
                         MAX_ATTEMPTS_TO_DOWNLOAD :  11,

                         # 2. If the connection dies, wait this long(seconds) before reconnecting
                         RETRY_TIMEOUT            :  15,

                         ########################################################################################################



                         # Four technically advanced settings ( Caution: Are you sure you want to change these? )
                         ########################################################################################################
                         
                         # 1. FTP host address
                         FTP_HOST_ADDR        :  'goldsmr3.sci.gsfc.nasa.gov', # '169.154.132.64'

                         # 2. Home directory over ftp server
                         # If you are uncertain which should be your parent dir over ftp server, set it to ["/"]
                         # Or, you can select multiple parent dir over ftp server in which you want to search. Ex:["/x/y", "dat"]
                         FTP_HOME_DIR         :  ["data"],

                         # 3. Use this setting to observe interacton of this tool with ftp server
                         #    0 = none, 1 = some output, 2 = max debugging output
                         FTP_DEBUG_LEVEL      :  0,

                         # 4. Type of downloading/processing file
                         PROCESSING_FILE_TYPE :  '.hdf',

                         ########################################################################################################
                      
                         
}



