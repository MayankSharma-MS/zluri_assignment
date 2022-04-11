import psycopg2
from retrying import retry
from psycopg2 import sql, extras


class DBConnection:
    __shared_instance = None

    @staticmethod
    @retry(stop_max_attempt_number=3, stop_max_delay=6000, wait_fixed=1000)
    def get_connection():
        if not DBConnection.__shared_instance:
            DBConnection.__shared_instance = DBConnection.__create_connection()
        return DBConnection.__shared_instance

    @staticmethod
    def __create_connection():
        connection = psycopg2.connect(
            host='localhost',
            database='zluriTransactionDB',
            user='zluriUser',
            password='jarvis',
            port=5455
        )
        connection.set_session(autocommit=True)
        return connection


class DBUtils:
    cursor = None
    connection_object = None

    def __init__(self):
        self.connection_object = DBConnection.get_connection()
        self.get_cursor()

    @retry(stop_max_attempt_number=3, stop_max_delay=6000, wait_fixed=100)
    def get_cursor(self):
        try:
            self.cursor = self.connection_object.cursor()
        except psycopg2.InterfaceError as e:
            self.connection_object = DBConnection.get_connection()

    @retry(stop_max_attempt_number=3, stop_max_delay=6000, wait_fixed=1000)
    def execute_query(self, create_query):
        try:
            self.cursor.execute(create_query)
        except psycopg2.InterfaceError as e:
            self.get_cursor()

    def batch_insert(self, z_df, table_name):
        # dataframe -> list of tuples
        tuples = [tuple(x) for x in z_df.to_numpy()]
        # Comma-separated dataframe columns
        cols = ','.join(list(z_df.columns))
        upsert_query = sql.SQL(f"INSERT INTO {table_name}({cols}) VALUES %s ON CONFLICT(sku) DO UPDATE SET (name, "
                               f"description) = (EXCLUDED.name, EXCLUDED.description)")
        try:
            extras.execute_values(self.cursor, upsert_query, tuples)
            self.connection_object.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            self.connection_object.rollback()
        print("batch_insert() done")
