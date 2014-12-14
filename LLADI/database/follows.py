import sqlite3
from time import strftime, gmtime

db_url = 'C:\\Users\\Sam\\Desktop\\LLADI\\database\\lladi.db'


class Follow():
    def __init__(self, follower=None, followee=None, ufid=None):
        conn = sqlite3.connect(db_url)
        cur = conn.cursor()

        if follower:
            cur.execute('SELECT "Followee" FROM "Follow" WHERE "Follower" LIKE ?', (int(follower),))
        elif followee:
            cur.execute('SELECT "Follower" FROM "Follow" WHERE "Followee" LIKE ?', (int(followee),))
        elif ufid:
            cur.execute('SELECT * FROM "Follow" WHERE "UFID" LIKE ?', (int(ufid),))
        self.data = cur.fetchall()


def new_follow(follower, followee):
    conn = sqlite3.connect(db_url)
    cur = conn.cursor()
    date = strftime("%Y%m%d%H%M%S", gmtime())
    cur.execute("insert into Follow('Follower', 'Followee', 'Follow Date') VALUES(?, ?, ?)",
                (int(follower), int(followee), date))
    conn.commit()
    conn.close()


def remove_follow(follower, followee):
    conn = sqlite3.connect(db_url)
    cur = conn.cursor()
    cur.execute('DELETE FROM "Follow" WHERE "Follower" LIKE ? AND "Followee" LIKE ?', (int(follower), int(followee)))
    conn.commit()
    conn.close()
