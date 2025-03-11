import sqlite3

class Database:
    def __init__(self, db_name = "data/database.db"):
        self.conn = sqlite3.connect(database=db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

        self._init_user_table()
        self._init_chats_table()
        
    def _init_division_database(self):
        """
        Inicilização e configuração inicial de tabelas básicas para testes.
        """
        self._create_division_table("em")
        db.create_role('auxiliar', 1, 0, 1, 0, 1, 0)
        db.create_role('sublider', 1, 1, 1, 0, 1, 0)
        db.create_role('vicelider', 1, 1, 1, 1, 1, 1)
        db.create_role('lider', 1, 1, 1, 1, 1, 1)
        
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
        
    def _create_division_table(self, table_name : str) -> None:
        try:
            self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER UNIQUE,
                    username TEXT,
                    nickname TEXT,
                    role INTEGER
                )
            """)
            self.conn.commit()
        except Exception as err:
            print(f"Error creating division table ->\n{err}")
            
        try:
            self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name}_roles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role_name TEXT,
                    can_change_info INTEGER,
                    can_delete_messages INTEGER,
                    can_invite_users INTEGER,
                    can_restrict_members INTEGER,
                    can_pin_messages INTEGER,
                    can_promote_members INTEGER
                )
            """)
            self.conn.commit()
        except Exception as err:
            print(f"Error creating division table ->\n{err}")
            
    def create_role(self, role_name, info, delete, invite, rescrict, pin, promote):
        try:
            self.cursor.execute(f"INSERT OR IGNORE INTO em_roles (role_name, can_change_info, can_delete_messages, can_invite_users, can_restrict_members, can_pin_messages, can_promote_members) VALUES (?, ?, ?, ?, ?, ?, ?);", (role_name, info, delete, invite, rescrict, pin, promote))
            self.conn.commit()
        except Exception as err:
            print(f"Error creating role ->\n{err}")
            
    def get_role_permissions(self, role_name):
        try:
            self.cursor.execute("SELECT can_change_info, can_delete_messages, can_invite_users, can_restrict_members, can_pin_messages, can_promote_members FROM guias_roles WHERE role_name=?", (role_name,))
            result = self.cursor.fetchall()

            if result:
                permissions = [
                    {
                        "can_change_info": True if row[0] == 1 else False,
                        "can_delete_messages": True if row[1] == 1 else False,
                        "can_invite_users": True if row[2] == 1 else False,
                        "can_restrict_members": True if row[3] == 1 else False,
                        "can_pin_messages": True if row[4] == 1 else False,
                        "can_promote_members": True if row[5] == 1 else False
                    }
                    for row in result
                ]
                return permissions[0]
            else:
                return None
        except Exception as err:
            print(f"Error getting role permissions ->\n{err}")
            
    def insert_member_in_division(self, user_id : id, username : str, nickname : str, table_name : str = "em"):
        try:
            self.cursor.execute(f"INSERT OR IGNORE INTO {table_name} (user_id, username, nickname, role) VALUES (?, ?, ?, ?);", (user_id, username, nickname, 0))
            self.conn.commit()
        except Exception as err:
            print(f"Error inserting member in division ->\n{err}")
            
    def update_member_role(self, username : str, new_role_id : int, table_name : str = "em"):
        try:
            self.cursor.execute(f"UPDATE {table_name} SET role = ? WHERE username = ?", (new_role_id, username))
            self.conn.commit()
        except Exception as err:
            print(f"Error updating member role ->\n{err}")
            
    def get_role_id(self, role_name : str, table_name : str = "em"):
        try:
            self.cursor.execute(f"SELECT id FROM {table_name}_roles WHERE role_name=?", (role_name,))
            result = self.cursor.fetchone()
        
            if result:
                return result[0]  
            else:
                return None 
        except Exception as err:
            print(f"Error getting role id ->\n{err}")
            
    def close(self):
        self.conn.close()
        
