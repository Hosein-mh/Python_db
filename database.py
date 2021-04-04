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


def read(statements=None, update_statements=None):
    """ 
    reading data from the users table 
    """
    users_list = []
    users_json_list = []
    if update_statements:
        statements = update_statements

    with open('database.txt', mode='r') as database_file:
        users_list = [x.split('|') for x in database_file.read().split('\n')]
        database_file.close

    if statements and len(statements) <= 5:

        if len(users_list) < 1:
            print('no data found')
            return
        for user_data in users_list:
            user = json.loads(user_data[1])
            users_json_list.append(user)

        print(users_json_list)
        return(users_json_list)
    
    elif statements == None:
        return
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


                


def delete(statements=None, update_statements=None):
    database_lines = ''
    # check if delte fundtion fired from update method with update statements:
    if update_statements:
        statements = update_statements
    with open("database.txt", mode="r+") as database_file: 
        database_lines = database_file.readlines()

        # if query have delete keyword but not completed delete all data
        if statements and len(statements) < 4:
            database_file.truncate(0)
            print('all data cleared')
            return

    if statements and len(statements) >= 4:
        with open("database.txt", mode="w") as database_file:
            condition_list = statements[4].split('=')
            if len(condition_list) == 2:
                for line in database_lines:
                    if not line.strip().startswith(f"{condition_list[1]}|"):
                        database_file.write(line)
                print('delete done')
                return
            print('wrong conditional query')
            return



def update(statements):
    if len(statements) < 5 or statements[4] != 'where' :
        print('rong query set')
        return
    else:
        value_list = statements[3].split(',')
        where_condition_list = statements[5].split('=')

        # first read current data from database
        current_user = {}
        updated_user_line = ''
        read_statements = ['select', 'all', 'from', 'users', 'where', statements[5]]
        readed_data = read(None, read_statements)
        # just if user exists, update it
        if readed_data:
            current_user = readed_data[0]

            for value in value_list:
                user_key_value_list= value.split('=')
                current_user.update({ user_key_value_list[0]: user_key_value_list[1] })

            updated_user_line = f'\n{current_user["username"]}|{{"username":"{current_user["username"]}","password":"{current_user["password"]}","age":{current_user["age"]},"email":"{current_user["email"]}"}}'

        # now delete the old/current database user
        delete_statements = ['delete', 'from', 'users', 'where', statements[5]]
        delete(None, delete_statements)

        # then add updated usr line to the end of the file
        with open('database.txt', mode='a') as database_file:
            if updated_user_line:
                database_file.write(updated_user_line)
                database_file.close()
                print('data successfully updated')
                return
            print('no data found to update')
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