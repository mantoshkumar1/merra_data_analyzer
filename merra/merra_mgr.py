import sys
import os
import cfg
from merra.merra_constants import *

cfg = cfg.MEERA_ANALYZER_CFG

class merra_tool:

    def __init__(self):

        self.download_path = cfg[MERRA_DATA_DOWNLOAD_PATH]

    def download_data(self):    #downlink data from ftp server
       
        import ftplib 
        from ftplib import FTP, error_perm
        import socket

        try:
            ftp = FTP(cfg[HOST_ADDR]) #hostname
        except (socket.error, socket.gaierror), e:
            print 'ERROR: cannot reach "%s"' % cfg[HOST_ADDR]
            return
        print '*** Connected to host "%s"' % cfg[HOST_ADDR]
        
        try:
            ftp.login()
        except ftplib.error_perm:
            print 'ERROR: cannot login anonymously : authentication denied'
            ftp.quit()
            return
        print '*** Logged in as "anonymous"'
        
        # Return the welcome message sent by the server in reply to the initial connection
        print os.linesep #new line
        print ftp.getwelcome()
        print os.linesep #new line


        try:  #moving to directory where desired file is stored over ftp server
            ftp.cwd(cfg[DIR_NAME])
        except ftplib.error_perm:
            print 'ERROR: cannot CD to "%s"' % cfg[DIR_NAME]
            ftp.quit()
            return
        

        print '*** Downloading of HDF files starts now'        
        dwnld_dir = cfg[MERRA_DATA_DOWNLOAD_PATH]

        # Loop through matching files and download each one individually
        for fl in ftp.nlst(cfg[FILE_NAME]):
            # create a full local filepath
            try: #getting binary file from ftp server
                #gFile = open(fl, 'wb')
                gFile = open(os.path.join(dwnld_dir, fl), 'w')
                ftp.retrbinary('RETR %s' % fl, gFile.write)
            except ftplib.error_perm:
                print 'ERROR: cannot read file "%s"' % fl
                os.unlink(fl)
                gFile.close()
            else:
                print '*** %s is downloaded' % fl
                gFile.close()
        else:
            print os.linesep #new line
            print '*** Downloading sucessfully finished' 
            print '*** HDF files are downloaded at "%s""' % cfg[MERRA_DATA_DOWNLOAD_PATH]


        #closing connection
        ftp.quit()

       
       
    '''
    def read_hdf4_file():
        from pyhdf import SD
        FILE_NAME="my_file.hdf" # The hdf file to read
        SDS_NAME="my_sds" # The name of the sds to read
        X_LENGTH=5
        Y_LENGTH=16

        # open the hdf file for reading
        hdf=SD.SD(FILE_NAME)
        # read the sds data
        sds=hdf.select(SDS_NAME)
        data=sds.get()
        # turn [y,x] (HDF representation) data into [x,y] (numpy one)
        data=data.reshape(data.shape[1],data.shape[0])
        # print out the data
        msg_out=""
        for i in range(X_LENGTH):
            for j in range(Y_LENGTH):
                msg_out+=str(data[i,j])+" "
            msg_out+="\n"
        print msg_out
    '''

