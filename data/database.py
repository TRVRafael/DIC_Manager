import sqlite3

from config import bot_logger
from bot.utils import get_fancy_name

class Database:
    def __init__(self, db_name = "data/database.db"):
        self.conn = sqlite3.connect(database=db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        
    def _restart_database(self):
        self._clear_tables()
        self._init_chats_table()
        self._init_user_table()
        self._init_division_database()
    
    def _init_division_database(self):
        """
        Inicilização e configuração inicial de tabelas básicas para testes.
        """
        self._init_division_table("em")
        self.create_role('auxiliar', 1, 0, 1, 0, 1, 0)
        self.create_role('sublider', 1, 1, 1, 0, 1, 0)
        self.create_role('vicelider', 1, 1, 1, 1, 1, 1)
        self.create_role('lider', 1, 1, 1, 1, 1, 1)
        self.create_role('core', 1, 1, 1, 1, 1, 1)
        self.create_role('comando', 0, 0, 1, 1, 1, 0)
        self.create_role('comandogeral', 1, 1, 1, 1, 1, 1)
        self.create_role('presidencia', 1, 1, 1, 1, 1, 1)
        
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
            bot_logger.warn(f"Error creating initial users table ->\n{err}")

    def _init_chats_table(self):
        try:
            self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS chats (
                    chat_id TEXT PRIMARY KEY,
                    chat_title TEXT,
                    is_official BOOLEAN
                )
            """)
            self.conn.commit()
        except Exception as err:
            bot_logger.warn(f"Error creating initial chats table ->\n{err}")
            
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
            bot_logger.warn(f"Error inserting user ->\n{err}")
    
    def get_user_id_by_username(self, username : str) -> int | None:
        try:
            self.cursor.execute("SELECT user_id, nickname FROM em WHERE username=?;", (username,))
            result = self.cursor.fetchone()
            
            if result:
                return result
            else:
                return None
        except Exception as err:
            bot_logger.info(f"DB - Error getting User id by username ({username}) ->\n{err}")

    def create_new_chat(self, chat_id: str, chat_title: str):
        try:
            self.cursor.execute(f"INSERT OR IGNORE INTO chats (chat_id, chat_title, is_official) VALUES (?, ?, ?);", (chat_id, chat_title, False))
            self.conn.commit()
        except Exception as err:
            bot_logger.warn(f"Error inserting chat ->\n{err}")

    def set_chat_as_official(self, chat_id: str):
        try:
            self.cursor.execute(f"UPDATE chats SET is_official=true WHERE chat_id=?;", (chat_id,))
            self.conn.commit()
        except Exception as err:
            bot_logger.warn(f"Error updating chat ->\n{err}")

    def delete_chat_by_id(self, chat_id: str):
        try:
            self.cursor.execute(f"DELETE FROM chats WHERE chat_id=?;", (chat_id,))
            self.conn.commit()
        except Exception as err:
            bot_logger.warn(f"Error deleting chat ->\n{err}")

    def get_all_chats(self):
        try:
            self.cursor.execute("SELECT chat_id, chat_title, is_official FROM chats;")
            result = self.cursor.fetchall()
            return result
        except Exception as err:
            bot_logger.warn(f"Error fetching all chats ->\n{err}")
            return []
        
    def get_chat_by_id(self, chat_id: str):
        try:
            self.cursor.execute(f"SELECT chat_id, chat_title, is_official FROM chats WHERE chat_id=?;", (chat_id,))
            result = self.cursor.fetchone()
            return result
        except Exception as err:
            bot_logger.warn(f"Error getting chat ->\n{err}")
        
    def _init_division_table(self, table_name : str) -> None:
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
            bot_logger.warn(f"Error creating division table ->\n{err}")
            
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
            bot_logger.warn(f"Error creating division role table ->\n{err}")
            
    def create_role(self, role_name, info, delete, invite, rescrict, pin, promote):
        try:
            self.cursor.execute(f"INSERT OR IGNORE INTO em_roles (role_name, can_change_info, can_delete_messages, can_invite_users, can_restrict_members, can_pin_messages, can_promote_members) VALUES (?, ?, ?, ?, ?, ?, ?);", (role_name, info, delete, invite, rescrict, pin, promote))
            self.conn.commit()
        except Exception as err:
            bot_logger.warn(f"Error creating role ->\n{err}")
            
    def get_role_permissions(self, role_name, table_name="em"):
        try:
            self.cursor.execute(f"""
                SELECT can_change_info, can_delete_messages, can_invite_users, 
                    can_restrict_members, can_pin_messages, can_promote_members 
                FROM {table_name}_roles WHERE role_name=?""", (role_name,))
            result = self.cursor.fetchone()

            if result:
                return {
                    "can_change_info": bool(result[0]),
                    "can_delete_messages": bool(result[1]),
                    "can_invite_users": bool(result[2]),
                    "can_restrict_members": bool(result[3]),
                    "can_pin_messages": bool(result[4]),
                    "can_promote_members": bool(result[5]),
                }
            return None
        except Exception as err:
            bot_logger.warning(f"Error fetching role permissions ->\n{err}")
            return None

    def update_role_permission(self, role_name, permission, value, table_name="em"):
        bot_logger.info(f"ROLE: {role_name} / PERMISSION: {permission} / VALUE: {value} / TABLE NAME: {table_name}");
        try:
            self.cursor.execute(f"UPDATE {table_name}_roles SET {permission} = ? WHERE role_name = ?", (int(value), role_name,))
            self.conn.commit()
            return True
        except Exception as err:
            bot_logger.warning(f"Error updating role permission ({permission}) ->\n{err}")
            return False

    async def get_all_roles(self):
        query = """
        SELECT role_name, can_change_info, can_delete_messages, can_invite_users,
            can_restrict_members, can_pin_messages, can_promote_members
        FROM em_roles
        """
        try:
            # Execute the query to fetch all the roles and their permissions
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            # Create a dictionary to hold role names and their permissions
            roles_with_permissions = {}

            # Loop through the fetched rows and populate the dictionary
            for row in rows:
                role_name = row[0]  # The first element in the tuple is the role_name
                permissions = {
                    "can_change_info": bool(row[1]),
                    "can_delete_messages": bool(row[2]),
                    "can_invite_users": bool(row[3]),
                    "can_restrict_members": bool(row[4]),
                    "can_pin_messages": bool(row[5]),
                    "can_promote_members": bool(row[6]),
                }

                # Store the permissions under the corresponding role name
                roles_with_permissions[role_name] = permissions

            return roles_with_permissions

        except Exception as e:
            # Log and handle any errors during the execution
            print(f"Error fetching roles and permissions: {e}")
            return None
    
    async def log_roles_with_permissions(self):
        try:
            # Fetch all roles from the database
            roles = await self.get_all_roles()

            if not roles:
                bot_logger.warning("No roles found in the database.")
                return

            bot_logger.info("📌 Listing all roles and their permissions:")

            for role_name, permissions in roles.items():  # Roles is a dictionary
                perms_dict = {
                    "Permissão 1 (Alterar informações)": permissions.get("can_change_info", False),
                    "Permissão 2 (Excluir mensagens)": permissions.get("can_delete_messages", False),
                    "Permissão 3 (Convidar usuários)": permissions.get("can_invite_users", False),
                    "Permissão 4 (Restringir membros)": permissions.get("can_restrict_members", False),
                    "Permissão 5 (Fixar mensagens)": permissions.get("can_pin_messages", False),
                    "Permissão 6 (Promover membros)": permissions.get("can_promote_members", False),
                }

                # Log the role and its permissions
                bot_logger.info(f"🔹 {get_fancy_name(role_name)}")
                for perm, value in perms_dict.items():
                    emoji = "✅" if value else "❌"
                    bot_logger.info(f"    {emoji} {perm}")

                bot_logger.info("")

        except Exception as err:
            bot_logger.error(f"Error fetching roles and permissions: {err}")
    
    def insert_member_in_division(self, user_id : id, username : str, nickname : str, table_name : str = "em", role = 0):
        try:
            self.cursor.execute(f"SELECT nickname FROM {table_name} WHERE user_id = ?", (user_id,))
            has_nickname = self.cursor.fetchone()

            if has_nickname:
                self.cursor.execute(f"UPDATE {table_name} SET nickname = ?, role = ? WHERE user_id = ?", (nickname, role, user_id,))
            else:
                self.cursor.execute(f"INSERT OR IGNORE INTO {table_name} (user_id, username, nickname, role) VALUES (?, ?, ?, ?);", (user_id, username, nickname, role,))
            
            self.conn.commit()

        except Exception as err:
            bot_logger.warning(f"Error inserting or updating member in division ->\n{err}")
            
    def update_member_role(self, username : str, new_role_id : int, table_name : str = "em"):
        try:
            self.cursor.execute(f"UPDATE {table_name} SET role = ? WHERE username = ?", (new_role_id, username))
            self.conn.commit()
        except Exception as err:
            bot_logger.warn(f"Error updating member role ->\n{err}")
            
    def get_role_id(self, role_name : str, table_name : str = "em"):
        try:
            self.cursor.execute(f"SELECT id FROM {table_name}_roles WHERE role_name=?", (role_name,))
            result = self.cursor.fetchone()
        
            if result:
                return result[0]  
            else:
                return None 
        except Exception as err:
            bot_logger.warn(f"Error getting role id ->\n{err}")
            
    def get_members_list(self):
        try:
            self.cursor.execute(f"SELECT username, role, id, nickname FROM em;")
            result = self.cursor.fetchall()
            return result
        except Exception as err:
            return []
        
    def get_members_by_role(self, role_id):
        try:
            self.cursor.execute(f"SELECT username, nickname FROM em WHERE role=?;", (role_id,))
            result = self.cursor.fetchall()
            return result
        except Exception as err:
            return []
        
    def delete_member(self, username):
        try:
            self.cursor.execute(f"DELETE FROM em WHERE user_id=?;", (user_id,))
            self.conn.commit()
        except Exception as err:
            bot_logger.warn(f"Error deleting chat ->\n{err}")
        
    def get_user_id_from_users_table(self, username):
        try:
            self.cursor.execute(f"SELECT user_id FROM users WHERE username=?", (username,))
            result = self.cursor.fetchone()
        
            if result:
                return result
            else:
                return None 
        except Exception as err:
            bot_logger.warning(f"Error getting role id ->\n{err}")
                
    def close(self):
        self.conn.close()

db_controller = Database()