# You can use this software for your purpose provided you include below two lines.
# This file is part of merra_data_analyzer, a high-level ftp-protocol big size recursive file downloader and merra file analyser.
# Copyright : Mantosh Kumar @ TUM, Germany


This README document contains all the informations that are necessary to get this application up and running.


### Summary ###
---------------------------------------------------------------------------------------------------
* MERRA DATA ANALYZER
* Description :
* Version     : 1.0
* Repository  : https://bitbucket.org/mantoshkumar1/merra_data_analyzer


### How to use this tool ###
---------------------------------------------------------------------------------------------------
$ cd merra_analyzer
$ export PYTHONPATH=$PWD
$ python scripts/hdf_script.py
--------- Relax Now ----------

Note : You can see the logging of this tool in home directory "log" file.

# For advanced user / Developer only to manually configure MERRA DB
$ psql
$ create database merra; (Set this DB_NAME in cfg.py)
$ \c merra;  (connect to DB)
$ \q         (exit from psql prompt)


### Configuration ###
---------------------------------------------------------------------------------------------------
You can adjust the control settings of this tool by modifying "cfg.py" in home directory.
By default every field is assigned some values. Each field is explained below in this section.
Note : Please always remember that merra_analyzer is the home directory of this tool. All relative addresses should be \
       computed based on this.


1. YOUR_LOCAL_HDFFILE_DIR_PATH

   # YOUR_LOCAL_HDFFILE_DIR_PATH = '/user/local_hdf_files',
     You can use this setting to populate the MERRA DB with local HDF files.

     Set this field to relative / absolute path of a directory where you have local HDF files. It will find all the hdf files \
     stored inside that directory & its subdirectories.

     Please note that if you enable this setting then all settings related with FTP server will be disabled. There will be no \
     FTP server crawling. Good part is you do not need internet connectivity for this.

   # YOUR_LOCAL_HDFFILE_DIR_PATH = None,
     You can use this setting for crawling FTP server and finding all HDF files over there.

2. MERRA_DATA_DOWNLOAD_DIR_PATH
   This is one of the FTP related setting.

   MERRA_DATA_DOWNLOAD_DIR_PATH = /user/download_hdf_dir,
   Set your choice of directory path where you want to download HDF files. By default those files will be \ 
   downloaded in "merra_downloaded_data" directory.

3. SAVE_DOWNLOADING_DATA
   This is one of the FTP related setting.

   SAVE_DOWNLOADING_DATA = True,
   if you want to store downloading files in your preferred directory.

   SAVE_DOWNLOADING_DATA = False,
   if you do not want to store downloading files. After DB population it will be deleted.

4. USER_EMAIL_ADDR   
   This is one of the FTP related setting.

   USER_EMAIL_ADDR : 'user@tum.de',
   NASA FTP server uses email as password for login (even dummy email will work) 

5. FTP_HOST_ADDR
   This is one of the FTP related setting.

   FTP_HOST_ADDR : 'ftp.tum.de',
   FTP_HOST_ADDR : '1.2.3.4',
   Set FTP host address. Both Domain name and ip address are acceptable.

6. FTP_HOME_DIR
   This is one of the FTP related setting. It sets the home directory over ftp server.

   FTP_HOME_DIR : ["/"],
   If you are uncertain which should be your home dir over ftp server, set it to ["/"]

   FTP_HOME_DIR : ["/x/y", "dat"],
   You can select multiple home directory over ftp server in which you want to crawl.

7. FTP_DEBUG_LEVEL
   This is one of the FTP related setting.
 
   FTP_DEBUG_LEVEL : 0, 
   Use this setting to observe interacton of this tool with ftp server. You can choose one among \ 
   0(none), 1(some output), 2 (max output).
   
8. PROCESSING_FILE_TYPE
   This is one of the FTP related setting.

   PROCESSING_FILE_TYPE : '.hdf',
   Set the type of downloading/processing file from FTP server.

