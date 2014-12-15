from LLADI.database import users
from LLADI.database import follows


def create_feed(user):
    feed = []
    for nusers in user.follows:
        fusers = users.User(nusers[0])
        feed.append({
            "date": "{}-{}-{} {}:{}:{}".format(str(fusers.date)[:4], fusers.date[4:6], fusers.date[6:8],
                                               fusers.date[8:10], fusers.date[10:12], fusers.date[12:14]),
            "title": fusers.display_name + " created their account",
            "body": "",
            "link": "/user/" + str(fusers.uuid),
        })
        for nuser_follows in fusers.follows:
            date = follows.Follow(ufid=follows.get_follow(fusers.uuid, nuser_follows[0])).data[0][3]
            follow_target = users.User(nuser_follows[0]).display_name
            if follow_target == user.display_name:
                follow_target = "you"
            feed.append({
                "date": "{}-{}-{} {}:{}:{}".format(date[:4], date[4:6], date[6:8], date[8:10], date[10:12],
                                                   date[12:14]),
                "title": fusers.display_name + " followed " + follow_target,
                "body": "",
                "link": "/user/" + str(fusers.uuid),
            })

    return feed