from db_utils import *

class DBProxy:
    def __init__(self):
        #self.db = MySQLDatabase(host="71.56.95.208", user="rajkumar", password="rose", database="TwitterExplorer")
        self.db = MySQLDatabase(host="sql5.freesqldatabase.com", user="sql5783149", password="CHejqGpeCt", database="sql5783149")
    
    def isUserRecord(self, user):
        ret = False
        self.db.connect()
        select_query = "SELECT * FROM Following WHERE UserName = '" + user + "'"
        results = self.db.fetch_results(select_query)
        #print(results)
        if(results[0][3] == 1):
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
        if(displayname == None):
            return
        query = "INSERT INTO Following (username, DisplayName) VALUES (%s, %s) ON DUPLICATE KEY UPDATE DisplayName = VALUES(DisplayName)"
        self.db.connect()
        params = (username, displayname)
        self.db.execute_query(query, params)
        self.db.close()
        
    def DeleteFollower(self, username):
        self.db.connect()
        delete_query = (
            "DELETE FROM Following "
            "WHERE UserName='some_user' "
            "AND (MainUser IS NULL OR MainUser <> 1)"
        )
        self.db.execute_query(delete_query)
        self.db.close()
        
    def CloseSpace(self, spaceId):
        self.db.connect()
        update_query = "UPDATE TwitterSpacesMain SET IsActive = 0 WHERE SpaceUrl = '" + spaceId + "'"
        self.db.execute_query(update_query)
        self.db.close()
        #print("Space: ", spaceId, " Closed")
        