9. MAX_ATTEMPTS_TO_DOWNLOAD
   This is one of the FTP related setting.

   MAX_ATTEMPTS_TO_DOWNLOAD : 11,
   Set the number of maximum tries to reconnect with network in case of network failure while downloading a file.

10. RETRY_TIMEOUT
    This is one of the FTP related setting.

    RETRY_TIMEOUT : 15,
    Set this waiting time(seconds) before reconnecting while downloading if the connection dies.

11. MERRA_DB_NAME : 'merra',
    This is one of the MERRA DB related setting. Enter the name of your db.

12. MERRA_DB_LOGIN : 'postgres',
    This is one of the MERRA DB related setting. Enter your user name / login of db
    
13. MERRA_DB_PASSWORD : 'password',
    This is one of the MERRA DB related setting. Enter your password of your db.

14. MERRA_DB_HOST_IP : '127.0.0.1',
    This is one of the MERRA DB related setting. Set host ip of your db.

15. MERRA_DB_PORT : '5432',
    This is one of the MERRA DB related setting. Set the port of your db.

16. RESET_MERRA_DB
    This is one of the MERRA DB related setting. Set the port of your db.

    RESET_MERRA_DB : True,
    It will delete all previous data saved in merra db and all tables will be droped. DB will be populated with new data.

    RESET_MERRA_DB : False,
    It will keep old data intact.
    

### How do I get set up? / Dependencies ###
---------------------------------------------------------------------------------------------------

*  Follow following steps:
1. Operating system description: Debian GNU/Linux 8.1 (jessie)
   # Get ISO image for the Debian GNU/Linux operating system from 
     http://cdimage.debian.org/debian-cd/8.1.0/i386/iso-dvd/debian-8.1.0-i386-DVD-1.iso
   
   $ cat /etc/debian_version

2. $ sudo apt-get update
   $ sudo apt-get install build-essential

3. Python version : 2.7.9 (Any version [ 2.7 or 3 family ] above 2.7.5  is adequate)
   <3.1> $ whereis python
           if python is already installed then check the version of python
           <3.1.1> $ python -V
                   if the version of python is correct, goto step 4.
  
           if python is not installed or version is not suitable, then proceed to following steps.

   <3.2> $ sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev
   <3.3> $ sudo apt-get install libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
   <3.4> $ wget http://python.org/ftp/python/2.7.5/Python-2.7.5.tgz
   <3.5> $ tar -xvf Python-2.7.5.tgz cd Python-2.7.5
   <3.5> $ cd Python-2.7.5
   <3.6> $ ./configure 
   <3.7> $ make
   <3.8> $ sudo make install
   <3.9> $ python -V

4. Install easy_install to automatically download, build, install, and manage Python packages.
   Execute only one of the following steps 4.1 or 4.2:
   <4.1>  you need to invoke this command with superuser privileges to install to the system Python: (see NOTE)
          $ wget https://bootstrap.pypa.io/ez_setup.py -O - | sudo python

   <4.2>  Alternatively, Setuptools may be installed to a user-local path: (see NOTE)
          $ wget https://bootstrap.pypa.io/ez_setup.py -O - | python - --user

   NOTE: In case it fails, please check the failure log displayed on screen and find out which dependencies are missing.
         Download and install those dependencies one after another and once it's done, try the same command again.

