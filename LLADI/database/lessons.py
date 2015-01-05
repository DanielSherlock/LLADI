import sqlite3
from time import strftime, gmtime

db_url = 'C:\\Users\\Daniel\\Documents\\GitHub\\LLADI\\database\\lladi.db'


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


class Question:
    def __init__(self, q_type, uqid):
        conn = sqlite3.connect(db_url)
        cur = conn.cursor()
        if q_type == "Q_3OPT":
            cur.execute('SELECT * FROM "Q_3OPT" WHERE "UQID" LIKE ?', (uqid,))
        data = cur.fetchone()
        if data:
            self.exists = True
            self.type = q_type
            self.uqid = data[0]
            self.word = data[1]
            self.target = data[2]
            self.picture = data[3]
            self.lesson_ulid = data[4]
            self.audio = data[5]
            cur.execute('SELECT "Key UKID", "Required Knowledge" FROM "KeyQuestionRequire" WHERE "Question UQID" LIKE ?', (uqid,))
            self.requiredKeys = {}
            for key in cur.fetchall():
                self.requiredKeys[key[0]] = key[1]
            cur.execute('SELECT "Key UKID" FROM "KeyQuestionEffect" WHERE "Question UQID" LIKE ?', (uqid,))
            self.effectedKeys = []
            for key in cur.fetchall():
                self.effectedKeys.append(key[0])
        else:
            self.exists = False
        conn.close()
