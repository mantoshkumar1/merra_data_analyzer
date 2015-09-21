#!/usr/bin/python2.7

import os

#### Importing MERRA tool modules
from merra.merra_mgr import *
from merra_db_operation.ExtractMerra import *
from merra_db_operation.merra_product import *
from merra_db_operation.MerraDataBase import *
import cfg

cfg = cfg.MEERA_ANALYZER_CFG

##### Enabling logging of merra tool
log_file = open(cfg[MERRA_LOGGING_FILE_PATH], 'a+')


##### MERRA products info handler 
Merra = Merra_Product(log_file)


##### MERRA data extraction handler
Extract = ExtractMerraFile(log_file) 


##### MERRA DataBase handler
DB = MerraDatabase(cfg[MERRA_DB_NAME], cfg[MERRA_DB_LOGIN], cfg[MERRA_DB_PASSWORD], cfg[MERRA_DB_HOST_IP], \
                   cfg[MERRA_DB_PORT], log_file)


##### MERRA FTP HANDLER
mt = merra_tool(DB, Merra, Extract, log_file)
mt.download_process_hdf_data()


##### Closing application
mt.disconnect()


##### Closing log file
log_file.close()




