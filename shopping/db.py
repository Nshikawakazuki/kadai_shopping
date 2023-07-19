import os, psycopg2, string, random, hashlib

def get_connection():
    url = os.environ['DATABASE_URL']
    print(url)
    connection = psycopg2.connect(url)
    return connection

def get_salt():
    charset = string.ascii_letters + string.digits
    
    salt = ''.join(random.choices(charset, k=30))
    return salt

def get_hash(password, salt):
    b_pw = bytes(password, 'utf-8')
    b_salt = bytes(salt, 'utf-8')
    hashed_password = hashlib.pbkdf2_hmac('sha256', b_pw, b_salt, 1246).hex()
    return hashed_password

def insert_user(user_name, mail, password):
    sql = 'INSERT INTO login1 VALUES (default, %s, %s, %s,%s)'
    salt = get_salt()
    hashed_password = get_hash(password, salt)
    
    try :
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (user_name, mail, hashed_password, salt))
        count = cursor.rowcount 
        connection.commit()
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()
        
    return count

def login(user_name, password):
    sql = 'SELECT hashed_password, salt FROM login1 WHERE name = %s'
    flg = False

    try :
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (user_name, ))
        user = cursor.fetchone()

        if user != None:
            salt = user[1]

            hashed_password = get_hash(password, salt)

            if hashed_password == user[0]:
                flg = True
    except psycopg2.DatabaseError:
        flg = False
    finally :
        cursor.close()
        connection.close()
    
    return flg

def insert_merchan(merchan_name, price):
    sql = 'INSERT INTO merchan VALUES (default, %s, %s)'
    
    try :
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (merchan_name, price))
        count = cursor.rowcount 
        connection.commit()
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()
        
    return count

def admin_login(user_name, password):
    sql = "SELECT hashed_password, salt FROM shop_user WHERE name = 'hatakeyama'"
    flg = False
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (user_name))
        admin = cursor.fetchone()
        if admin != None:
            salt = admin[1]
        hashed_password = get_hash(password, salt)
        if hashed_password == admin[0]:
                flg = True
    except psycopg2.DatabaseError:
        flg = False
    finally:
        cursor.close()
        connection.close()
    return flg