import mysql.connector
from mysql.connector import Error

class MySQLDatabase:
    def __init__(self, host, user, password, database, port=3306, ssl_ca=None):
        """Initialize the database connection."""
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.ssl_ca = ssl_ca
        self.connection = None

    def connect(self):
        """Connect to the MySQL database."""
        try:
            connect_kwargs = {
                "host": self.host,
                "user": self.user,
                "password": self.password,
                "database": self.database,
                "port": self.port,
            }

            # If an SSL CA is provided (Aiven case), enable SSL
            if self.ssl_ca:
                connect_kwargs["ssl_ca"] = self.ssl_ca
                connect_kwargs["ssl_disabled"] = False

            self.connection = mysql.connector.connect(**connect_kwargs)

            if self.connection.is_connected():
                pass
                # print("Connected to MySQL database")
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")

    def fetch_results(self, query, params=None):
        """Fetch results from a query."""
        cursor = None
        results = None
        try:
            if self.connection is None or not self.connection.is_connected():
                print("Not connected to the database.")
                return None

            cursor = self.connection.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
        except Error as e:
            print(f"Error: '{e}'")
        finally:
            if cursor:
                cursor.close()
        return results

    def execute_query(self, query, params=None):
        """Executes a given query with optional parameters."""
        if self.connection is None or not self.connection.is_connected():
            print("Not connected to the database.")
            return 0  # nothing affected
    
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            self.connection.commit()
            affected_rows = cursor.rowcount
            return affected_rows
        except Error as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()
            return 0
        finally:
            cursor.close()


    def generate_insert_statement(self, table, data):
        """
        Generates an SQL INSERT statement.

        :param table: str, name of the table
        :param data: dict, dictionary of column names and values
        :return: str, generated SQL INSERT statement
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        insert_stmt = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        return insert_stmt
    
    def execute_insert(self, table, data):
        """
        Executes an SQL INSERT statement.

        :param table: str, name of the table
        :param data: dict, dictionary of column names and values
        """
        if self.connection is None or not self.connection.is_connected():
            print("Not connected to the database.")
            return

        insert_stmt = self.generate_insert_statement(table, data)
        values = tuple(data.values())
        
        cursor = self.connection.cursor()
        try:
            cursor.execute(insert_stmt, values)
            self.connection.commit()
            affected_rows = cursor.rowcount
            return affected_rows
            # print(f"Record inserted successfully into {table} table")
        except Error as e:
            # print(f"Error: {e}")
            self.connection.rollback()
        finally:
            cursor.close()
                        
    def close(self):
        """Close the database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
