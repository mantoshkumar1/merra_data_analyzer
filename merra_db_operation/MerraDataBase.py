
#### Command Line Access
##   sudo -i -u postgres
##   Access Command Prompt     :   psql
##   \c Merra
##   \dt
##   \db
##   Select * from Tablename; 




#!/usr/bin/python
import psycopg2

class MerraDatabase:
    ### Initialize Database Configuration
    def __init__(self,DataBaseName,Username,Password,hostIP,port):
        self.DataBaseName=DataBaseName
        self.Username=Username
        self.Password=Password
        self.hostIP=hostIP
        self.port=port
        self.tableforfilesadded=None
        print "MerraDatabase INIT"
    
    ### Open database connection
    def DatabaseConnection(self):
        self.conn = psycopg2.connect(database=self.DataBaseName, user=self.Username, password=self.Password,host=self.hostIP, port=self.port)
        print " conn ",self.conn
        self.cur = self.conn.cursor()

    ### Create Table
    def CreateTable(self,Tablename):    
        self.cur.execute("CREATE TABLE "+str(Tablename)+"( NAME  TEXT,AGE   INT );")
        print "Table created successfully"
        self.conn.commit()


    ### Create Table
    def check_If_Table_Exist(self,Tablename):    
        self.cur.execute("SELECT relname FROM pg_class WHERE relname ='"+Tablename+"';")
        self.conn.commit()
        result=self.cur.fetchone()
        print result
        if result ==None:
            return False
        else:
            return True
        
        

    ### Create Table
    def CreateTableforFiles(self,Tablename):    
        self.cur.execute("CREATE TABLE "+str(Tablename)+"( FileName  TEXT);")
        print Tablename+" Table created successfully"
        self.conn.commit()
        self.tableforfilesadded=Tablename;
        
    #### Add Filename  in Table    
    def AddfilesnameinTable(self,filename):
        self.cur.execute("INSERT INTO "+self.tableforfilesadded+"(FileName) VALUES('"+str(filename)+"');")
        print filename+" Added successfully"      
        self.conn.commit()
        
    #### Check If file exist in Table or Not    
    
    def file_exist_in_db(self,filename):
        """ 
        Function name : file_exist_in_db

        Description   : Check whether this file(file_name) has already been used to populate the DB or not

        Parameters    : file_name (String, name of file)
         
        Return        : If file_name has already been used to populate DB, returns True
                        else return False
        """

        self.cur.execute("select FileName from " + self.tableforfilesadded + " where FileName='" + filename + "';")
        self.conn.commit()
        result=self.cur.fetchone()
        print result
        if result ==None:
            return False
        else:
            return True
        
      
    ### Create POSTGIS extension
    def CreatePostGISExtension(self):    
        self.cur.execute("CREATE EXTENSTION POSTGIS;")
        print "POSTGIS Extension Created"
        self.conn.commit() 
        
          
    ### Create Spatial Table
    def CreateSpatialTable(self,Tablename,AttributeName):  
        print " Tablename  : ",Tablename  
        self.cur.execute("CREATE TABLE "+str(Tablename)+"( time TIMESTAMP,geom GEOMETRY (PointZ, 4326),"+str(AttributeName)+" NUMERIC);")
        print "Spatial Table created successfully"
        self.conn.commit()    
    
    def AddColumnInTable(self,Tablename,Colname,Datatype):    
        self.cur.execute("ALTER TABLE "+str(Tablename)+" ADD COLUMN "+Colname+" "+Datatype+";")
        print "Spatial Table created successfully"
        self.conn.commit()    
    
    #### Drop Table    
    def DropTable(self,Tablename):    
        self.cur.execute("DROP TABLE "+str(Tablename)+";")
        print "Table Deleted successfully"
        self.conn.commit()   
   
    #### Add Data in Table    
    def AddData(self,name,age):
   
        self.cur.execute("INSERT INTO Test(NAME,AGE) VALUES( '''"+str(name)+"''',"+str(age)+" );")
        print "Data Added successfully"      
        self.conn.commit()
    
    #### Add Spatial Data in Table    
    def AddSpatialData(self,tablename,time,lat,lon,alt,value):
        #self.cur.execute("INSERT INTO "+str(tablename)+" VALUES("+str(time)+",ST_GeomFromText('POINT("+str(lat)+" "+str(lon)+" "+str(alt)+")',4326),"+str(value)+","+str(unit)+");")
        print "tablename",tablename
        self.cur.execute("INSERT INTO "+str(tablename)+" VALUES('2004-10-19 10:23:54',ST_GeomFromText('POINT("+str(lat)+" "+str(lon)+" "+str(alt)+")',4326),"+str(value)+");")
        print "Spatial Data Added successfully"      
        self.conn.commit()

      
    ### DataBase Connection Disconnected
    def DatabaseClosed(self):  
        self.conn.close()  


    
    
