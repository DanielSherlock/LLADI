from LLADI.database import follows

def validate_follow(follower, followee):
    fcheck = follows.Follow(follower=follower).data
    match = False
    for followed in fcheck:
        if followee in followed:
            match = True
    return not match
