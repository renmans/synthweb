import sqlite3
import hashlib

def migration():
    with sqlite3.connect('app.db') as connection:
        cursor = connection.cursor()
        cursor.execute('select password from users')
        passwords = [password[0] for password in cursor.fetchall()]
        print(passwords)
        passwd_hash = hashlib.sha512()
        for password in passwords:
            byte_passwd = password.encode('utf-8')
            passwd_hash.update(byte_passwd)
            cursor.execute('update users set password = ? where password = ?', [
                           passwd_hash.hexdigest(), password])
        cursor.execute('select password from users')
        passwords = [password[0] for password in cursor.fetchall()]
        print(passwords)


if __name__ == '__main__':
    migration()
