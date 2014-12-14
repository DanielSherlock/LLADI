import sqlite3
from time import strftime, gmtime
from LLADI.functions.users import current_user

db_url = 'C:\\Users\\Sam\\Desktop\\LLADI\\database\\lladi.db'


class Course:
    def __init__(self, ucid=None, course_name=None):
        conn = sqlite3.connect(db_url)
        cur = conn.cursor()
        if ucid:
            cur.execute('SELECT * FROM "Course" WHERE "UCID" LIKE ?', (ucid,))
        elif course_name:
            cur.execute('SELECT * FROM "Course" WHERE "Course Name" LIKE ?', (course_name,))
        data = cur.fetchone()
        conn.close()
        if data:
            self.exists = True
            self.ucid = data[0]
            self.course_name = data[1]
            self.owner = data[2]
            self.date = data[3]
            self.picture = data[4]
        else:
            self.exists = False


def new_course(course_name):
    cu = current_user()
    if not cu:
        return None
    conn = sqlite3.connect(db_url)
    cur = conn.cursor()
    date = strftime("%Y%m%d%H%M%S", gmtime())
    cur.execute("insert into Course('Course Name', 'Owner UUID', 'Creation Date') VALUES(?, ?)",
                (course_name, current_user().uuid, date))
    conn.commit()
    conn.close()

