# You can use this software for your purpose provided you include below two lines.
# This file is part of merra_data_analyzer, a high-level ftp-protocol big size recursive file downloader and merra file analyser.
# Copyright : Mantosh / Gaurav  @ TUM, Germany

import os

## Merra_Product class manages all the Info about merra products

class Merra_Product:

    def __init__(self, log):
        """
        Function name : __init__
        
        Description   : Initialize Merra Class
            
        Parameters    : None
    
        Return        : None
        """  
    
        self.MerraProductsInfo = { }
        self.log = log

        # setting MerraProductsInfo
        self.ExtractingMerraProductsInfo()

        print "MERRA Class initialized"


        import time 
        now = time.strftime("%c") 
        self.log.write('\n\n')
        self.log.write("\nExecution time : %s" % now)
        self.log.write("\n=======================================================================================")
        self.log.write('\nMERRA class initialized')



    def ExtractingMerraProductsInfo(self):
        """
        Function name : ExtractingMerraProductsInfo
        
        Description   : Creating an Dictionary MerraProductsInfo that contains all Merra Products .
            
        Parameters    : None
    
        Return        : None
        """

        TextFileName = os.getcwd() + "/merra_db_operation/MerraProductsInfo.txt"
        self.file = open(TextFileName, 'r')

        self.lines = self.file.readlines() # will append in the list out

        for line in self.lines:

            if not line.startswith("//") and not line.startswith("  "):

                Fileinfo = line.split("##")
                print Fileinfo[0]


                FilesDescriptionsplit = Fileinfo[0].split("::::")
                print FilesDescriptionsplit


                Filename = FilesDescriptionsplit[0]
                timeinterval = FilesDescriptionsplit[1]
                Description = FilesDescriptionsplit[2]


                self.MerraProductsInfo[Filename] = { }
                timeinterval = timeinterval.split(",")
                self.MerraProductsInfo[Filename]['timeintervallist'] = timeinterval
                self.MerraProductsInfo[Filename]['Description'] = Description

    
                AttributesInfo = Fileinfo[1]
                AttributesList = AttributesInfo.split(",")
                self.MerraProductsInfo[Filename]['AttributesList'] = [ ]
                self.MerraProductsInfo[Filename]['DIMList'] = [ ]


                for Attinfo in AttributesList:
                    Attribute = Attinfo.split("::::")[0]
                    dimesion = Attinfo.split("::::")[1]

                    self.MerraProductsInfo[Filename]['AttributesList'].append(Attribute)
                    self.MerraProductsInfo[Filename]['DIMList'].append(dimesion)

                 
        print "self.MerraProductsInfo : ",self.MerraProductsInfo     

   

      
    def ExtractMerraProductDate(self,filename):
        """
        Function name : ExtractMerraProductDate
        
        Description   : Extract Merraproduct date of creation.            
       
        Parameters    : filename (String)
    
        Return        : None
        """         

        self.datestring = filename.split(".")[4]
        Year = self.datestring[0:4]
        month = self.datestring[4:6]
        Day = self.datestring[6:8]
        
        self.date = month + "/" + month + "/" + Year
        return self.date



    def ExtractMerraProductName(self,filename):
        """
        Function name : ExtractMerraProductName
        
        Description   : Extract MerraProduct name from filename.            
       
        Parameters    : filename (String)
    
        Return        : None
        """        
 
        self.MerraProductName = filename.split(".")[3]
        return self.MerraProductName
            
