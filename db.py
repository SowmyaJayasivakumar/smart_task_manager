import pymysql

def get_connection():
    return pymysql.connect(
        host = 'localhost',
        user = 'smart_task',
        password = 'task123',
        database = 'smart_task_manager'
    )