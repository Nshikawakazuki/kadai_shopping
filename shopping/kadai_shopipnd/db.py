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
    sql = 'INSERT INTO login2 VALUES (default, %s, %s, %s, %s)'
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

def delete_user(id):
    sql = 'DELETE FROM login2 WHERE id = %s'
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (id,))
        count = cursor.rowcount
        connection.commit()
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()
        
    return count

def delete_goods(id):
    sql = 'DELETE FROM merchan WHERE id = %s'
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (id,))
        count = cursor.rowcount
        connection.commit()
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()
        
    return count

def update_goods(id, name, price):
    sql = 'UPDATE merchan SET name = %s,  price = %s WHERE id = %s'
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (name, price, id))
        count = cursor.rowcount
        connection.commit()
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()
    
    return count

def goods_buy(id,number):
    sql = 'UPDATE goods SET stock = stock - %s WHERE id = %s'
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (number,id,))
        count = cursor.rowcount
        connection.commit()
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()
        
    return count

def search_goods(key):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT id, name, price FROM merchan WHERE name LIKE %s'
    key = '%' + key + '%'
    
    cursor.execute(sql, (key,))
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return rows
    
        

def select_all_goods():
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT id, name, price FROM merchan'
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return rows

def select_all_users():
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT id, name, mail FROM login2'
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return rows

def login(user_name, password):
    sql = 'SELECT hashed_password, salt FROM login2 WHERE name = %s'
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

def admin_login(user_name, password):
    sql = "SELECT hashed_password, salt FROM login2 WHERE name = 'nishikawa'"
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

def get_goods_by_id(goods_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = "SELECT id, name, price FROM merchan WHERE id = %s;"
    
    cursor.execute(query, (goods_id,))
    goods_data = cursor.fetchone()

    if goods_data:
        goods_info = {
            'id': goods_data[0],
            'name': goods_data[1],
            'price': goods_data[2]
        }
        return goods_info
    else:
        return None