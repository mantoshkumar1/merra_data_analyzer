import os


### Merra class is the Master Class that manages all the SUB classes objects to do various Task :
##   -  Fetching MERRA files from FTP server(TBD) 
##   -  Extracting MERRA data from downloaded MERRA files (ExtractMerraFile Class)
##   -  Managing MERRA database(MerraDatabase class)


class Merra_Product:
    
    ### Initialize Merra Class
    def __init__(self):
        print " Initialize MERRA Class "
        self.MerraProductsInfo={}

    ## Creating an Dictionary MerraProductsInfo that contains all Merra Products Info Like
    ## Info about all attributes in an merra file
    ## Dimension of the attribute whether 2D or 3D
    def ExtractingMerraProductsInfo(self):

        TextFileName = os.getcwd() + "/merra_db_operation/MerraProductsInfo.txt"
        self.file = open(TextFileName, 'r')

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
      
      
    
