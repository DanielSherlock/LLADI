import sqlite3
from time import strftime, gmtime

db_url = 'C:\\Users\\Sam\\Desktop\\LLADI\\database\\lladi.db'


class Lesson:
    def __init__(self, ulid):
        conn = sqlite3.connect(db_url)
        cur = conn.cursor()
        cur.execute('SELECT * FROM "Lesson" WHERE "ULID" LIKE ?', (ulid,))
        data = cur.fetchone()
        conn.close()
        if data:
            self.exists = True
            self.ulid = data[0]
            self.name = data[1]
            self.course_ucid = data[2]
            self.tier = data[3]
            self.date = data[4]
        else:
            self.exists = False