import mysql.connector
import time

failover_hosts = [
    {
        "user": "username",
        "password": "secret",
        "host": "10.10.10.1",
        "port": 4000,
        "database": "databasename",
    },
    {
        "user": "username",
        "password": "secret",
        "host": "10.10.10.2",
        "port": 4000,
        "database": "databasename",
    },
    {
        "user": "username",
        "password": "secret",
        "host": "10.10.10.3",
        "port": 4000,
        "database": "databasename",
    }
]


def connect_to_database():
    try:
        connection = mysql.connector.connect(
            user="username",
            password="secret",
            host="10.10.10.1",
            port="4000",
            database="databasename",
            failover=failover_hosts,
        )
        return connection
    except mysql.connector.errors.InterfaceError:
        raise


db_connection = connect_to_database()

while True:

    try:
        cursor = db_connection.cursor()

        query = ("SELECT NOW()")

        cursor.execute(query)

        for (x) in cursor:
            print(f"Database host: {db_connection._host} SELECT NOW() output: {x}")

        cursor.close()
        time.sleep(0.5)
    except mysql.connector.errors.OperationalError as e:
        print(f"Connection error: {e}")
        time.sleep(0.5)
        try:
            db_connection = connect_to_database()
        except mysql.connector.errors.InterfaceError:
            time.sleep(0.5)
            pass
    except mysql.connector.errors.InterfaceError as e:
        print(f"All mysql hosts down?: {e}")
        time.sleep(0.5)
        try:
            db_connection = connect_to_database()
        except mysql.connector.errors.InterfaceError:
            time.sleep(0.5)
            pass


db_connection.close()
