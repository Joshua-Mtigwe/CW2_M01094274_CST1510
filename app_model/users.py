#add user
def add_user(conn, username, hash, twofa_secret):
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO users (username, password_hash, twofa_secret)
        VALUES (?, ?, ?)
        """,
        (username, hash, twofa_secret)
    )
    conn.commit()

#user migration
def migration_user(conn):
    with open ('DATA/user_data.txt', "r") as f:
        users = f.readlines()

    for user in users:
        name, hash =user.strip().split(",")
        add_user(conn,name, hash)
                

#if __name__ == "__main__":
#    main()

def get_all_users(conn):
    cur = conn.cursor()
    sql = '''SELECT * FROM users'''
    conn.execute(sql)
    users  = cur.fetchall()
    return (users)

def get_user(conn, name):
    cur = conn.cursor()
    sql = '''SELECT id, username, password_hash, twofa_secret FROM users WHERE username = ?'''
    param = (name,)
    cur.execute(sql, param)
    user  = cur.fetchone()
    return(user)

def update_user(conn, old_name, new_name):
    cur = conn.cursor()
    sql = '''UPDATE users SET username = ? WHERE username = ?'''
    param = (new_name, old_name)
    cur.execute(sql, param)
    conn.commit()
    conn.close()

def delete_user(conn, user_name):
    cur = conn.cursor()
    sql = '''DELETE FROM users WHERE username = ?'''
    param = (user_name,)
    cur.execute(sql, param)
    conn.commit()
    conn.close()


