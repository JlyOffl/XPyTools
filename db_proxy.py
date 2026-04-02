from db_utils import *
import os

class DBProxy:
    def __init__(self):
        #self.db = MySQLDatabase(host="71.56.95.208", user="rajkumar", password="rose", database="TwitterExplorer")

        # Prepare SSL certificate path
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ssl_path = os.path.join(base_dir, "ssl", "aiven-ca.pem")

        # Aiven MySQL connection (correct host, port, SSL)
        self.db = MySQLDatabase(
            host="fireflyapp-db-firefly-3ba2.j.aivencloud.com",
            user="avnadmin",
            password="AVNS_Ny5_tVz668cRzFC1YNV",
            database="defaultdb",
            port=18245,
            ssl_ca=ssl_path,
        )
    
    def isUserRecord(self, user):
        ret = False
        self.db.connect()
        select_query = "SELECT * FROM Following WHERE UserName = '" + user + "'"
        results = self.db.fetch_results(select_query)
        #print(results)
        if(results and results[0][3] == 1):
            ret = True
        self.db.close()
        return ret
    
    def GetSettingValue(self, key):
        self.db.connect()
        select_query = "SELECT * FROM Settings"
        results = self.db.fetch_results(select_query)
        ret = ''
        for row in results:
            if(row[1] == key):
                ret = row[2]
                break
        
        self.db.close()
        return ret
        
    def GetFollowingList(self):
        self.db.connect()
        select_query = "SELECT username FROM Following ORDER BY 1 ASC"
        results = self.db.fetch_results(select_query)
        ret = []
        for row in results:
            ret.append(row[0])
        
        self.db.close()
        #print(ret)
        return ret
    
    def GetActiveSpaces(self):
        self.db.connect()
        select_query = "SELECT SpaceUrl FROM TwitterSpacesMain WHERE isActive = 1 ORDER BY 1 DESC"
        results = self.db.fetch_results(select_query)
        ret = []
        for row in results:
            ret.append(row[0])
        
        self.db.close()
        return ret
        
    def saveSpaceToDb(self, spaceId, username, audio_url, title, user_name):
        self.db.connect()
        table = 'TwitterSpacesMain'
        data = {
            'spaceUrl': spaceId,
            'HostName': username,
            'M3U8Url': audio_url,
            'SpaceTitle' : title,
            'HostDisplayName' : user_name,
            'IsActive' : "1",
            'IsHost' : "1"
        }
        ret = self.db.execute_insert(table, data)
        self.db.close()
        return ret
        
    def UpdateFollowerDisplayName(self, username, displayname):
        if not username:
            return
    
        self.db.connect()
    
        try:
            # 1. Check if user exists
            select_sql = "SELECT ID, DisplayName FROM Following WHERE UserName = %s"
            rows = self.db.fetch_results(select_sql, (username,))
    
            if rows:
                # user exists
                _, current_displayname = rows[0]
    
                # update only if displayname is empty
                if (current_displayname is None or current_displayname == "") and displayname:
                    update_sql = "UPDATE Following SET DisplayName = %s WHERE UserName = %s"
                    self.db.execute_query(update_sql, (displayname, username))
    
            else:
                # user does not exist → insert manually with MAX + 1
                insert_sql = """
                    INSERT INTO Following (ID, UserName, DisplayName)
                    SELECT IFNULL(MAX(ID), 0) + 1, %s, %s
                    FROM Following;
                """
                self.db.execute_query(insert_sql, (username, displayname))
    
        finally:
            self.db.close()

    def DeleteFollower(self, username):
        if not username:
            return

        self.db.connect()
        delete_query = (
            "DELETE FROM Following "
            "WHERE UserName = %s "
            "AND (MainUser IS NULL OR MainUser <> 1)"
        )
        self.db.execute_query(delete_query, (username,))
        self.db.close()

    def CloseSpace(self, spaceId):
        self.db.connect()
        update_query = "UPDATE TwitterSpacesMain SET IsActive = 0 WHERE SpaceUrl = '" + spaceId + "'"
        self.db.execute_query(update_query)
        self.db.close()
        #print("Space: ", spaceId, " Closed")

    def UpsertFollower(self, username):
        self.db.connect()
        try:
            # Check if username already exists (case insensitive)
            check_sql = "SELECT ID FROM Following WHERE LOWER(UserName) = LOWER(%s)"
            existing = self.db.fetch_results(check_sql, (username,))
            
            # If user already exists, do nothing
            if existing:
                return 0
            
            insert_sql = f"""
                INSERT INTO Following (ID, UserName) 
                SELECT IFNULL(MAX(ID), 0) + 1, %s
                FROM Following
            """
            
            result = self.db.execute_query(insert_sql, (username,))
            return result
            
        finally:
            self.db.close()
