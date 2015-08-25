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


# importing merra tool modules
import cfg
from merra.merra_constants import *

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

    def __init__(self):

        if cfg[YOUR_DOWNLOADED_HDFFILE_DIR_PATH] is not None:
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
            print("Error: {}".format(str(err)))
            return
      
 
        except:
            print ("An error occured")
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

        if cfg[YOUR_DOWNLOADED_HDFFILE_DIR_PATH] is not None:
            print "Wir danken fur . Auf Wiedersehen!"
            print "Thank you for using this application!"
            return
        
        try:
            self.conn.quit()

        except (ftplib.error_reply, ftplib.error_proto):
            print "NASA ftp server will miss your company :( ... Anyway GoodBye!"
            print "Wir danken fur . Auf Wiedersehen!"

        except:
            print "NASA ftp server will miss your company :( ... Anyway GoodBye!"


    def move_to_dir(self, curr_dir = None):
        """
        Function name : move_to_dir

        Description   : Set the current directory on the server

        Parameters    : curr_dir (String, Desired directory name)

        Return        :
        """

        try:
            if(curr_dir is not None):
                self.conn.cwd(curr_dir)

            else:
                self.conn.cwd(self.directory)

      
        except ftplib.error_perm:
            print 'Error: cannot move to "%s"' % curr_dir
            

        except:
            print 'Some error occured'
 
    
    def download_hdf_data(self):
        """
        Function name : crwal_server

        Description   : Driver function to crwal the server and download

        Parameters    : 

        Return        :
        """

        if cfg[YOUR_DOWNLOADED_HDFFILE_DIR_PATH] is not None:

            files_path_list = self.find_files_in_dir(cfg[YOUR_DOWNLOADED_HDFFILE_DIR_PATH])
         
            for local_file in files_path_list:

                # Check whether you have permission to access this file or not and it exist or not, if yes then populate the DB
                if os.path.isfile(local_file) and os.access(local_file, os.R_OK):
                    self.process_hdf_file(local_file)

            return
                

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
        self.directory = self.conn.pwd()
        
        if self.isdir(dir_name):
            print("Changing directory from " + self.directory + " to " + dir_name)
            self.move_to_dir(dir_name)


            self.directory = self.conn.pwd()
            print("Current directory: " + self.directory)

 
            # listing all files/subdir inside this directoty
            new_dirs = self.retrive_file_list()
            self.organise_dir_files(new_dirs)

             
            print("Total HDF files found so far inside " + dir_name + ": " + str(len(self.hdffile_list)))
           
 
            # download hdf files stored in self.hdffile_list
            for hdf_file in self.hdffile_list:
                if(self.file_exist_in_db(hdf_file)):
                    print "\n" + hdf_file + " data is already available in MERRA DB"
                    continue
                    
                    
                print "\n" + "downloading starts for : " + hdf_file
                print "************************************************************************"
                #if(self.download_file(hdf_file)):
                if 0:
                    dwnlded_hdf_full_path = os.path.join(self.download_path, hdf_file)
                    self.process_hdf_file(dwnlded_hdf_full_path, hdf_file)
 
                    # Once DB is populated, you can delete the downloaded file
                    if cfg[SAVE_DOWNLOADED_DATA] is False:
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
            print "Some error occured"
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
            print "Some error occured"
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


            #stop monitor
            mon.set()


            if not res.startswith('226 Transfer complete'):
                logging.error('Downloading of file {0} failed.'.format(file_name))
                print 'Downloading of file {0} failed.'.format(file_name)
                self.delete_file(file_name)
                return False

            else:
                logging.info('File {} successfully downloaded.'.format(file_name))
                print 'File {} successfully downloaded.'.format(file_name)

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
        except OSError:
            pass
        except:
            pass



    def shutdown(self):
        """ 
        Function name : shutdown

        Description   : Terminates program forcefully

        Parameters    : 
        
        Return        : 

        """

        print "***************************************************"           
        print "Internet / FTP server down"
        print "Program Terminating"
        print "***************************************************"          

        try: 
            self.conn.close()
            sys.exit(0)
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
            print "Set correct path in  YOUR_DOWNLOADED_HDFFILE_DIR_PATH in cfg.py"
            print "********************************************************************\n"
            return files_path_list


        for dirpath, dirnames, filenames in os.walk(dir_path):
            for filename in [f for f in filenames if f.endswith(cfg[PROCESSING_FILE_TYPE])]:
                files_path_list.append(os.path.join(dirpath, filename))


        if not files_path_list: # empty list
            print "There is no HDF file inside " + dir_path + " directory"


        return files_path_list



    def process_hdf_file(self, full_path, file_name = None):
        """ 
        Function name : process_hdf_file

        Description   : This is a bridge function between web crawl and DB functions. 
                        This function sends file to DB function for extraction and processing and populating Merra DB.

                        Scenario 1: If user has specified an locally downloaded HDF file, then this function \
                        doesn't need file_name (= None) and obviously this file_name (= None) will not be updated \
                        in downloaded_hdf_files_db
         
                        Scenario 2: If this tool is crawling all over ftp server, then this function needs full_path \
                        and name of the downloaded hdf file


        Parameters    : full_path: (String, Relative/Absolute full path of the hdf file)
                        file_name: (String, Name of hdf file)

        Return        : 

        """

        pass


    def file_exist_in_db(self, file_name):
        """ 
        Function name : file_exist_in_db

        Description   : Check whether this file(file_name) has already been used to populate the DB or not

        Parameters    : file_name (String, name of file)
         
        Return        : If file_name has already been used to populate DB, returns True
                        else return False
        """

        return False


    def reset_merra_db(self):
        """ 
        Function name : reset_merra_db

        Description   : This function will wipe out every info saved in merra DB (Are you sure to make MERRA DB dumb ?)

        Parameters    : 
         
        Return        : 
        """

        pass

 
