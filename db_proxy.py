import os

from db_utils import MySQLDatabase


class DBProxy:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ssl_path = os.path.join(base_dir, "ssl", "aiven-ca.pem")

        self.db = MySQLDatabase(
            host="fireflyapp-db-firefly-3ba2.j.aivencloud.com",
            user="avnadmin",
            password="AVNS_Ny5_tVz668cRzFC1YNV",
            database="defaultdb",
            port=18245,
            ssl_ca=ssl_path,
        )

    def GetSettingValue(self, key):
        self.db.connect()
        select_query = "SELECT * FROM Settings"
        results = self.db.fetch_results(select_query)
        ret = ""
        for row in results:
            if row[1] == key:
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
        return ret

    def UpdateFollowerDisplayName(self, username, displayname):
        if not username:
            return

        self.db.connect()
        try:
            select_sql = "SELECT ID, DisplayName FROM Following WHERE UserName = %s"
            rows = self.db.fetch_results(select_sql, (username,))

            if rows:
                _, current_displayname = rows[0]
                if (current_displayname is None or current_displayname == "") and displayname:
                    update_sql = "UPDATE Following SET DisplayName = %s WHERE UserName = %s"
                    self.db.execute_query(update_sql, (displayname, username))
            else:
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

    def UpsertFollower(self, username):
        self.db.connect()
        try:
            check_sql = "SELECT ID FROM Following WHERE LOWER(UserName) = LOWER(%s)"
            existing = self.db.fetch_results(check_sql, (username,))
            if existing:
                return 0

            insert_sql = """
                INSERT INTO Following (ID, UserName)
                SELECT IFNULL(MAX(ID), 0) + 1, %s
                FROM Following
            """

            result = self.db.execute_query(insert_sql, (username,))
            return result

        finally:
            self.db.close()
