import ExtractMerra
import MerraDataBase
import os
from Canvas import Line
from datetime import datetime



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




    Merra=Merra()
    FileName="MerraProductsInfo.txt"
    Merra.ExtractingMerraProductsInfo(FileName)

    raw_input("Press enter to continue ")
    
    ####### Extract Data  from MERRA file  ###########################
    # If a certain environment variable is set, look there for the input
    # file, otherwise look in the current directory.
 
    hdffilename='MERRA300.prod.assim.inst3_3d_chm_Ne.20021201.hdf'
    try:
        hdffile = os.path.join(os.environ['HDFEOS_ZOO_DIR'], hdffilename)
    except KeyError:
        hdffile=hdffilename
        pass
 
    Extract=ExtractMerra.ExtractMerraFile()
    
    MerraProductName= Merra.ExtractMerraProductName(hdffilename)
    print " MerraProductName ", MerraProductName
    
    raw_input("Press enter to continue ")
    
    Attri=Merra.MerraProductsInfo[MerraProductName]['AttributesList'][0]
    Dim=Merra.MerraProductsInfo[MerraProductName]['DIMList'][0]
    print " Attri  : ",Attri
    print " Dim    : ",Dim
    raw_input("Press enter to continue ")
    
    
        
    Attribute=Attri
    Extract.ConfigureMerraFiledetails(hdffile,Attribute)
    Extract.HDFFileHandler()
    Extract.ExtractDataDimesions()
    timeInterval=7
    Extract.ExtractData(timeInterval)
 
     
    raw_input("Press enter to continue Merra Data extracted ")
     
 ################### DataBase Connection SetUP AND Loading Data in DataBase #####################

    ## Connection Setup 
     
    hostIP="127.0.0.1"
    DB=MerraDataBase.MerraDatabase('merra','postgres','gnusmas',hostIP,"5432")
    DB.DatabaseConnection()
    
    tablename="MerraDatabase"
    AttributeName=Attribute
    DB.DropTable("MerraDatabase")
    
 
    # Table Created
    DB.CreateSpatialTable(tablename,AttributeName)
    time=datetime.now()

    counter=0
    for ht in range(Extract.height_len):
        if(counter >1000):
            break
        for lat in range(Extract.latitude_len):
            if(counter >1000):
                break
            for lon in range(Extract.longitude_len):
                value=Extract.data[ht][lat][lon]
                Height=Extract.height_list[ht]
                Lattitude=Extract.latitude_list[ht]
                Longitude=Extract.longitude_list[ht]
                unit=str(Extract.unit)
                # Value Added
                DB.AddSpatialData(tablename,time,Lattitude,Longitude,Height,value,unit)
                counter=counter+1
                print " counter : ",counter
                
                
    print" Total Number of Elements Inserted : ",counter           
    
    DB.DatabaseClosed()
   
   
    
