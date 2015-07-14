import os

import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
from pyhdf.SD import SD, SDC
    
class ExtractMerraFile:
    
    ### Initialize Database Configuration
    def __init__(self):
        print " ExtractMerraFile Init "
        
    def ConfigureMerraFiledetails(self,hdffile,variablename): 
        self.hdffile=hdffile
        self.variablename=variablename           
        
    def HDFFileHandler(self):    
        self.hdf = SD(self.hdffile, SDC.READ)
        print " hdf  ",self.hdf
        
        
    def ExtractDataDimesions(self):
            
        # Xdim is Lognitude
        lon = self.hdf.select('XDim')
        self.longitude_list = lon[:]
        self.longitude_len=len(self.longitude_list)
        print "longitude_list : ",self.longitude_list
        print "longitude_len : ",self.longitude_len

        # Ydim is Lattitude
        lat = self.hdf.select('YDim')
        self.latitude_list = lat[:]
        self.latitude_len=len(self.latitude_list)
        print "latitude_list : ",self.latitude_list
        print "latitude_len : ",self.latitude_len
        
        ht = self.hdf.select('Height')
        self.height_list = ht[:]
        self.height_len=len(self.height_list)
        print "height_list : ",self.height_list
        print "height_len : ",self.height_len
        

        t = self.hdf.select('Time')
        self.time_list = t[:]
        self.time_len=len(self.time_list)
        print "time_list : ",self.time_list
        print "time_len : ",self.time_len
        
      

    def ExtractData(self,timeInterval):
        # Read dataset.
        self.data4D = self.hdf.select(self.variablename)
        # TIME : HEIGHT(Altitude) : YDIM(Latitude, in degrees north) : XDIM(Longitude, in degrees east)
        self.data = np.array(self.data4D[timeInterval,:,:,:]).astype(np.float64)
 
        print " self.data ",self.data
 
        print " Height Len (Datam)",len(self.data) 
        print " YDIM   Len (Datam[0]",len(self.data[0]) 
        print " XDIM   Len (Datam[0][0])",len(self.data[0][0]) 
 
        # Retrieve the attributes.
        attrs = self.data4D.attributes(full=1)
        #print " Attributes  :  ",attrs
        mva=attrs["missing_value"]
        #print " mva   : ",mva
        missing_value = mva[0]
        #print " missing_value   : ",missing_value
        lna=attrs["long_name"]
        #print " lna   : ",lna
        long_name = lna[0]
        ua=attrs["units"]
        #print " ua       : ",ua
        self.unit = ua[0] 
        #print " units    : ",units       

        # Replace the missing values with NaN.        
        self.data[self.data == missing_value] = np.nan
        self.datam = np.ma.masked_array(self.data, np.isnan(self.data))
        
if __name__ == "__main__":

    hdffile='MERRA300.prod.assim.inst3_3d_chm_Ne.20021201.hdf'
    try:
        hdffile = os.path.join(os.environ['HDFEOS_ZOO_DIR'], hdffile)
    except KeyError:
        pass

    Extract=ExtractMerraFile()
    
    variablename='PLE'
    Extract.ConfigureMerraFiledetails(hdffile,variablename)
    Extract.HDFFileHandler()
    Extract.ExtractDataDimesions()
    Extract.ExtractData(0)


    # If a certain environment variable is set, look there for the input
    # file, otherwise look in the current directory.
    #hdffile = 'MERRA300.prod.assim.tavg3_3d_chm_Ne.20150401.hdf'
    #try:
    #    hdffile = os.path.join(os.environ['HDFEOS_ZOO_DIR'], hdffile)
    #except KeyError:
    #    pass
    #

    #Extract=ExtractMerraFile()
    
  
    #variablename='MFZ'
    #Extract.ConfigureMerraFiledetails(hdffile,variablename)
    #Extract.run()
    
    #variablename='CMFMC'
    #Extract.ConfigureMerraFiledetails(hdffile,variablename)
    #Extract.run()
        
    
    #variablename='KH'
    #Extract.ConfigureMerraFiledetails(hdffile,variablename)
    #Extract.run()
    
    