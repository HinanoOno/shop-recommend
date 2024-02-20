import mysql.connector

# MySQL接続情報
config = {
    "user": "posse",
    "password": "password",
    "host": "mysql",
    "database": "website",
    "port": 3306,
}


def connect_to_db():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("USE website")
    return connection, cursor
