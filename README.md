# You can use this software for your purpose provided you include below two lines.
# This file is part of merra_data_analyzer, a high-level ftp-protocol big size recursive file downloader and merra file analyser.
# Copyright : Mantosh Kumar @ TUM, Germany

This README document contains all the informations that are necessary to get this application up and running.

### How to use this tool ###
---------------------------------------------------------------------------------------------------
$ cd merra_analyzer
$ export PYTHONPATH=$PWD
$ python scripts/hdf_script.py

$ psql
$ create database merra; (Set this DB_NAME in cfg.py)
$ \c merra;  (connect to DB)
$ \q         (exit from psql prompt)

### Where is its repository? ###

* MERRA DATA ANALYZER (write a short description)
* Version : 1.0
* https://bitbucket.org/mantoshkumar1/merra_data_analyzer

### How do I get set up? ###

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
   4.1  you will may need to invoke the command with superuser privileges to install to the system Python: (NOTE)
        $ wget https://bootstrap.pypa.io/ez_setup.py -O - | sudo python

   4.2  Alternatively, Setuptools may be installed to a user-local path: (NOTE)
        $ wget https://bootstrap.pypa.io/ez_setup.py -O - | python - --user

   NOTE: In case it fails, please check the failure log displayed on screen and find out which dependencies are missing.
         Download and install those dependencies one after another and once it's done, try the same command again.

5. Installing C and gfortan compiler with software package gcc:
   # check the list of installed compilers
     $ dpkg --list | grep compiler

   Note : If both gcc and gfortran are missing, follow step 5.1
          If gcc is missing, follow step 5.1
          If gcc is installed but gfortran is missiing, follow steep 5.2

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

   $ sudo -i -u postgres     (postgres is your db user name, bu default it is set in cfg.py)
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
You can see the logging of this tool in home directory "log" file.


* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###
 
* Please see the contributors text file

