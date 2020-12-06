import mysql.connector

class DatabaseManager:
    """
    This class defines a database manager for opening connections, 
    closing connections, and querying the tables within the database.
    """

    def __init__(self, host, user, password, database):
        """
        Parameters
        ----------
        host: str
            The database host.
        user: str
            The database user.
        password: str
            The database password.
        database: str
            The database name.
        """

        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

    def close(self):
        """
        Closes the open connection to the database
        Users of this class should **always** call close when they are
        done with this class so it can clean up the DB connection.
        """

        self.db.close()

    def connect(self):
        """
        Opens a connection to the database.
        """
        
        self.db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def execute(self, query, values):
        """
        Executes the provided query with the value(s) on the 
        database.

        Parameters
        ----------
        query: str
            A sql insert query.
        values: tuple
            Values to be inserted to the table
        """

        cursor = self.db.cursor()

        if type(values) is list:
            cursor.executemany(query, values)
        elif type(values) is None:
            cursor.execute(query)
        else:
            cursor.execute(query, values)

        self.db.commit()

    def check_table_exists(self, tablename):
        """
        Checks if a table exists within the database.

        tablename: str
            Name of the table to check if exists.
        """

        cursor = self.db.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_name = '{0}'
            """.format(tablename.replace('\'', '\'\'')))

        if cursor.fetchone()[0] == 1:
            return True

        return False