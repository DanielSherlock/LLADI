import sqlite3
import base64

db_url = 'C:\\Users\\Sam\\Desktop\\LLADI\\database\\lladi.db'

class User():
    def __init__(self, uuid=0, username=""):
        conn = sqlite3.connect(db_url)
        cur = conn.cursor()
        if uuid:
            cur.execute('SELECT * FROM "User" WHERE "UUID" LIKE ?', (uuid,))
        elif username:
            cur.execute('SELECT * FROM "User" WHERE "Username" LIKE ?', (username,))
        data = cur.fetchone()
        conn.close()
        self.uuid = data[0]
        self.username = data[1]
        self.password = data[2]
        self.display_name = data[3]
        self.picture = data[4]