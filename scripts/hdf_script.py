#!/usr/bin/python2.7


#### All Python Files Import
from merra.merra_mgr import *
from merra_db_operation.ExtractMerra import *
from merra_db_operation.merra_product import *
from merra_db_operation.MerraDataBase import *
import cfg
import os

cfg = cfg.MEERA_ANALYZER_CFG

##### MERRA PRODUCTS Info handler 
Merra = Merra_Product()
Merra.ExtractingMerraProductsInfo()


##### MERRA Data Extraction handler
Extract = ExtractMerraFile() 

#### DataBase Initialization
DB = MerraDatabase(cfg[MERRA_DB_NAME], cfg[MERRA_DB_LOGIN], cfg[MERRA_DB_PASSWORD], cfg[MERRA_DB_HOST_IP], cfg[MERRA_DB_PORT])
DB.DatabaseConnection()
tablename = DatabaseTablesName['FilesAdded']
## Table name should be in LowerCase only
tablename = tablename.lower()
flag = DB.check_If_Table_Exist(tablename)
DB.CreateTableforFiles(tablename)


#### MERRA FTP HANDLER
mt = merra_tool(DB, Merra, Extract)

mt.download_process_hdf_data()

mt.disconnect()

#### End

