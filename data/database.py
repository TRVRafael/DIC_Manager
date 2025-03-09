import sqlite3

class Database:
    def __init__(self, db_name = "data/database.db"):
        self.conn = sqlite3.connect(database=db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

        self._init_user_table()
        self._init_chats_table()
        
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

    def _init_chats_table(self):
        try:
            self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS chats (
                    chat_id TEXT PRIMARY KEY,
                    chat_title TEXT
                )
            """)
            self.conn.commit()
        except Exception as err:
            print(f"Error creating initial chats table ->\n{err}")
            
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

    def create_new_chat(self, chat_id: str, chat_title: str):
        try:
            self.cursor.execute(f"INSERT OR IGNORE INTO chats (chat_id, chat_title) VALUES (?, ?);", (chat_id, chat_title))
            self.conn.commit()
        except Exception as err:
            print(f"Error inserting chat ->\n{err}")

    def delete_chat_by_id(self, chat_id: str):
        try:
            self.cursor.execute(f"DELETE FROM chats WHERE chat_id=?;", (chat_id,))
            self.conn.commit()
        except Exception as err:
            print(f"Error deleting chat ->\n{err}")

    def get_all_chats(self):
        try:
            self.cursor.execute("SELECT chat_id, chat_title FROM chats;")
            result = self.cursor.fetchall()
            return result
        except Exception as err:
            print(f"Error fetching all chats ->\n{err}")
            return []
            
    def close(self):
        self.conn.close()
