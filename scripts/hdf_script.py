#!/usr/bin/python2.7


#### All Python Files Import
from merra.merra_mgr import *
from merra_db_operation.ExtractMerra import *
from merra_db_operation.merra_product import *
from merra_db_operation.MerraDataBase import *
from merra_db_operation.DBConfigFile import *

import os
from Canvas import Line


##### MERRA PRODUCTS Info handler 
Merra=Merra_Product()
Merra.ExtractingMerraProductsInfo()


##### MERRA Data Extraction handler
Extract = ExtractMerraFile() 

####DataBase Initialize
DB = MerraDatabase(DatabaseConfig['DataBaseName'],DatabaseConfig['Username'],DatabaseConfig['Password'],DatabaseConfig['hostIP'],DatabaseConfig['port'])
DB.DatabaseConnection()
tablename = DatabaseTablesName['FilesAdded']
## Table name should be in LowerCase only
tablename = tablename.lower()
flag = DB.check_If_Table_Exist(tablename)
### Handling needed to be check
if(flag == False):
    DB.CreateTableforFiles(tablename)


#### MERRA FTP HANDLER
mt = merra_tool(DB, Merra, Extract)

mt.download_process_hdf_data()



mt.disconnect()

#### End

