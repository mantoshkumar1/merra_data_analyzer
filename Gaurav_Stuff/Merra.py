import ExtractMerra
import MerraDataBase
import os
from Canvas import Line
from datetime import datetime
import ConfigFile


### Merra class is the Master Class that manages all the SUB classes objects to do various Task :
##   -  Fetching MERRA files from FTP server(TBD) 
##   -  Extracting MERRA data from downloaded MERRA files (ExtractMerraFile Class)
##   -  Managing MERRA database(MerraDatabase class)


class Merra:
    
    ### Initialize Merra Class
    def __init__(self):
        print " Initialize MERRA Class "
        self.MerraProductsInfo={}

    ## Creating an Dictionary MerraProductsInfo that contains all Merra Products Info Like
    ## Info about all attributes in an merra file
    ## Dimension of the attribute whether 2D or 3D
    def ExtractingMerraProductsInfo(self,TextFilename):
        self.file = open(TextFilename,'r')
        self.lines = self.file.readlines() # will append in the list out
        for line in self.lines:
            if not line.startswith("//") and not line.startswith("  "):
                Fileinfo=line.split("##")
                Filename=Fileinfo[0].split(":")[0]
                Description=Fileinfo[0].split(":")[1]
                self.MerraProductsInfo[Filename]={}
                self.MerraProductsInfo[Filename]['Description']=Description
    
                AttributesInfo=Fileinfo[1]
                AttributesList=AttributesInfo.split(",")
                self.MerraProductsInfo[Filename]['AttributesList']=[]
                self.MerraProductsInfo[Filename]['DIMList']=[]
                for Attinfo in AttributesList:
                    Attribute=Attinfo.split(":")[0]
                    dimesion=Attinfo.split(":")[1]
                    self.MerraProductsInfo[Filename]['AttributesList'].append(Attribute)
                    self.MerraProductsInfo[Filename]['DIMList'].append(dimesion)
                 
        print "self.MerraProductsInfo : ",self.MerraProductsInfo        

    def ExtractMerraProductName(self,filename):
        self.MerraProductName=filename.split(".")[3]
        return self.MerraProductName
      
      
if __name__ == "__main__":


### Initilaize the Master Class Constructor
    Merra=Merra()


##### Reading MERRA PRODUCTS info 
## Needed to be called Just Once
    FileName="MerraProductsInfo.txt"
    Merra.ExtractingMerraProductsInfo(FileName)

    raw_input("Press enter to continue ")
    
    ####### Extract Data  from MERRA file  ###########################
    # If a certain environment variable is set, look there for the input
    # file, otherwise look in the current directory.
 
    hdffilename='MERRA300.prod.assim.tavg3_3d_tdt_Cp.20150101.hdf'
    try:
        hdffile = os.path.join(os.environ['HDFEOS_ZOO_DIR'], hdffilename)
    except KeyError:
        hdffile=hdffilename
        pass
    
    DB=MerraDataBase.MerraDatabase(ConfigFile.DatabaseConfig['DataBaseName'],ConfigFile.DatabaseConfig['Username'],ConfigFile.DatabaseConfig['Password'],ConfigFile.DatabaseConfig['hostIP'],ConfigFile.DatabaseConfig['port'])
    DB.DatabaseConnection()
    
    tablename=ConfigFile.DatabaseTablesName['FilesAdded']
    ## Table name should be in LowerCase only
    tablename=tablename.lower()
    
    flag=DB.check_If_Table_Exist(tablename)
    
    ### Handling needed to be check
    if(flag==True):
        DB.DropTable(tablename)
    DB.CreateTableforFiles(tablename)

    flag=DB.file_exist_in_db(hdffilename)
    print "  File in DB Flag     :  "+str(flag)
    
    
 

    
    MerraProductName= Merra.ExtractMerraProductName(hdffilename)
    print " MerraProductName ", MerraProductName
    
    Attribute_list=len(Merra.MerraProductsInfo[MerraProductName]['AttributesList'])
    
    for counter in range(0,Attribute_list):

        Extract=ExtractMerra.ExtractMerraFile()
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
  
     ################### DataBase Connection SetUP AND Loading Data in DataBase #####################
    
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
    
    
    DB.AddfilesnameinTable(hdffilename)         
    
    DB.DatabaseClosed()
   
   
    
