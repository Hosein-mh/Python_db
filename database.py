"""
Query samples:
    INSERT: insert into users values(username_srt,password_str,age_int,email_str)
    READ: select all from users where age=21 || select *
    UPDATE: update users set username=Jafar,password=1234 where username=Ali,
    DELETE: delete from users where username=Ali || delete #this will delete all data
"""

import json

def insert(data):
    """ 
    inserting data to the users table 
    """
    with open('database.json', mode='r') as userFile:
        users_json = json.load(userFile)
        users_json['users'].append(data)
        userFile.close()
    with open('database.json', mode='w') as userFile:
        userFile.write(json.dumps(users_json))
        userFile.close()
        print('insert done')


def read(statements):
    """ 
    reading data from the users table 
    """
    if len(statements) <= 5:
        # return all data
        with open('database.json', mode='r') as userFile:
            users_json = json.load(userFile)
            userFile.close()
            print(users_json)
            return users_json
    else:
        # example: condition username=Hossein , condition_list = ["username", "Hossein"]
        condition_list = statements[5].split('=')
        if len(condition_list) == 2:
            with open('database.json', mode='r') as userFile:
                users_json = json.load(userFile)
                userlist = []
                for user in users_json['users']:
                    for user_key, user_value in user.items():
                        if condition_list[0] == 'age':
                            # age field is integer
                            if user_key=='age' and user_value==int(condition_list[1]):
                                userlist.append(user)
                                
                        if user_key==condition_list[0] and user_value==condition_list[1]:
                            userlist.append(user)
                            
                if userlist:
                    print(userlist)
                    return userlist
                else:
                    print('no user found')
                    return None
                userFile.close()


def delete(statements):
    message=''
    with open("database.json", mode="r") as userFile: 
        users_json = json.load(userFile)
    
    if len(statements) < 4:
        # if query have delete keyword but not completed delete all data
        users_json['users'].clear()
        message = 'all data have removed'

    else:
        condition_list = statements[4].split('=')

        for user in users_json['users']:
            if condition_list[0] == 'age':
                if user[condition_list[0]] == int(condition_list[1]):
                    users_json['users'].remove(user)
                    message = 'the user have removed'

            if user[condition_list[0]] == condition_list[1]:
                users_json['users'].remove(user)
                message = 'the user have removed'
    
    with open("database.json", mode="w") as userFile:
        json.dump(users_json, userFile)
        print(message)


def update(statements):
    if len(statements) < 5 or statements[4] != 'where' :
        print('rong query set')
        return
    else:
        value_list = statements[3].split(',')
        where_condition_list = statements[5].split('=')

        with open("database.json", mode="r") as userFile:
            users_json = json.load(userFile)

        users = users_json['users']
        user_founded = False
        for user in users:
            if user[where_condition_list[0]] == where_condition_list[1]:
                user_founded = True
                for value in value_list:
                    item_list = value.split('=')
                    user[item_list[0]] = item_list[1]

        with open("database.json", mode="w") as userFile:
            json.dump(users_json, userFile)
            if user_founded:
                print('successfully updated')
            else:
                print('user not found')
        return


while(True):
    query = input('Enter your query or "e" for exit: ')
    if query.startswith('e'):
        break
    statements = query.split(' ')
    if statements[0] == 'insert':
        value_list = statements[3][7:-1].split(',')

        data = {
            'username': value_list[0],
            'password': value_list[1],
            'age': int(value_list[2]),
            'email': value_list[3]
        }
        insert(data)
    if statements[0] == 'select':
        read(statements)

    if statements[0] == 'delete':
        delete(statements)

    if statements[0] == 'update':
        update(statements)


# select * from users