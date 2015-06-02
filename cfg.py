from merra.merra_constants import *

MEERA_ANALYZER_CFG = {
                         HOST_ADDR : "169.154.132.64", # goldsmr3.sci.gsfc.nasa.gov
                         DIR_NAME  : "data/s4pa/MERRA_MONTHLY/MATMNXFLX.5.2.0/2015",    #Scope of improvement
                         FILE_NAME : "*.hdf",
                         MERRA_DATA_DOWNLOAD_PATH  : './merra_downloaded_data',

                         DELETE_DOWNLOADED_DATA : True, # False if you want to keep
                         
}

