import bcrypt, sqlite3, pandas as pd

from app_model.db import conn
from app_model.users import add_user, get_user
from app_model.schema import create_user_table

#hashing using bcrypt
def hash_generation(password):
    salt = bcrypt.gensalt()
    byte_psw = password.encode('utf-8')
    hashed_psw = bcrypt.hashpw(byte_psw, salt)

    return hashed_psw.decode('utf-8')

#Hash validation against the password
def is_hash_valid(password, hash):
    hash_ = hash.encode('utf-8')
    byte_psw = password.encode('utf-8')
    is_valid = bcrypt.checkpw(byte_psw, hash_)
    return is_valid

#User registration
def register_user(conn):
    name = input("Please enter your name: > ")
    password = input("Please enter your password: > ")
    hash = hash_generation(password)
    add_user(conn, name, hash)



#user log in
def login_user(conn):
    name = input("Please enter your username: >  ")
    password = input("Please enter your password: > ")
    id, user_name, user_hash = get_user(conn, name)
    print(f"Welcome {user_name}!!")
    if name == user_name and is_hash_valid(password, user_hash):
        print("Logged in successfully")
    else:
        print("Incorrect username or password! Please try again.")
        return True
    return False

#Main menu
def main():
    while True:
        print("Welcome to the User Authentication System")
        print("Please select an option: ")
        print("1. Register New User")
        print("2. Login Existing User")
        print("3. Exit")

        choice = input(": > ")

        if choice == "1":
            register_user(conn)
        elif choice == "2":
            login_user(conn)
        elif choice == "3":
            print("Exiting User Authentication System. Goodbye!")
            break
        else:
            print("Option not recognised. Please try again.")



def migrate_cyber_incidents(conn):
    data = pd.read_csv('DATA/cyber_incidents.csv')
    data.to_sql('cyber_incidents', conn)
def migrate_datasets_metadata(conn):
    data = pd.read_csv('DATA/datasets_metadata.csv')
    data.to_sql('datasets_metadata', conn)

def migrate_it_tickets(conn):
    data = pd.read_csv('DATA/it_tickets.csv')
    data.to_sql('it_tickets', conn)


def get_all_cyber_incidents(conn):
    sql = 'SELECT * FROM cyber_incidents'
    data = pd.read_sql(sql, conn)
    conn.close()
    return(data)

def get_all_datasets_metadata(conn):
    sql = 'SELECT * FROM datasets_metadata'
    data = pd.read_sql(sql, conn)
    conn.close()
    return(data)

def get_all_it_tickets(conn):
    sql = 'SELECT * FROM it_tickets'
    data = pd.read_sql(sql, conn)
    conn.close()
    return(data)

#if __name__ == "__main__":
 #   main()

conn = sqlite3.connect("DATA/project_data.db")

def migrate_cyber_incidents(conn):
    data = pd.read_csv('DATA/cyber_incidents.csv')
    data.to_sql('cyber_incidents', conn, if_exists='replace', index=False)

def migrate_datasets_metadata(conn):
    data = pd.read_csv('DATA/datasets_metadata.csv')
    data.to_sql('datasets_metadata', conn, if_exists='replace', index=False)

def migrate_it_tickets(conn):
    data = pd.read_csv('DATA/it_tickets.csv')
    data.to_sql('it_tickets', conn, if_exists='replace', index=False)


def migrate_it_user(conn):
    data = pd.read_csv(
        "DATA/user_data.txt",
        names=["username", "password_hash"],
        header=None
    )

    data.to_sql(
        "users",
        conn,
        if_exists="append",
        index=False
    )
if __name__ == "__main__":
    main()

# Close the connection
conn.close()
