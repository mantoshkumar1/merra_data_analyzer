# You can use this software for your purpose provided you include below two lines.
# This file is part of merra_data_analyzer, a high-level ftp-protocol big size recursive file downloader and merra file analyser.
# Copyright : Mantosh Kumar @ TUM, Germany


# importing system library package
import sys
import os
import ftplib
import socket
import logging
import time
import threading
from datetime import datetime


# importing merra tool modules
import cfg
from merra.merra_constants import *
from merra_db_operation.DBConfigFile import *

cfg = cfg.MEERA_ANALYZER_CFG

run_once = 1

# checking version of python
if sys.hexversion < 34014704:
    raise ImportError('Merra analyzer tool requires python version 2.7.5 or later')



def setInterval(interval, times = -1):
    """
    Function name : setInterval
    Description   : Set time interval for thread to display download status
        
    Parameters    : times (Integer, time interval for thread to be invoked)

    Return        :
    """

    # This will be the actual decorator, with fixed interval and times parameter
    def outer_wrap(function):
        # This will be the function to be called
        def wrap(*args, **kwargs):
            stop = threading.Event()
            # This is another function to be executed in a different thread to simulate setInterval
            def inner_wrap():
                i = 0
                while i != times and not stop.isSet():
                    stop.wait(interval)
                    function(*args, **kwargs)
                    i += 1


            t = threading.Timer(0, inner_wrap)
            t.daemon = True
            t.start()
            return stop

        return wrap

    return outer_wrap



