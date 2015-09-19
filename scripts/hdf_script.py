#!/usr/bin/python2.7

#### Importing MERRA tool modules
from merra.merra_mgr import *
from merra_db_operation.ExtractMerra import *
from merra_db_operation.merra_product import *
from merra_db_operation.MerraDataBase import *
import cfg
import os

cfg = cfg.MEERA_ANALYZER_CFG

##### Enabling logging of merra tool
log_file = open('./log','a+')

##### MERRA products info handler 
Merra = Merra_Product(log_file)
Merra.ExtractingMerraProductsInfo()


##### MERRA data extraction handler
Extract = ExtractMerraFile(log_file) 


##### DataBase Initialization
DB = MerraDatabase(cfg[MERRA_DB_NAME], cfg[MERRA_DB_LOGIN], cfg[MERRA_DB_PASSWORD], cfg[MERRA_DB_HOST_IP], \
                   cfg[MERRA_DB_PORT], log_file)

DB.DatabaseConnection()
tablename = DatabaseTablesName['FilesAdded']
## Table name should be in LowerCase only
tablename = tablename.lower()
flag = DB.check_If_Table_Exist(tablename)
DB.CreateTableforFiles(tablename)


##### MERRA FTP HANDLER
mt = merra_tool(DB, Merra, Extract, log_file)
mt.download_process_hdf_data()


##### Closing application
mt.disconnect()

#closing log file
log_file.close()




