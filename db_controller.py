import sqlite3

class Database:
    def __init__(self, db_name = "database.db"):
        self.conn = sqlite3.connect(database=db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._init_user_table()
        
    def _init_user_table(self):
        try:
            self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER UNIQUE,
                    username TEXT,
                    nickname TEXT
                )
            """)
            self.conn.commit()
        except Exception as err:
            print(f"Error creating initial users table ->\n{err}")
            
    def _clear_tables(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = self.cursor.fetchall()

        for table in tables:
            table_name = table[0]
            self.cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
            
        self.conn.commit()
        
    def create_new_user(self, id : int, username : str):
        try:
            self.cursor.execute(f"INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?);", (id, username))
            self.conn.commit()
        except Exception as err:
            print(f"Error inserting user ->\n{err}")
    
    def get_user_id_by_username(self, username : str) -> int | None:
        try:
            self.cursor.execute(f"SELECT user_id FROM users WHERE username=?", (username,))
            result = self.cursor.fetchone()
        
            if result:
                return result[0]  
            else:
                return None 
        except Exception as err:
            print(f"Error getting user ->\n{err}")
            
    def close(self):
        self.conn.close()