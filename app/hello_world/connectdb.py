import psycopg2

def query_python_code():
    cursor = connection.cursor()
    query = "select * from PythonCode"

    cursor.execute(query)
    python_records = cursor.fetchall()
    print("Print each row and it's columns values")
    for row in python_records:
        print("Id = ", row[0], "\n")

try:
    connection = psycopg2.connect(user="postgres",
                                  password="postgres",
                                  host="db",
                                  port="5432",
                                  database="postgres")
    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    print(connection.get_dsn_parameters(), "\n")
    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")


    cursor.execute("dt")
    record = cursor.fetchone()
    print("Tables - ", record, "\n")
    query_python_code()
except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    # closing database connection.
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")