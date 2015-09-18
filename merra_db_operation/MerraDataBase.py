
#### Command Line Access
##   sudo -i -u postgres
##   Access Command Prompt     :   psql
##   \c Merra
##   \dt
##   \db
##   Select * from Tablename; 


import psycopg2
from cfg import MEERA_ANALYZER_CFG, RESET_MERRA_DB

class MerraDatabase:
    ### Initialize Database Configuration
    def __init__(self,DataBaseName,Username,Password,hostIP,port):
        self.DataBaseName = DataBaseName
        self.Username  = Username
        self.Password = Password
        self.hostIP = hostIP
        self.port = port
        self.tableforfilesadded = None
        print "MerraDatabase INIT"

        if MEERA_ANALYZER_CFG[RESET_MERRA_DB]:
            self.reset_merra_db()

    
    ### Open database connection
    def DatabaseConnection(self):
        try:
            self.conn = psycopg2.connect(database=self.DataBaseName, user=self.Username, password=self.Password,host=self.hostIP, port=self.port)
            print " conn ",self.conn
            self.cur = self.conn.cursor()

        except psycopg2.Error as e:
            print e

    ### Create Table
    def CreateTable(self,Tablename):
        try:
            if(False == self.check_If_Table_Exist(Tablename)):
                self.cur.execute("CREATE TABLE "+str(Tablename)+"( NAME  TEXT,AGE   INT );")
                print "Table created successfully"
                self.conn.commit()
        
        except psycopg2.Error as e:
            print e


    ### Check if Table exist
    def check_If_Table_Exist(self,Tablename):

        result = False
        try:
            self.cur.execute("select exists(select relname from pg_class where relname ='"+ Tablename + "');")
            result = self.cur.fetchone()[0]

        except psycopg2.Error as e:
            print e
 
        return result
        
        

    ### Create Table
    def CreateTableforFiles(self,Tablename):
        if(False == self.check_If_Table_Exist(Tablename)):
            try:
                self.cur.execute("CREATE TABLE "+str(Tablename)+"( FileName  TEXT);")
                print Tablename+" Table created successfully"
                self.conn.commit()

            except psycopg2.Error as e:
                print e

        self.tableforfilesadded = Tablename;
        
    #### Add Filename  in Table    
    def AddfilesnameinTable(self,filename):
        try:
            self.cur.execute("INSERT INTO "+self.tableforfilesadded+"(FileName) VALUES('"+str(filename)+"');")
            print filename+" Added successfully"      
            self.conn.commit()
 
        except psycopg2.Error as e:
            print e
        
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
            result=self.cur.fetchone()
            if result == None:
                return False
            else:
                return True

        except psycopg2.Error as e:
            print e
        
      
    ### Create POSTGIS extension
    def CreatePostGISExtension(self):
        try: 
            self.cur.execute("CREATE EXTENSTION POSTGIS;")
            print "POSTGIS Extension Created"
            self.conn.commit() 

        except psycopg2.Error as e:
            print e
        
          
    ### Create Spatial Table
    def CreateSpatialTable(self,Tablename,AttributeName): 
        try: 
            print " Tablename  : ",Tablename  
            self.cur.execute("CREATE TABLE "+str(Tablename)+"( time TIMESTAMP,geom GEOMETRY (PointZ, 4326),"+str(AttributeName)+" NUMERIC);")
            print "Spatial Table created successfully"
            self.conn.commit()    

        except psycopg2.Error as e:
            print e
    
    def AddColumnInTable(self,Tablename,Colname,Datatype):    
        try:
            self.cur.execute("ALTER TABLE "+str(Tablename)+" ADD COLUMN "+Colname+" "+Datatype+";")
            print "Spatial Table created successfully"
            self.conn.commit()    

        except psycopg2.Error as e:
            print e
    
    #### Drop Table    
    def DropTable(self,Tablename):    
        try:
            self.cur.execute("DROP TABLE "+str(Tablename)+";")
            print "Table Deleted successfully"
            self.conn.commit()   

        except psycopg2.Error as e:
            print e
   
    #### Add Data in Table    
    def AddData(self,name,age):
     
        try:  
            self.cur.execute("INSERT INTO Test(NAME,AGE) VALUES( '''"+str(name)+"''',"+str(age)+" );")
            print "Data Added successfully"      
            self.conn.commit()

        except psycopg2.Error as e:
            print e
    
    #### Add Spatial Data in Table    
    def AddSpatialData(self,tablename,time,lat,lon,alt,value):
        try:
            #self.cur.execute("INSERT INTO "+str(tablename)+" VALUES("+str(time)+",ST_GeomFromText('POINT("+str(lat)+" "+str(lon)+" "+str(alt)+")',4326),"+str(value)+","+str(unit)+");")
            print "tablename",tablename
            self.cur.execute("INSERT INTO "+str(tablename)+" VALUES('2004-10-19 10:23:54',ST_GeomFromText('POINT("+str(lat)+" "+str(lon)+" "+str(alt)+")',4326),"+str(value)+");")
            print "Spatial Data Added successfully"      
            self.conn.commit()

        except psycopg2.Error as e:
            print e

      
    ### DataBase Connection Disconnected
    def DatabaseClosed(self):
        try: 
            self.conn.close() 
            self.cur.close() 

        except psycopg2.Error as e:
            print e


    def reset_merra_db(self):
        """ 
        Function name : reset_merra_db

        Description   : This function will wipe out every info saved in merra DB (Are you sure to make MERRA DB dumb ?)

        Parameters    : 
         
        Return        : 
        """

        try:
            self.cur.execute("SELECT table_schema,table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_schema,table_name")

            rows = cur.fetchall()
            for row in rows:
                print "dropping table: ", row[1]
                cur.execute("drop table " + row[1] + " cascade")
 

            self.cur.close()
            self.conn.close()

        except:
            print "Error: ", sys.exc_info()[1]

    
    
