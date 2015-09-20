# You can use this software for your purpose provided you include below two lines.
# This file is part of merra_data_analyzer, a high-level ftp-protocol big size recursive file downloader and merra file analyser.
# Copyright : Mantosh Kumar @ TUM, Germany

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

class MerraDatabase:

    ### Initialize Database Configuration
    def __init__(self,DataBaseName,Username,Password,hostIP,port, log):

        self.DataBaseName       = DataBaseName
        self.Username           = Username
        self.Password           = Password
        self.hostIP             = hostIP
        self.port               = port
        self.tableforfilesadded = None
        self.log                = log

        print "MerraDatabase INIT"
        self.log.write('\nMerraDatabase class initialized')


    
    ### Open database connection
    def DatabaseConnection(self):

        try:

            self.conn = psycopg2.connect(database=self.DataBaseName, user=self.Username, password=self.Password, \
                                         host=self.hostIP, port=self.port)

            print "Successfully connected with db" + str(self.conn)
            self.log.write('\nSuccessfully connected with db' + str(self.conn))

            self.cur = self.conn.cursor()
        
            # Resetting merra db
            if MEERA_ANALYZER_CFG[RESET_MERRA_DB]:
                self.reset_merra_db()


        except psycopg2.Error as e:

            print "Error : " + str(e)
            self.log.write('\nError : db connection refused - ' + str(e))


        except:

            e = sys.exc_info()[0]
            print "Error : " + str(e)
            self.log.write('\nError : db connection refused - ' + str(e))



    ### Create Table
    def CreateTable(self,Tablename):

        try:

            if(False == self.check_If_Table_Exist(Tablename)):

                self.cur.execute("CREATE TABLE "+str(Tablename)+"( NAME  TEXT,AGE   INT );")
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



    ### Check if Table exist
    def check_If_Table_Exist(self,Tablename):

        result = False

        try:

            self.cur.execute("select exists(select relname from pg_class where relname ='"+ Tablename + "');")
            result = self.cur.fetchone()[0]

            print str(Tablename) + ' already exists in db'
            self.log.write('\n' + str(Tablename) + ' already exists in db')


        except psycopg2.Error as e:

            print str(Tablename) + " does not exist in db - " + str(e)
            self.log.write('\n' + str(Tablename) + ' does not exist in db - ' + str(e))


        except:

            e = sys.exc_info()[0]
            print str(Tablename) + " does not exist in db - " + str(e)
            self.log.write('\n' + str(Tablename) + ' does not exist in db - ' + str(e))
 

        return result
        
        

    ### Create Table
    def CreateTableforFiles(self,Tablename):

        if(False == self.check_If_Table_Exist(Tablename)):

            try:

                self.cur.execute("CREATE TABLE "+str(Tablename)+"( FileName  TEXT);")
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


        
    #### Add Filename  in Table    
    def AddfilesnameinTable(self,filename):

        try:

            self.cur.execute("INSERT INTO "+self.tableforfilesadded+"(FileName) VALUES('"+str(filename)+"');")
            self.conn.commit()

            print filename + " file name inserted successfully in table " + str(self.tableforfilesadded)
            self.log.write('\nSuccess : ' + str(filename) + ' file name inserted in ' + str(self.tableforfilesadded))

 
        except psycopg2.Error as e:

            print "Error : " + str(e)
            self.log.write('\nError : insertion failed for ' + str(filename) + ' in ' +  
                              str(self.tableforfilesadded) + ' : ' + str(e))


        except:

            e = sys.exc_info()[0]
            print "Error : " + str(e)
            self.log.write('\nError : insertion failed for ' + str(filename) + ' in ' +  \
                              str(self.tableforfilesadded) + ' : ' + str(e))



    #### Check If file exist in Table or Not        
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
        

      
    ### Create POSTGIS extension
    def CreatePostGISExtension(self):

        try: 

            self.cur.execute("CREATE EXTENSTION POSTGIS;")
            self.conn.commit()
 
            print "POSTGIS Extension Created"
            self.log.write('\nSuccess : POSTGIS Extension Created')


        except psycopg2.Error as e:

            print "Error : " + str(e)
            self.log.write('\nError : POSTGIS Extension creation failed - ' + str(e))


        except:

            e = sys.exc_info()[0]
            print "Error : " + str(e)
            self.log.write('\nError : POSTGIS Extension creation failed - ' + str(e))
        

          
    ### Create Spatial Table
    def CreateSpatialTable(self,Tablename,AttributeName):

        try: 

            self.cur.execute("CREATE TABLE " + str(Tablename) + "( time TIMESTAMP,geom GEOMETRY (PointZ, 4326)," \
                              + str(AttributeName) + " NUMERIC);")

            self.conn.commit()    

            print "Spatial Table " + str(Tablename) + " created successfully"
            self.log.write('\nSuccess : Spatial Table ' + str(Tablename) + ' created successfully')


        except psycopg2.Error as e:

            print "Error : " + str(e)
            self.log.write('\nError : Spatial Table ' + str(Tablename) + ' created failed - '  + str(e))


        except:

            e = sys.exc_info()[0]
            print "Error : " + str(e)
            self.log.write('\nError : Spatial Table ' + str(Tablename) + ' created failed - '  + str(e))


    
    def AddColumnInTable(self,Tablename,Colname,Datatype):  
 
        try:

            self.cur.execute("ALTER TABLE "+str(Tablename)+" ADD COLUMN "+Colname+" "+Datatype+";")
            self.conn.commit()
 
            print str(Colname) + " is added in " + str(Tablename) 
            self.log.write('\nSuccess : ' + str(Colname) + ' is added in ' + str(Tablename))


        except psycopg2.Error as e:

            print "Error : " + str(e)
            self.log.write('\nError : ' + str(Colname) + ' is addition in ' + str(Tablename) + ' failed - ' + str(e))


        except:

            e = sys.exc_info()[0]
            print "Error : " + str(e)
            self.log.write('\nError : ' + str(Colname) + ' is addition in ' + str(Tablename) + ' failed - ' + str(e))


    
    #### Drop Table    
    def DropTable(self,Tablename):

        try:

            self.cur.execute("DROP TABLE "+str(Tablename)+";")
            self.conn.commit()
 
            print "Table " + str(Tablename) + "Deleted successfully"
            self.log.write('\nSuccess : Table ' + str(Tablename) + 'Deleted successfully')


        except psycopg2.Error as e:

            print "Error : " + str(e)
            self.log.write('\nError : Table ' + str(Tablename) + 'Deletion failed - ' + str(e))


        except:

            e = sys.exc_info()[0]
            print "Error : " + str(e)
            self.log.write('\nError : Table ' + str(Tablename) + 'Deletion failed - ' + str(e))


   
    #### Add Data in Table    
    def AddData(self,name,age):
     
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


    
    #### Add Spatial Data in Table    
    def AddSpatialData(self,tablename,time,lat,lon,alt,value):

        try:

            #self.cur.execute("INSERT INTO "+str(tablename)+" VALUES("+str(time)+",ST_GeomFromText('POINT("+str(lat)+" "+str(lon)+" "+str(alt)+")',4326),"+str(value)+","+str(unit)+");")
            self.cur.execute("INSERT INTO " + str(tablename) + " VALUES('2004-10-19 10:23:54',ST_GeomFromText('POINT(" + \
                              str(lat) + " " + str(lon) + " " + str(alt) + ")',4326)," + str(value) + ");")

            self.conn.commit()

            print "Success : Spatial data added in " + str(tablename)
            self.log.write('\nSuccess : Spatial data added in ' + str(tablename))


        except psycopg2.Error as e:

            print "Error : " + str(e)
            self.log.write('\nError : Spatial Data addition failed  in ' + str(tablename) + ' - ' + str(e))


        except:

            e = sys.exc_info()[0]
            print "Error : " + str(e)
            self.log.write('\nError : Spatial Data addition failed  in ' + str(tablename) + ' - ' + str(e))


      
    ### DataBase Connection Disconnected
    def DatabaseClosed(self):

        try: 

            self.conn.close() 
            self.cur.close() 
            self.log.write('\nSuccess : database connection closed')


        except psycopg2.Error as e:

            print "Error: database connection failed to close - ", str(e)
            self.log.write('\nError : database connection failed to close- ' + str(e))


        except:

            e = sys.exc_info()[0]
            print "Error: database connection failed to close - ", str(e)
            self.log.write('\nError : database connection failed to close- ' + str(e))



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

                    print "Table " + str(row[1]) + " droped"
                    self.log.write('\nSuccess : Table ' + str(row[1]) + ' droped')

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
            print "Error : db reset failed - ", e
            self.log.write('\nError: db reset failed - ' + str(e))


    
