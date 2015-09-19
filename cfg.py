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
                         YOUR_LOCAL_HDFFILE_DIR_PATH   :  '/home/gaurav/Git_IDP/merra_data_analyzer/Gaurav_Stuff', #None,



                         # Nine FTP settings
                         ########################################################################################################

                         # 1. Directory path where you want to download HDF files
                         MERRA_DATA_DOWNLOAD_DIR_PATH  :  './merra_downloaded_data',

                         # 2. Set to True if you want to store downloading files in above directory
                         #            False: it will be deleted once db gets populated
                         SAVE_DOWNLOADING_DATA         :  False,

                         # 3. NASA FTP server uses email as password for login (even dummy email will work)
                         USER_EMAIL_ADDR               :  'demo@tum.de',

                         # 4. FTP host address **
                         FTP_HOST_ADDR        :  'goldsmr3.sci.gsfc.nasa.gov', # '169.154.132.64'

                         # 5. Home directory over ftp server **
                         # If you are uncertain which should be your parent dir over ftp server, set it to ["/"]
                         # Or, you can select multiple parent dir over ftp server in which you want to search. Ex:["/x/y", "dat"]
                         FTP_HOME_DIR         :  ["data"],

                         # 6. Use this setting to observe interacton of this tool with ftp server
                         #    0 = none, 1 = some output, 2 = max debugging output
                         FTP_DEBUG_LEVEL      :  0,

                         # 7. Type of downloading/processing file **
                         PROCESSING_FILE_TYPE :  '.hdf',

                         # Two network failure settings
                         ##############################

                         # 8. In case of network failure, number of maximum tries to reconnect with network
                         MAX_ATTEMPTS_TO_DOWNLOAD :  11,

                         # 9. If the connection dies, wait this long(seconds) before reconnecting
                         RETRY_TIMEOUT            :  15,

                         ########################################################################################################



                         # Six MERRA DB settings
                         ########################################################################################################
                         
                         # 1. Tool DB Name
                         MERRA_DB_NAME                 :  'merra',

                         # 2. Tool DB user name
                         MERRA_DB_LOGIN                :  'postgres', #mantosh

                         # 3. Tool DB password
                         MERRA_DB_PASSWORD             :  'gnusmas', #password
 
                         # 4. Tool DB host ip **
                         MERRA_DB_HOST_IP              :  '127.0.0.1', 

                         # 5. Toob DB port **
                         MERRA_DB_PORT                 :  '5432',

                         # 6. Delete all data saved in merra db, all tables will be droped **
                         RESET_MERRA_DB       :   False,               

                         ########################################################################################################
                      

# Symbol ** : Technically advanced settings ( Caution: Are you sure you want to change these? )
                         
}



