import mysql.connector

def get_db_connection():
    """
    Creates and returns a connection to the MySQL database
    """
    connection = mysql.connector.connect(
        host='localhost',
        user='root',         # Replace with your MySQL username
        password='varsha@123',         # Replace with your MySQL password
        database='lms_database' # Replace with your database name
    )
    return connection