import sqlite3
import base64
from time import strftime, gmtime
from . import follows

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
        if data:
            self.exists = True
            self.uuid = data[0]
            self.username = data[1]
            self.password = data[2]
            self.display_name = data[3]
            self.picture = data[4]
            self.date = data[5]
            self.follows = follows.Follow(follower=self.uuid).data
            self.followed_by = follows.Follow(followee=self.uuid).data
        else:
            self.exists = False

    def __del__(self):
        pass


def search_user(search):
    conn = sqlite3.connect(db_url)
    cur = conn.cursor()
    cur.execute('SELECT "UUID" FROM "User" WHERE "Display Name" LIKE ?', ("%" + search + "%",))
    data = cur.fetchall()
    conn.close()
    ret = []
    for suser in data:
        ret.append(User(int(suser[0])))
    return ret


def new_user(username, password, display_name):
    conn = sqlite3.connect(db_url)
    cur = conn.cursor()
    date = strftime("%Y%m%d%H%M%S", gmtime())
    cur.execute("insert into User('Username', 'Password', 'Display Name', 'Creation Date') VALUES(?, ?, ?, ?)",
                (username, password, display_name, date))
    conn.commit()
    conn.close()


def get_tier_knowledge(course, user):
    conn = sqlite3.connect(db_url)
    cur = conn.cursor()
    cur.execute('SELECT "Tier" FROM "Tier Knowledge" WHERE "Course UCID" LIKE ? AND "User UUID" LIKE ?', (course, user))
    data = cur.fetchone()
    conn.close()
    if not data:
        return 0
    return data[0]