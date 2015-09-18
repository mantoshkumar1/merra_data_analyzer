#!/usr/bin/python2.7


#### All Python Files Import
from merra.merra_mgr import *
import ExtractMerra
import merra_product
import MerraDataBase

import os
from Canvas import Line
from datetime import datetime
import ConfigFile



##### MERRA PRODUCTS Info 
Merra=merra_product.Merra()
FileName="MerraProductsInfo.txt"
Merra.ExtractingMerraProductsInfo(FileName)

##### MERRA Data Extraction
Extract=ExtractMerra.ExtractMerraFile() 

####DataBase Initialize
DB=MerraDataBase.MerraDatabase(ConfigFile.DatabaseConfig['DataBaseName'],ConfigFile.DatabaseConfig['Username'],ConfigFile.DatabaseConfig['Password'],ConfigFile.DatabaseConfig['hostIP'],ConfigFile.DatabaseConfig['port'])
DB.DatabaseConnection()
tablename=ConfigFile.DatabaseTablesName['FilesAdded']
## Table name should be in LowerCase only
tablename=tablename.lower()
flag=DB.check_If_Table_Exist(tablename)
### Handling needed to be check
if(flag==False):
	DB.CreateTableforFiles(tablename)


#### MERRA FTP HANDLER
mt = merra_tool()

mt.download_process_hdf_data()


hdffilename=""
flag=DB.file_exist_in_db(hdffilename)
print "  File in DB Flag     :  "+str(flag)

### Say flag is False
if(flag==False):

    MerraProductName= Merra.ExtractMerraProductName(hdffilename)
    print " MerraProductName ", MerraProductName
    
    Attribute_list=len(Merra.MerraProductsInfo[MerraProductName]['AttributesList'])
    
    for counter in range(0,Attribute_list):
        
        AttributeName=Merra.MerraProductsInfo[MerraProductName]['AttributesList'][counter]
        Dim=Merra.MerraProductsInfo[MerraProductName]['DIMList'][counter]
        print " AttributeName  : ",AttributeName
        print " Dim    : ",Dim

        Extract.ConfigureMerraFiledetails(hdffile,AttributeName)
        Extract.HDFFileHandler()
        Extract.ExtractDataDimesions()
        
        ### For Loop o handle time 
        timeInterval=1
        Extract.ExtractData(timeInterval)
  
 
        ## Connection Setup 
        tablename=ConfigFile.DatabaseTablesName[MerraProductName]
        tablename=tablename+"_"+AttributeName
        ## Table name should be in LowerCase only
        tablename=tablename.lower()
        
        flag=DB.check_If_Table_Exist(tablename)
        
        ## If table does not exist than create it else append Data in existing Table
        if(flag==False):
            # Table Created
            DB.CreateSpatialTable(tablename,AttributeName)       
         
        time=datetime.now()
    
        counter=0
        for ht in range(0,Extract.height_len):
            if(counter >1000):
                break
            for lat in range(0,Extract.latitude_len):
                if(counter >1000):
                    break
                for lon in range(0,Extract.longitude_len):
                    value=Extract.data[ht][lat][lon]
                    print Extract.data[0][0][0]
                    Height=Extract.height_list[ht]
                    Lattitude=Extract.latitude_list[ht]
                    Longitude=Extract.longitude_list[ht]
                    unit=str(Extract.unit)
                    # Value Added
                    DB.AddSpatialData(tablename,time,Lattitude,Longitude,Height,value)
                    counter=counter+1
                    print " counter : ",counter
                    
                    
        print" Total Number of Elements Inserted : ",counter  
    
    
      
    










mt.disconnect()

DB.AddfilesnameinTable(hdffilename)   





#### End
DB.DatabaseClosed()

