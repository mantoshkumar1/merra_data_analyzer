# You can use this software for your purpose provided you include below two lines.
# This file is part of merra_data_analyzer, a high-level ftp-protocol big size recursive file downloader and merra file analyser.
# Copyright : Mantosh / Gaurav @ TUM, Germany

#### Command Line Access
##   sudo -i -u postgres
##   Access Command Prompt     :   psql
##   \c Merra
##   \dt
##   \db
##   Select * from Tablename; 

import psycopg2
import sys

from cfg import MEERA_ANALYZER_CFG, RESET_MERRA_DB
from merra_db_operation.DBConfigFile import DatabaseTablesName

class MerraDatabase:

    def __init__(self,DataBaseName,Username,Password,hostIP,port, log):
        """
        Function name : __init__
        
        Description   : Initialize MerraDatabase Class Configuration
            
        Parameters    : DataBaseName, Username, Password, hostIP, port
    
        Return        : 
        """          

        self.DataBaseName       = DataBaseName
        self.Username           = Username
        self.Password           = Password
        self.hostIP             = hostIP
        self.port               = port
        self.tableforfilesadded = None
        self.log                = log


        # connect with db
        self.DatabaseConnection()


        # initializing FilesAdded table in db (use lowercase for table name/s) - it keeps track of already populated hdf files
        tablename = DatabaseTablesName['FilesAdded'].lower()
        self.CreateTableforFiles(tablename)


        print "MerraDatabase class initialized"
        self.log.write('\nMerraDatabase class initialized')


    
    def DatabaseConnection(self):
        """
        Function name : DatabaseConnection
        
        Description   : Open database connection
            
        Parameters    : 
    
        Return        : 
        """         

        try:

            self.conn = psycopg2.connect(database=self.DataBaseName, user=self.Username, password=self.Password, \
                                         host=self.hostIP, port=self.port)

            print "Successfully connected with db" + str(self.conn)
            self.log.write('\nSuccess : connected with db' + str(self.conn))

            self.cur = self.conn.cursor()
        
            # Resetting merra db if user said so
            if MEERA_ANALYZER_CFG[RESET_MERRA_DB]:
                self.reset_merra_db()


        except psycopg2.Error as e:

            print "Error : " + str(e)
            self.log.write('\nError : db connection refused - ' + str(e))


        except:

            e = sys.exc_info()[0]
            print "Error : " + str(e)
            self.log.write('\nError : db connection refused - ' + str(e))



    def CreateTable(self,Tablename):
        """
        Function name : CreateTable
        
        Description   : Create table in Database
            
        Parameters    : table name
    
        Return        : None
        """             

        try:

            if(False == self.check_If_Table_Exist(Tablename)):

                self.cur.execute("CREATE TABLE " + str(Tablename) + "( NAME  TEXT,AGE   INT );")
                self.conn.commit()

                print "Success : Table " + str(Tablename) + " created"
                self.log.write('\nSuccess : ' + str(Tablename) + ' created')

        
        except psycopg2.Error as e:

            print "Error : " + str(e)
            self.log.write('\nError : ' + str(Tablename) + ' table creation failed : ' + str(e))


        except:

            e = sys.exc_info()[0]
            print "Error : " + str(e)
            self.log.write('\nError : ' + str(Tablename) + ' table creation failed : ' + str(e))



    def check_If_Table_Exist(self,Tablename):
        """
        Function name : check_If_Table_Exist
        
        Description   : Check if a table exist in Data base or not
            
        Parameters    : table name
    
        Return        : Flag :True if exist otherwise False
        """         

        result = False

        try:

            self.cur.execute("select exists(select relname from pg_class where relname ='"+ Tablename + "');")
            result = self.cur.fetchone()[0]

            if(result == True):
                print "Table "  + str(Tablename) + ' already exists in db'
                self.log.write('\nTable ' + str(Tablename) + ' already exists in db')

            else:
                print "Table "  + str(Tablename) + ' does not exist in db'
                self.log.write('\nTable ' + str(Tablename) + ' does not exist in db')


        except psycopg2.Error as e:

            print "Table " + str(Tablename) + " does not exist in db - " + str(e)
            self.log.write('\nTable ' + str(Tablename) + ' does not exist in db - ' + str(e))


        except:

            e = sys.exc_info()[0]
            print "Table " + str(Tablename) + " does not exist in db - " + str(e)
            self.log.write('\nTable ' + str(Tablename) + ' does not exist in db - ' + str(e))
 

        return result
        
        

    def CreateTableforFiles(self,Tablename):
        """
        Function name : CreateTableforFiles
        
        Description   : Create a Table in Database which store info about HDF files
            
        Parameters    : table name
    
        Return        : Flag :True if exist False if not
        """        

        if(False == self.check_If_Table_Exist(Tablename)):

            try:

                self.cur.execute("CREATE TABLE " + str(Tablename) + "( FileName  TEXT);")
                self.conn.commit()

                print Tablename+" Table created successfully"
                self.log.write('\nSuccess : ' + str(Tablename) + ' created')


            except psycopg2.Error as e:

                print "Error : " + str(e)
                self.log.write('\nError : ' + str(Tablename) + ' table creation failed - ' + str(e))

            except:

                e = sys.exc_info()[0]
                print "Error : " + str(e)
                self.log.write('\nError : ' + str(Tablename) + ' table creation failed - ' + str(e))


        self.tableforfilesadded = Tablename;


        
    def AddfilesnameinTable(self,filename):
        """
        Function name : AddfilesnameinTable
        
        Description   : Add HDF files names from which data is successfully added in Database
            
        Parameters    : File name
    
        Return        : None
        """          

        try:

            self.cur.execute("INSERT INTO " + self.tableforfilesadded + "(FileName) VALUES('" + str(filename) + "');")
            self.conn.commit()

            print "Success : File name '" + str(filename) + "' inserted in table '" + str(self.tableforfilesadded) + "'"
            self.log.write('\nSuccess : File name = ' + str(filename) + ' inserted in table ' + str(self.tableforfilesadded))

 
        except psycopg2.Error as e:

            print "Error : " + str(e)
            self.log.write('\nError : insertion failed for file name ' + str(filename) + ' in table ' +  
                              str(self.tableforfilesadded) + ' : ' + str(e))


        except:

            e = sys.exc_info()[0]
            print "Error : " + str(e)
            self.log.write('\nError : insertion failed for file name ' + str(filename) + ' in table ' +  \
                              str(self.tableforfilesadded) + ' : ' + str(e))



    def file_exist_in_db(self,filename):
        """ 
        Function name : file_exist_in_db

        Description   : Check whether this file(file_name) has already been used to populate the DB or not

        Parameters    : file_name (String, name of file)
         
        
        Return        : If file_name has already been used to populate DB, returns True
                        else return False
        """

        try:

            self.cur.execute("select FileName from " + self.tableforfilesadded + " where FileName='" + filename + "';")
            self.conn.commit()
            result = self.cur.fetchone()

            if result == None:

                self.log.write('\n' + str(filename) + ' does not exist in ' + str(self.tableforfilesadded) + ' table')
                print str(filename) + ' does not exist in ' + str(self.tableforfilesadded) + ' table'
                return False

            else:

                self.log.write('\n' + str(filename) + ' already exists in ' + str(self.tableforfilesadded) + ' table')
                print str(filename) + ' already exists in ' + str(self.tableforfilesadded) + ' table'
                return True


        except psycopg2.Error as e:

            print "Error : " + str(e)
            self.log.write('\nError : file_exist_in_db function failed - ' + str(e))


        except:

            e = sys.exc_info()[0]
            print 'Error: ' + str(e)
            self.log.write('\nError : file_exist_in_db function failed - ' + str(e))


        return False
        
        

    def CreatePostGISExtension(self): 
        """
        Function name : CreatePostGISExtension
        
        Description   : Create a PostGIS extension for storing spatial data            
        
        Parameters    : None
        
        Return        : None
        """             
      
        try: 

            self.cur.execute("CREATE EXTENSTION POSTGIS;")
            self.conn.commit()
 
            print "POSTGIS Extension created"
            self.log.write('\nSuccess : POSTGIS Extension created')


        except psycopg2.Error as e:

            print "Error : " + str(e)
            self.log.write('\nError : POSTGIS Extension creation failed - ' + str(e))


        except:

            e = sys.exc_info()[0]
            print "Error : " + str(e)
            self.log.write('\nError : POSTGIS Extension creation failed - ' + str(e))
        

          
    def Create3DTable(self,Tablename,AttributeName): 
        """
        Function name : CreateSpatialTable
        
        Description   : Create a spatial table for storing 3D spatial data            
        
        Parameters    : Table name and Attribute Name
        
        Return        : None
        """

        try: 

            self.cur.execute("CREATE TABLE " + str(Tablename) + "( time TIMESTAMP,geom GEOMETRY (PointZ, 4326)," + str(AttributeName) + " NUMERIC);")
            self.conn.commit()   
            self.log.write('\nSuccess : Table ' + str(Tablename) + ' created')
            print "\nSuccess : Table " + str(Tablename) + " created"

        except psycopg2.Error as e:

            print "Error : " + str(e)
            self.log.write('\nError : 3D spatial table creation failed - ' + str(e))


        except:

            e = sys.exc_info()[0]
            self.log.write('\nError : 3D spatial table creation failed - ' + str(e))
            print "Error : " + str(e)
        

    def Create2DTable(self,Tablename,AttributeName): 
        """
        Function name : CreateSpatialTable

        Description   : Create a spatial table for storing 2D spatial data            
        
        Parameters    : Table name and Attribute Name
        
        Return        : None
        """
        try:

            self.cur.execute("CREATE TABLE "+str(Tablename)+"( time TIMESTAMP,geom GEOMETRY (Point,4326),"+str(AttributeName)+" NUMERIC);")
            self.conn.commit()
 
            self.log.write('\nSuccess : Table ' + str(Tablename) + ' created')
            print "\nSuccess : Table " + str(Tablename) + " created"
 
        except psycopg2.Error as e:

            print "Error : " + str(e)
            self.log.write('\nError : 2D spatial table creation failed - ' + str(e))

        except:

            e = sys.exc_info()[0]
            self.log.write('\nError : 2D spatial table creation failed - ' + str(e))
            print "Error : " + str(e)
            
   
    def DropTable(self,Tablename): 
        """
        Function name : DropTable
        
        Description   : Delete a table from Database           
        
        Parameters    : Table name 
        
        Return        : None
        """          
 
        try: 

            self.cur.execute("DROP TABLE " + str(Tablename) + ";")
            self.conn.commit()  

            self.log.write('\nSuccess : Table ' + str(Tablename) + ' dropped')
            print "\nSuccess : Table " + str(Tablename) + " dropped"
 
        except psycopg2.Error as e:

            print "Error : " + str(e)
            self.log.write('\nError : Drop table ' + str(Tablename) + 'failed - ' + str(e))

        except:

            e = sys.exc_info()[0]
            self.log.write('\nError : Drop table ' + str(Tablename) + 'failed - ' + str(e))
            print "Error : " + str(e)
            
   
   
    def Add3DData(self,tablename,time,lat,lon,alt,value):
        """
        Function name : Add3DData
        
        Description   : Add 3d Data in Table       
        
        Parameters    : tablename,time,lat,lon,alt,value
        
        Return        : None
        """

        print tablename
        print time
        print lat
        print lon
        print alt
        print value        

        try:
            self.cur.execute("INSERT INTO "+str(tablename)+" VALUES('"+str(time)+"',ST_GeomFromText('POINT("+str(lat)+" "+str(lon)+" "+str(alt)+")',4326),"+str(value)+");")

            self.conn.commit()
            print "3D Data Added successfully in " + str(tablename)
            self.log.write('\nSuccess : 3D data added in table ' + str(tablename))

        except psycopg2.Error as e:

            print "Error : " + str(e)
            self.log.write('\nError : 3D Data addition failed in table ' + str(tablename) + ' - ' + str(e))

        except:

            e = sys.exc_info()[0]
            self.log.write('\nError : 3D Data addition failed in table ' + str(tablename) + ' - ' + str(e))
            print "Error : " + str(e)
            


    def Add2DData(self,tablename,time,lat,lon,value):
        """
        Function name : Add2DData
        
        Description   : Add 2D Spatial Data in Table       
        
        Parameters    : tablename,time,lat,lon,alt,value
        
        Return        : None
        """

        print tablename
        print time
        print lat
        print lon
        print value

        try:

            self.cur.execute("INSERT INTO "+str(tablename)+" VALUES('"+str(time)+"',ST_GeomFromText('POINT("+str(lat)+" "+str(lon)+")',4326),"+str(value)+");")
            self.conn.commit()
            print "2D Data Added successfully in " + str(tablename)
            self.log.write('\nSuccess : 2D data added in table ' + str(tablename))

        except psycopg2.Error as e:

            print "Error : " + str(e)
            self.log.write('\nError : 2D Data addition failed in table ' + str(tablename) + ' - ' + str(e))


        except:

            e = sys.exc_info()[0]
            self.log.write('\nError : 2D Data addition failed in table ' + str(tablename) + ' - ' + str(e))
            print "Error : " + str(e)
        
    
    def AddColumnInTable(self,Tablename,Colname,Datatype):  
        """
        Function name : AddColumnInTable
        
        Description   : Add column in a table
        
        Parameters    : table name,column name and data type
        
        Return        : None
        """
 
        try:

            self.cur.execute("ALTER TABLE " + str(Tablename) + " ADD COLUMN " + Colname + " " + Datatype + ";")
            self.conn.commit()
 
            print str(Colname) + " is added in " + str(Tablename) 
            self.log.write('\nSuccess : ' + str(Colname) + ' is added in ' + str(Tablename))


        except psycopg2.Error as e:

            print "Error : " + str(e)
            self.log.write('\nError : ' + str(Colname) + ' addition failed in ' + str(Tablename) + ' - ' + str(e))


        except:

            e = sys.exc_info()[0]
            print "Error : " + str(e)
            self.log.write('\nError : ' + str(Colname) + ' addition failed in ' + str(Tablename) + ' - ' + str(e))



    def AddData(self,name,age):
        """
        Function name : AddData
        
        Description   : Add data
        
        Parameters    : name, age
        
        Return        : None
        """
     
        try:  

            self.cur.execute("INSERT INTO Test(NAME,AGE) VALUES( '''"+str(name)+"''',"+str(age)+" );")
            self.conn.commit()

            print "Success: Data Added in table"      
            self.log.write('\nSuccess : Data added in table')


        except psycopg2.Error as e:

            print "Error : " + str(e)
            self.log.write('\nError : Data addition failed - ' + str(e))


        except:

            e = sys.exc_info()[0]
            print "Error : " + str(e)
            self.log.write('\nError : Data addition failed - ' + str(e))


      
    def DatabaseClosed(self):
        """
        Function name : DatabaseClosed
        
        Description   : To Disconnect the DataBase Connection      
        
        Parameters    : None
        
        Return        : None
        """        

        try: 

            self.conn.close() 
            self.cur.close() 
            self.log.write('\nSuccess : database connection closed')


        except psycopg2.Error as e:

            print "Error: database connection failed to close - ", str(e)
            self.log.write('\nError : database connection failed to close - ' + str(e))


        except:

            e = sys.exc_info()[0]
            print "Error: database connection failed to close - ", str(e)
            self.log.write('\nError : database connection failed to close - ' + str(e))



    def reset_merra_db(self):
        """ 
        Function name : reset_merra_db

        Description   : This function will wipe out every info saved in merra DB (Are you sure to make MERRA DB dumb ?)

        Parameters    : 
         
        Return        : 
        """

        try:

            self.cur.execute("SELECT table_schema,table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_schema,table_name")

            rows = self.cur.fetchall()

            for row in rows:

                try:

                    self.cur.execute("drop table " + row[1] + " cascade")
                    self.conn.commit()

                    print "Table " + str(row[1]) + " dropped"
                    self.log.write('\nSuccess : Table ' + str(row[1]) + ' dropped')

                except:

                    e = sys.exc_info()[1]
                    print "Error : drop table " + str(row[1]) + " failed - " + str(e)
                    self.log.write('Error : drop table ' + str(row[1]) + ' failed - ' + str(e))


            print "Success : MERRA db is reset"
            self.log.write('\nSuccess : MERRA db is reset')


        except psycopg2.Error as e:

            print "Error : db reset failed - ", str(e)
            self.log.write('\nError : db reset failed - ' + str(e))
 

        except:
            
            e = sys.exc_info()[1]
            print "Error : db reset failed - ", str(e)
            self.log.write('\nError: db reset failed - ' + str(e))


    
