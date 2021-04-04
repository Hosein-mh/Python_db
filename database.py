"""
Query samples:
    INSERT: insert into users values(username_srt,password_str,age_int,email_str)
    READ: select all from users where username=Ali || select * // it just searchs based on username
    UPDATE: update users set username=Jafar,password=1234 where username=Ali,
    DELETE: delete from users where username=Ali || delete #this will delete all data
"""

import json

def insert(data):
    """ 
    inserting data to the users table 
    """
    value_list = statements[3][7:-1].split(',')

    data = {
        'username': value_list[0],
        'password': value_list[1],
        'age': int(value_list[2]),
        'email': value_list[3]
    }

    with open('database.txt', mode='a') as database_file:
        string = f'''\n{data["username"]}|{{"username":"{data["username"]}","password":"{data["password"]}","age":{data["age"]},"email":"{data["email"]}"}}'''
        database_file.write(string)
        database_file.close()


def read(statements):
    """ 
    reading data from the users table 
    """
    users_list = []
    users_json_list = []

    with open('database.txt', mode='r') as database_file:
        users_list = [x.split('|') for x in database_file.read().split('\n')]
        database_file.close

    if len(statements) <= 5:

        if len(users_list) < 1:
            print('no data found')
            return
        for user_data in users_list:
            user = json.loads(user_data[1])
            users_json_list.append(user)

        print(users_json_list)
        return(users_json_list)
    else:
        # example: condition username=Hossein , condition_list = ["username", "Hossein"]
        condition_list = statements[5].split('=')
        if len(condition_list) == 2:
            # find users and convert it to json and append it to users_json_list
            for user in users_list:
                if user[0] == condition_list[1]:
                    users_json_list.append(json.loads(user[1]))
            
        print(users_json_list)
        return users_json_list


                


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
        insert(statements)
    if statements[0] == 'select':
        read(statements)

    if statements[0] == 'delete':
        delete(statements)

    if statements[0] == 'update':
        update(statements)


# select * from users