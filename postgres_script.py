import psycopg2
from psycopg2 import sql

# Connect to PostgreSQL Database
def connect_to_db():
    try:
        connection = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='Football032!',
            host='localhost',  # or your database host
            port='5432'  # default PostgreSQL port
        )
        print('Database connection successful')
        return connection
    except Exception as e:
        print(f'Error connecting to database: {str(e)}')

# Create a new table for users
def create_user_table(connection):
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL
        )
    ''')
    connection.commit()
    cursor.close()
    print('User table created successfully')

# Example usage
if __name__ == '__main__':
    # Connect to database
    db_connection = connect_to_db()

    # Create user table
    create_user_table(db_connection)

    # Close the connection
    db_connection.close()
