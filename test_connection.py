print("Scrpit Added")
import pymysql

try:
    print("Trying to connect")
    conn = pymysql.connect(
        host = "127.0.0.1",
        user = "smart_task",
        password = "task123",
        database = "smart_task_manager"
    )
    print("Connecting")
    print("Connection Successfull")
    
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")

    for table in cursor.fetchall():
        print(table)

    cursor.close()
    conn.close()

except pymysql.Error as err:
    print(f"X Error: {err}")
