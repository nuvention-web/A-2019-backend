def getUserByName(db, username):
    all_users = db.child("users").get()

    for user in all_users.each():
        if username == user.val()['username']:
            print('success!!!')
            return user

    return None