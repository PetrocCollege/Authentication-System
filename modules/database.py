import sqlite3

from modules.queries import * 



connection = sqlite3.connect("database/users.db", check_same_thread=False)
cursor = connection.cursor()

class Authentication: 

    @staticmethod
    def initialise() -> None: 

        cursor.execute(SQL_USER_TABLE)
        connection.commit()
    
    @staticmethod
    def add_user(data: tuple):
        cursor.execute("INSERT INTO users VALUES (?, ?, ?)", data)
        connection.commit()
    
    @staticmethod 
    def check_user_id(user_id: str):
        query = cursor.execute("SELECT * FROM users WHERE user_id = (?)", (user_id,))
        return (True if query.fetchall() else False)

    @staticmethod 
    def check_pin(user_id: str, pin: str):
        query = cursor.execute("SELECT * FROM users WHERE user_id = (?) AND pin = (?)", (user_id, pin))
        return (True if query.fetchall() else False)
    
    @staticmethod 
    def fetch_password(user_id: str, pin: str):
        query = cursor.execute("SELECT * FROM users WHERE user_id = (?) AND pin = (?)", (user_id, pin))
        password = query.fetchone()[2]
        return password 
    