5. Install C and gfortan compiler with software package gcc:
   # check the list of installed compilers
     $ dpkg --list | grep compiler

   Note : If both gcc and gfortran are missing, follow step 5.1
          Else if gfortran is installed but gcc is missing, follow step 5.1
          Else if gcc is installed but gfortran is missiing, follow steep 5.2

          Follow only one of the below step (5.1 or 5.2).

   5.1  Intsall GCC using following steps (gfortran/C  both will get installed with gcc):
        <5.1.1>  $ mkdir GCC_4.9.2
        <5.1.2>  $ cd GCC_4.9.2
        <5.1.3>  $ wget https://ftp.gnu.org/gnu/gcc/gcc-4.9.2/gcc-4.9.2.tar.gz
        <5.1.4>  $ tar xzf gcc-4.9.2.tar.gz
        <5.1.5>  $ cd gcc-4.9.2
        <5.1.6>  $ ./contrib/download_prerequisites
        <5.1.7>  $ cd ..
        <5.1.8>  $ mkdir objdir
        <5.1.9>  $ cd objdir
        <5.1.10> $ $PWD/../gcc-4.9.2/configure
        <5.1.11> $ sudo make      (Goto a party, it will take significant time)
        <5.1.12> $ sudo make install
        <5.1.13> $ gcc --version

   5.2  Install gfortran using following steps:
        <5.2.1>  $ wget https://packages.debian.org/jessie/i386/gfortran/download
        <5.2.2>  $ sudo dpkg -i gfortran_4.9.2-2_i386.deb
        <5.2.3>  $ gfortran --version


6. Install libjpeg for stable and solid foundation for many application's JPEG support
   $ wget http://www.ijg.org/files/jpegsrc.v9a.tar.gz
   $ tar -xvf jpegsrc.v9a.tar.gz 
   $ cd jpeg-9a
   $ ./configure
   $ make
   $ make check
   $ sudo make install


7. Install Szip
   $ wget http://www.hdfgroup.org/ftp/lib-external/szip/2.1/src/szip-2.1.tar.gz
   $ tar -xvf szip-2.1.tar.gz
   $ cd szip-2.1
   $ ./configure --prefix=/usr/local/lib
   $ make
   $ make check
   $ sudo make install

8. Install NumPy, HDF4 libraries and zlib (Requirements for HDF4)
   $ sudo apt-get install python-dev python-numpy libhdf4-dev -y
   $ sudo apt-get install python-pip -y
   $ sudo pip install python-hdf4

9. Install object-relational database system POSTGRESQL/PGIS
   $ sudo apt-get install python-software-properties
   $ sudo apt-get install software-properties-common
   $ sudo apt-add-repository ppa:ubuntugis/ppa
   $ sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable
   $ sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

   $ sudo apt-get install wget ca-certificates
   $ wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
   $ sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt jessie-pgdg main" >> /etc/apt/sources.list'
   $ wget --quiet -O - http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | sudo apt-key add -
   $ sudo apt-get update
   $ sudo apt-get upgrade

   $ sudo apt-get install postgresql-9.4 postgresql-9.4-postgis pgadmin3 postgresql-contrib postgresql-9.4-postgis-scripts
   $ sudo apt-add-repository -y ppa:georepublic/pgrouting
   $ sudo apt-get update
   $ sudo apt-get install postgresql-9.4-pgrouting
   $ sudo apt-get install libpq-dev python-psycopg2

   $ sudo -i -u postgres     (postgres is your db user name / login, by default it is set in cfg.py)
   # For the first time, it would ask to set a password (Set this passowrd in cfg.py), \
     From next time you will be auto-logged in and will be able to interact with the \
     database management system right away. You can exit out of the PostgreSQL prompt by pressing Ctrl+D

   # Create a New Role for yourself as "admin".
     $ createuser --interactive
     # Press 'y' for role as a superuser

   $ createdb YOUR_DB_NAME;
   $ psql -U your_db_name;
   $ CREATE DATABASE routing;
   $ \c routing
   $ CREATE EXTENSION postgis;
   $ CREATE EXTENSION pgrouting;

   # If last call is successful, Installtion of POSTGRESQL/PGIS is complete.


10. $ sudo pip install matplotlib mpl_toolkits psycopg2


11. $ sudo apt-get update
    $ sudo apt-get upgrade

You are now ready to use the merra tool.


### Who do I talk to? ###
---------------------------------------------------------------------------------------------------
* Please see the contributors text file (contributors.txt) in home directory for complete info
# LinkedIn  : de.linkedin.com/in/mantoshk
# eMail     : mantosh.kumar@tum.de
#             mantoshkumar1@gmail.com



