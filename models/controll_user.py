from models.database import connect_db, password_hasher

def create_user_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    phone TEXT,  
                    email TEXT UNIQUE,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
                """)
    conn.commit()
    conn.close()

def login(email, password):
    password_hash = password_hasher(password)
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
                      SELECT * FROM users WHERE email=? AND password_hash=? 
                      """,(email, password_hash),)
    user = cur.fetchone()
    if user:
        cur.execute("UPDATE users SET last_login=CURRENT_TIMESTAMP WHERE id=?",(user[0],))
        conn.commit()
        
    conn.close()
    return user
    
    
def change_password(user_id, password, new_password):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT password_hash FROM users WHERE id=?",(user_id,))
    stored_password = cur.fetchone()
    if not stored_password or stored_password[0] != password_hasher(password):
        conn.close()
        return False
    new_hash = password_hasher(new_password)
    cur.execute("UPDATE users SET password_hash=? WHERE id=?",(new_hash,user_id))
    conn.commit()
    conn.close()
    return True


def register_user_db(first_name, last_name, phone, email, password):
    password_hash = password_hasher(password)
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
                INSERT INTO users(first_name, last_name, phone, email, password_hash)
                VALUES(?,?,?,?,?)
                """, (first_name, last_name, phone, email, password_hash))
    conn.commit()
    conn.close()
    

def get_user_by_id(user_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cur.fetchone()
    conn.close()
    return user