class merra_tool:

    def __init__(self, DB, Merra, Extract, log):

        self.DB      =  DB
        self.Merra   =  Merra
        self.Extract =  Extract
        self.log     =  log
      
        if cfg[YOUR_LOCAL_HDFFILE_DIR_PATH] is not None:
            return
        
        if cfg.has_key(FTP_HOST_ADDR) and cfg.get(FTP_HOST_ADDR) is not None:
            self.host = cfg[FTP_HOST_ADDR]
        else:
            self.host = 'goldsmr2.sci.gsfc.nasa.gov' # '169.154.132.64' (Both are same. Ping this web addr, you will get ip addr)


        if cfg.has_key(MERRA_DATA_DOWNLOAD_DIR_PATH) and cfg.get(MERRA_DATA_DOWNLOAD_DIR_PATH) is not None:
            self.download_path = cfg[MERRA_DATA_DOWNLOAD_DIR_PATH]
        else:
            self.download_path = './merra_downloaded_data'


        if cfg.has_key(FTP_DEBUG_LEVEL) and cfg.get(FTP_DEBUG_LEVEL) is not None:
            self.FTP_DEBUG_LEVEL = cfg[FTP_DEBUG_LEVEL]
        else:
            self.FTP_DEBUG_LEVEL = 1


        # NASA asks for email address as password for downloading
        if cfg.has_key(USER_EMAIL_ADDR) and cfg.get(USER_EMAIL_ADDR) is not None:
            self.passwd = cfg[USER_EMAIL_ADDR]
        else:
            self.passwd = 'demo@tum.de'
        
        self.login = 'anonymous'

        
        self.directory    =  ''       # A temp variable - keeps current directory of the ftp server
        self.dir_list     =  [ ]      # List of sub directory
        self.hdffile_list =  [ ]      # List of HDF file


        # For managing file transfers
        self.monitor_interval = 2     # seconds (thread will notify the status of download after every THIS seconds)
        self.ptr = None               # Used to calculate size of downloaded file
        self.waiting = True           # Used for thread


        # If the connection dies, wait this long before reconnecting
        if cfg.has_key(RETRY_TIMEOUT) and cfg.get(RETRY_TIMEOUT) is not None:
            self.retry_timeout = cfg[RETRY_TIMEOUT]
        else:
            self.retry_timeout = 15


        # In case of download/connection failure, number of max tries to download/reconnection
        if cfg.has_key(MAX_ATTEMPTS_TO_DOWNLOAD) and cfg.get(MAX_ATTEMPTS_TO_DOWNLOAD) is not None:
            self.max_attempts = cfg[MAX_ATTEMPTS_TO_DOWNLOAD]
        else:
            self.max_attempts = 11
       
        # sets self.conn 
        self.connect()



    def connect(self): 
        """
        Function name : connect

        Description   : Connect to FTP server 
        
        Parameters    : 

        Return        :
        """

        try:
            self.conn = ftplib.FTP(self.host, self.login, self.passwd)

            # Switching to binary mode because 550 SIZE is not allowed in ASCII mode
            self.conn.sendcmd("TYPE i")
 

            # Optimize socket params for download task
            self.conn.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            self.conn.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 75)
            self.conn.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)


            self.conn.set_debuglevel(self.FTP_DEBUG_LEVEL)


            # Setting passive mode on
            self.conn.set_pasv(True)


        except ftplib.error_perm as err:

            print("Error: failed to connect with ftp {}".format(str(err)))
            self.log.write('\nError : failed to connect with ftp ' + str(err))
            return
      
 
        except:

            e = sys.exc_info()[0]
            print "Error: failed to connect with ftp - " + str(e)
            self.log.write('\nError : failed to connect with ftp - ' + str(e))
            return

        
        print '*** Connected to host "%s"' % self.host

        
        # Welcome message sent by the server
        global run_once
        if(run_once):
            self.directory = self.conn.pwd()
            print os.linesep #new line
            print self.conn.getwelcome()
            print os.linesep #new line
            run_once = 0
     


    def disconnect(self):
        """
        Function name : disconnect

        Description   : Close the connection politely
        
        Parameters    : 

        Return        :
        """

        # closing db connection
        self.DB.DatabaseClosed()


        if cfg[YOUR_LOCAL_HDFFILE_DIR_PATH] is not None:
            print "Wir danken fur . Auf Wiedersehen!"
            print "Thank you for using this application!"
            self.log.write('\nSuccess : program ends\n')
            return
        
        try:
            self.conn.quit()

        except (ftplib.error_reply, ftplib.error_proto):
            print "NASA ftp server will miss your company :( ... Anyway GoodBye!"
            print "Wir danken fur . Auf Wiedersehen!"

        except:
            print "NASA ftp server will miss your company :( ... Anyway GoodBye!"

        else:
            print "Thank you for using this application!"
            
        
        self.log.write('\nSuccess : Program ends\n')



    def move_to_dir(self, curr_dir = None):
        """
        Function name : move_to_dir

        Description   : Set the current directory on the server

        Parameters    : curr_dir (String, Desired directory name)

        Return        :
        """

        if curr_dir is None:
            curr_dir = self.directory


        try:

            self.conn.cwd(curr_dir)
            self.log.write('\nSuccess : dir moved to ' + str(curr_dir))


        except ftplib.error_perm as err:

            print "Error : cannot move dir to " + str(curr_dir) + " - " + str(err)
            self.log.write('\nError: cannot move dir to ' + str(curr_dir) + ' - ' + str(err))


        except:

            e = sys.exc_info()[0]
            print "Error : cannot move dir to " + str(curr_dir) + " - " + str(e)
            self.log.write('\nError: cannot move dir to ' + str(curr_dir) + ' - ' + str(e))
 
   
 
    def download_process_hdf_data(self):
        """
        Function name : download_process_hdf_data

        Description   : Driver function to crwal the server/local directory and/or invokes processing of hdf data

        Parameters    : 

        Return        :
        """

        if cfg[YOUR_LOCAL_HDFFILE_DIR_PATH] is not None:

            self.log.write('\nWorking on local hdf files')

            files_path_list = self.find_files_in_dir(cfg[YOUR_LOCAL_HDFFILE_DIR_PATH])
         
            for local_file in files_path_list:

                # Check whether you have permission to access this file or not and it exist or not, 
                #    - if yes then populate the DB (Never trust user, always check)
                if os.path.isfile(local_file) and os.access(local_file, os.R_OK):
                    base_name, f_name = os.path.split(local_file)

                    if(self.DB.file_exist_in_db(f_name)):
                        continue

                    # check tool capability to handle this kind of hdf data, if No then no need to process it
                    if(False == self.check_tool_hdf_capa(f_name)):
                    
                        print "************************************************************************************************"
                        print "Currently MERRA tool can't handle this kind of hdf data " + f_name
                        print "************************************************************************************************"
                        continue

                    self.process_hdf_file(local_file, f_name)

                else:
                    print "\n********************************************************************"
                    print local_file + " : not existing / read access permission denied"
                    self.log.write('\nError : ' + str(local_file) +  ' : not existing / read access permission denied')
                    print "********************************************************************\n"

            return
                

        self.log.write('\nWorking on remote ftp server')

        for home_dir in cfg[FTP_HOME_DIR]:
            self.crwal_all_dir(home_dir)



    def crwal_all_dir(self, dir_name):
        """
        Function name : crwal_all_dir

        Description   : Recursive function - Crwal throughout ftp server

        Parameters    : dir_name (String, name of dir where further crawling will be done)

        Return        :
        """

        new_dirs = []

        try:

            self.directory = self.conn.pwd()

        except AttributeError as err:

            print("Error: {}".format(str(err)))
            self.log.write('\nError : ' + str(err))
            self.shutdown()

        except:

            e = sys.exc_info()[0]
            print e
            self.log.write('\nError : Some error occured in crwal_all_dir function - ' + str(e))
            self.shutdown()

 
        if self.isdir(dir_name):
            print("Changing directory from " + self.directory + " to " + dir_name)
            self.move_to_dir(dir_name)


            self.directory = self.conn.pwd()
            print("Current directory: " + self.directory)
            self.log.write("\nCurrent directory: " + str(self.directory))

 
            # listing all files/subdir inside this directoty
            new_dirs = self.retrive_file_list()
            self.organise_dir_files(new_dirs)

             
            print("Number of HDF files inside " + dir_name + " = " + str(len(self.hdffile_list)))
            self.log.write('\nNumber of HDF files inside ' + str(dir_name) + ' = ' + str(len(self.hdffile_list)))
           
 
            # Now download hdf files stored in self.hdffile_list
            for hdf_file in self.hdffile_list:

                # check if this hdf_file already exists in db, if yes do not download
                if(True == self.DB.file_exist_in_db(hdf_file)):
                    continue
                   
              
                # check tool capability to handle this kind of hdf data, if No then no need to download any hdf frm this dir 
                if(False == self.check_tool_hdf_capa(hdf_file)):
                    
                    print "************************************************************************************************"
                    print "Currently MERRA tool can't handle this kind of hdf data " + hdf_file
                    print "************************************************************************************************"
                    break


                print "\n" + "Downloading starts for : " + hdf_file
                self.log.write('\nDownloading starts for : ' + str(hdf_file))
                print "************************************************************************"
                if(self.download_file(hdf_file)):
                #if 0:
                    dwnlded_hdf_full_path = os.path.join(self.download_path, hdf_file)
                    self.process_hdf_file(dwnlded_hdf_full_path, hdf_file)
 
                    # Once DB is populated, you can delete the downloaded file
                    if cfg[SAVE_DOWNLOADING_DATA] is False:
                        self.delete_file(hdf_file)
                        print 'file {} is deleted as per user instruction.'.format(hdf_file)



            self.hdffile_list = [ ]


            new_dirs = self.dir_list
            for sub_dir in new_dirs:
                self.dir_list = [ ]
                self.crwal_all_dir(sub_dir) # recursive function call 


            self.move_to_dir('..') # come back to own directory when done


    
    def organise_dir_files(self, files):
        """
        Function name : organise_dir_files

        Description   : Store directories name and HDF file name in dir_list and gdffile_list respectively

        Parameters    : files (List, Names of HDF files and/or sub directories which are strings)

        Return        :
        """

        for entry in files:
            if self.isdir(entry):
                 self.dir_list.append(entry)

            elif entry.endswith(cfg[PROCESSING_FILE_TYPE]):
                 self.hdffile_list.append(entry) # full path


                 
    def retrive_file_list(self):
        """
        Function name : retrive_file_list

        Description   : Find all the files/subdirs inside current directoty

        Parameters    : 

        Return        : List of Strings (List of subdir/file names)
        """

        files = []
        try:
            files = self.conn.nlst()

        except ftplib.error_perm, resp:
            if str(resp) == "550 No files found":
                print "No files in this directory"
                pass # files remains []

        except:
            e = sys.exc_info()[0]
            self.log.write('\nError : ' + str(e))
            pass # files remains []
            

        return files

            

    def isdir(self, dir_name):
        """ 
        Function name : isdir

        Description   : Checks whether given subdir in current dir over the FTP server is a directory or not

        Parameters    : dir_name (String, Name of a directory)

        Return        : If dir_nam is a directory, returns True
                        else return False
        """

        try:

            prev_path = self.conn.pwd()
            self.conn.cwd(dir_name)
            self.conn.cwd(prev_path)
            return True


        except ftplib.all_errors:

            return False

        except:

            e = sys.exc_info()[0]
            print "Error : " + str(e)
            self.log.write('\nError : some error occured in isdir function ' + str(e))
            raise



    def download_file(self, file_name):
        """
        Function name: download_file

        Description : This method downloads the file from FTP server, tries to re-establish a broken connection, \
                      resumes the file transfer where it left off and shows the download progress

        Parameter   : file_name (String, Name of downloading HDF file)

        Return      : In case of successful download: True
                      In case of failure : False
        """
    
        num_attempts = self.max_attempts

        self.make_sure_path_exists(self.download_path)

        with open(os.path.join(self.download_path, file_name), 'w') as f:
            self.ptr = f.tell()

            # switching to binary mode because 550 SIZE is not allowed in ASCII mode
            self.conn.sendcmd("TYPE i")

            remote_filesize = self.conn.size(file_name)

            @setInterval(self.monitor_interval)
            def monitor():
                if not self.waiting and not f.closed:
                    i = f.tell()
                    if self.ptr < i:
                        logging.debug("%d - %0.1f Kb/s" % (i, (i-self.ptr)/(1024*self.monitor_interval)))
                        print "Downloading status: %d / %d bits  -  %0.1f Kb/s" % (i, remote_filesize, \
                                                                              (i-self.ptr)/(1024*self.monitor_interval))
                        self.ptr = i

            
            res = ''

            mon = monitor()
            while remote_filesize > f.tell():
                print "\n" + file_name + ": Downloading in progress ........"
                try:
                    self.connect()
                    self.move_to_dir()
                    self.waiting = False
                    # Retrieve file from the position where we were disconnected
                    if f.tell() == 0:
                        res = self.conn.retrbinary('RETR %s' % file_name, f.write)
                    else:
                        res = self.conn.retrbinary('RETR %s' % file_name, f.write, rest=f.tell())

                except:
                    num_attempts -= 1
                    if num_attempts == 0:
                        mon.set()
                        self.delete_file(file_name)
                        #logging.exception('')
                        self.shutdown()


                    self.waiting = True
                    logging.info('waiting {} sec...'.format(self.retry_timeout))
                    print 'waiting {} sec...'.format(self.retry_timeout)
                    time.sleep(self.retry_timeout)
                    logging.info('reconnect')
                    print 'reconnecting'
                    self.log.write('\nReconnecting while downloading ' + str(file_name))


            #stop monitor
            mon.set()


            if not res.startswith('226 Transfer complete'):
                logging.error('Downloading of file {0} failed.'.format(file_name))
                print 'Downloading of file {0} failed.'.format(file_name)
                self.log.write('\nError : Downloading of file ' + str(file_name) + ' failed')
                self.delete_file(file_name)
                return False

            else:
                logging.info('File {} successfully downloaded.'.format(file_name))
                print 'File {} successfully downloaded.'.format(file_name)
                self.log.write('\nSuccess : ' + str(file_name) + ' downloaded')

            return True



    def delete_file(self, file_name):
        """ 
        Function name : delete_file

        Description   : Delete local file on system

        Parameters    : file_name (String, name of file)
        
        Return        : 

        """
         
        file_full_path = os.path.join(self.download_path, file_name)

        try:

            os.remove(file_full_path)
            self.log.write('\nSuccess : ' + str(file_name) + ' deleted')


        except:

            e = sys.exc_info()[0]
            self.log.write('\nError : ' + str(e))



    def shutdown(self):
        """ 
        Function name : shutdown

        Description   : Terminates program forcefully

        Parameters    : 
        
        Return        : 

        """

        print "\n***************************************************"           
        print "Internet / FTP server down"
        print "Program Terminating"
        self.log.write('\nError : internet / ftp server down - program terminating\n')
        print "***************************************************\n"          

        try: 
            self.conn.close()
        except:
            pass
        
        raise SystemExit()



    def make_sure_path_exists(self, path):
        """ 
        Function name : make_sure_path_exists

        Description   : Create the directory, but if it already exists we ignore the error. 

        Parameters    : dir_path [String, Relative/Absolute Path of a directory) ]
        
        Return        : 

        """

        try:
            os.makedirs(path)

        except OSError as exception:
            pass

        except:
            pass



    def find_files_in_dir(self, dir_path):
        """ 
        Function name : find_files_in_dir

        Description   : Find all the HDF files stored inside given directory and its subdirectories

        Parameters    : dir_path [String, Relative/Absolute Path of parent directory inside which you want to search HDF files) ]
        
        Return        : List of strings(paths of HDF files)

        """

        files_path_list = [ ]

        if(False == os.path.isdir(dir_path)):
            print "\n********************************************************************"
            print "Directory " + dir_path + " doesn't exist\n"
            print "Set correct path in  YOUR_LOCAL_HDFFILE_DIR_PATH in cfg.py"
            self.log.write('\nError : dir ' + str(dir_path) + ' does not exist, set correct local hdf files dir path in cfg.py')
            print "********************************************************************\n"
            return files_path_list


        for dirpath, dirnames, filenames in os.walk(dir_path):
            for filename in [f for f in filenames if f.endswith(cfg[PROCESSING_FILE_TYPE])]:
                files_path_list.append(os.path.join(dirpath, filename))


        if not files_path_list: # empty list
            print "\n********************************************************************"
            print "There is no HDF file inside " + dir_path + " directory"
            self.log.write('\nWarning : No hdf files inside ' + str(dir_path) + ' directory')
            print "********************************************************************\n"


        return files_path_list



    def process_hdf_file(self, full_path, file_name):
        """ 
        Function name : process_hdf_file

        Description   : This is a bridge function between web crawl and DB functions. 
                        This function sends file to DB function for extraction and processing and populating Merra DB.

                        This function needs full_path and name of the downloaded hdf file.


        Parameters    : full_path: (String, Relative/Absolute full path of the hdf file)
                        file_name: (String, Name of hdf file)

        Return        : 

        """

	hdffile = full_path 
	hdffilename = file_name


        MerraProductName = self.Merra.ExtractMerraProductName(hdffilename)
        print "MerraProductName : ", MerraProductName


        Attribute_list = len(self.Merra.MerraProductsInfo[MerraProductName]['AttributesList'])
    
        for counter in range(0,Attribute_list):
        
            AttributeName = self.Merra.MerraProductsInfo[MerraProductName]['AttributesList'][counter]
            Dim = self.Merra.MerraProductsInfo[MerraProductName]['DIMList'][counter]
            print "AttributeName  : ",AttributeName
            print "Dim    : ",Dim

            self.Extract.ConfigureMerraFiledetails(hdffile,AttributeName)
            self.Extract.HDFFileHandler()
            self.Extract.ExtractDataDimesions()
        
            ### For Loop o handle time 
            timeInterval = 1
            self.Extract.ExtractData(timeInterval)
  
 
            ## Connection Setup 
            tablename = DatabaseTablesName[MerraProductName]
            tablename = tablename + "_" + AttributeName
            ## Table name should be in LowerCase only
            tablename = tablename.lower()
        
            flag = self.DB.check_If_Table_Exist(tablename)
        
            ## If table does not exist than create it else append Data in existing Table
            if(flag == False):
                # Table Created
                self.DB.CreateSpatialTable(tablename,AttributeName)       
        
 
            time = datetime.now()
    
            counter = 0
            for ht in range(0,self.Extract.height_len):
                # need improvement
                if(counter > 1000):
                    break
                for lat in range(0,self.Extract.latitude_len):
                    if(counter > 1000):
                        break
                    for lon in range(0,self.Extract.longitude_len):
                         value     = self.Extract.data[ht][lat][lon]
                         Height    = self.Extract.height_list[ht]
                         Lattitude = self.Extract.latitude_list[ht]
                         Longitude = self.Extract.longitude_list[ht]
                         unit      = str(self.Extract.unit)

                         # Value Added
                         self.DB.AddSpatialData(tablename,time,Lattitude,Longitude,Height,value)
                         counter = counter + 1
                         print " counter : ",counter
                    
                    
            print" Total Number of Elements Inserted : ",counter

        # adding downloaded hdf file name in DB 
        self.DB.AddfilesnameinTable(hdffilename)   
    

    def check_tool_hdf_capa(self, hdffilename):
        """ 
        Function name : check_tool_hdf_capa

        Description   :  Checks whether this tool can handle this type of hdf data or not.
                         This function needs name of the downloading file.


        Parameters    : hdffilename (String : Name of hdf file)

        Return        : if it can handle this kind of hdf data then return True else return False

        """


        capa = True

        try:

            MerraProductName = self.Merra.ExtractMerraProductName(hdffilename)
            Attribute_list = len(self.Merra.MerraProductsInfo[MerraProductName]['AttributesList'])

        except:

            capa = False
            self.log.write('\nError : HDF format not supported ' + str(hdffilename))

        
        return capa
   

  
