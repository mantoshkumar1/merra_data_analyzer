# You can use this software for your purpose provided you include below two lines.
# This file is part of merra_data_analyzer, a high-level ftp-protocol big size recursive file downloader and merra file analyser.
# Copyright : Mantosh Kumar @ TUM, Germany


This README document contains all the informations that are necessary to get this application up and running.


### Summary ###
---------------------------------------------------------------------------------------------------
* MERRA DATA ANALYZER
* Description : Download MERRA data from NASA FTP server, extract and populate them to Postgres database
* Version     : 1.0
* Repository  : https://bitbucket.org/mantoshkumar1/merra_data_analyzer


### How to use this tool ###
---------------------------------------------------------------------------------------------------
$ cd merra_analyzer
$ export PYTHONPATH=$PWD
$ python scripts/hdf_script.py
--------- Relax Now ----------

Note : You can see the logging of this tool in home directory "log.log" file.

# For advanced user / Developer only to manually configure MERRA DB
$ psql
$ create database merra; (Set this DB_NAME in cfg.py)
$ \c merra;  (connect to DB)
$ \q         (exit from psql prompt)

# How do I get set up? / Dependencies before using this tool
Please read DUMMY_READ_ME.txt file

# Tool Custom Configuration Settings
Please read DUMMY_READ_ME.txt file

### Who do I talk to? ###
---------------------------------------------------------------------------------------------------
# LinkedIn  : de.linkedin.com/in/mantoshk
# eMail     : mantosh.kumar@tum.de
#             mantoshkumar1@gmail.com



