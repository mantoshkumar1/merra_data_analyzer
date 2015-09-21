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
    def __init__(self,DataBaseName,Username,Password,hostIP,port):
        """
        Function name : __init__
        
        Description   : Initialize MerraDatabase Class Configuration
            
        Parameters    : DataBaseName,Username,Password,hostIP,port
    
        Return        :None
        """          
        self.DataBaseName=DataBaseName
        self.Username=Username
        self.Password=Password
        self.hostIP=hostIP
        self.port=port
        self.tableforfilesadded=None
        print "MerraDatabase INIT"
    
    def DatabaseConnection(self):
        """
        Function name : DatabaseConnection
        
        Description   : Open database connection
            
        Parameters    : None
    
        Return        : None
        """         
        self.conn = psycopg2.connect(database=self.DataBaseName, user=self.Username, password=self.Password,host=self.hostIP, port=self.port)
        self.cur = self.conn.cursor()

    def CreateTable(self,Tablename): 
        """
        Function name : CreateTable
        
        Description   : Create table in Database
            
        Parameters    : table name
    
        Return        : None
        """             
        self.cur.execute("CREATE TABLE "+str(Tablename)+"( NAME  TEXT,AGE   INT );")
        print "Table created successfully"
        self.conn.commit()


    def check_If_Table_Exist(self,Tablename):    
        """
        Function name : check_If_Table_Exist
        
        Description   : Check if a table exist in Data base or not
            
        Parameters    : table name
    
        Return        : Flag :True if exist False if not
        """         
        self.cur.execute("SELECT relname FROM pg_class WHERE relname ='"+Tablename+"';")
        self.conn.commit()
        result=self.cur.fetchone()
        print result
        if result ==None:
            return False
        else:
            return True

    def CreateTableforFiles(self,Tablename):    
        """
        Function name : CreateTableforFiles
        
        Description   : Create a Table in Database which store info about HDF files
            
        Parameters    : table name
    
        Return        : Flag :True if exist False if not
        """        
        self.cur.execute("CREATE TABLE "+str(Tablename)+"( FileName  TEXT);")
        print Tablename+" Table created successfully"
        self.conn.commit()
        self.tableforfilesadded=Tablename;
        
    #### Add Filename  in Table    
    def AddfilesnameinTable(self,filename):
        """
        Function name : AddfilesnameinTable
        
        Description   : Add HDF files names from which data is successfully added in Database
            
        Parameters    : File name
    
        Return        : None
        """          
        self.cur.execute("INSERT INTO "+self.tableforfilesadded+"(FileName) VALUES('"+str(filename)+"');")
        print filename+" Added successfully"      
        self.conn.commit()

    
    def file_exist_in_db(self,filename):
        """ 
        Function name : file_exist_in_db

        Description   : Check whether this file(file_name) has already been used to populate the DB or not

        Parameters    : file_name (String, name of file)
         
        
        Return        : If file_name has already been used to populate DB, returns True
                        else return False
        """
        self.cur.execute("select FileName from "+self.tableforfilesadded+" where FileName='"+filename+"';")
        self.conn.commit()
        result=self.cur.fetchone()
        print result
        if result ==None:
            return False
        else:
            return True
        

    def CreatePostGISExtension(self): 
        """
        Function name : CreatePostGISExtension
        
        Description   : Create a PostGIS extension for storing spatial data            
        
        Parameters    : None
        
        Return        : None
        """             
        self.cur.execute("CREATE EXTENSTION POSTGIS;")
        self.conn.commit() 
        
          
    def Create3DTable(self,Tablename,AttributeName): 
        """
        Function name : CreateSpatialTable
        
        Description   : Create a spatial table for storing spatial data            
        
        Parameters    : Table name and Attribute Name
        
        Return        : None
        """
        #print " Tablename  : ",Tablename  
        self.cur.execute("CREATE TABLE "+str(Tablename)+"( time TIMESTAMP,geom GEOMETRY (PointZ, 4326),"+str(AttributeName)+" NUMERIC);")
        #print "Spatial Table created successfully"
        self.conn.commit()    

    def Create2DTable(self,Tablename,AttributeName): 
        """
        Function name : CreateSpatialTable
        
        Description   : Create a spatial table for storing spatial data            
        
        Parameters    : Table name and Attribute Name
        
        Return        : None
        """
        #print " Tablename  : ",Tablename  
        self.cur.execute("CREATE TABLE "+str(Tablename)+"( time TIMESTAMP,geom GEOMETRY (Point,4326),"+str(AttributeName)+" NUMERIC);")
        #print "Spatial Table created successfully"
        self.conn.commit()  
            
   
    def DropTable(self,Tablename): 
        """
        Function name : DropTable
        
        Description   : Delete a table from Database           
        
        Parameters    : Table name 
        
        Return        : None
        """           
        self.cur.execute("DROP TABLE "+str(Tablename)+";")
        self.conn.commit()   
   
    
   
    def Add3DData(self,tablename,time,lat,lon,alt,value):
        """
        Function name : AddSpatialData
        
        Description   : Add Spatial Data in Table       
        
        Parameters    : tablename,time,lat,lon,alt,value
        
        Return        : None
        """
        print tablename
        print time
        print lat
        print lon
        print alt
        print value        
        #self.cur.execute("INSERT INTO "+str(tablename)+" VALUES("+str(time)+",ST_GeomFromText('POINT("+str(lat)+" "+str(lon)+" "+str(alt)+")',4326),"+str(value)+","+str(unit)+");")
        self.cur.execute("INSERT INTO "+str(tablename)+" VALUES('"+str(time)+"',ST_GeomFromText('POINT("+str(lat)+" "+str(lon)+" "+str(alt)+")',4326),"+str(value)+");")
        print "3D Data Added successfully"      
        self.conn.commit()


    def Add2DData(self,tablename,time,lat,lon,value):
        """
        Function name : AddSpatialData
        
        Description   : Add Spatial Data in Table       
        
        Parameters    : tablename,time,lat,lon,alt,value
        
        Return        : None
        """
        print tablename
        print time
        print lat
        print lon
        print value
        #self.cur.execute("INSERT INTO "+str(tablename)+" VALUES("+str(time)+",ST_GeomFromText('POINT("+str(lat)+" "+str(lon)+" "+str(alt)+")',4326),"+str(value)+","+str(unit)+");")
        self.cur.execute("INSERT INTO "+str(tablename)+" VALUES('"+str(time)+"',ST_GeomFromText('POINT("+str(lat)+" "+str(lon)+")',4326),"+str(value)+");")
        print "2D Data Added successfully"      
        self.conn.commit()
        
        
    def DatabaseClosed(self):  
        """
        Function name : DatabaseClosed
        
        Description   : To Disconnect the DataBase Connection      
        
        Parameters    : None
        
        Return        : None
        """        
        self.conn.close()  


    
    
