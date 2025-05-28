import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Leave blank if no password
        database="music_borrowing"
    )
