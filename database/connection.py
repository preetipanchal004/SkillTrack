import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="PRIT@123",
        database="skilltrack_db"
    )

    return connection