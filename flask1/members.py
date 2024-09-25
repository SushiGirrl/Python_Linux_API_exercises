import sqlite3
from data_dict import random_users

def create():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS members (
                    id INTEGER,
                    name TEXT)''')
        cur.execute('''INSERT INTO members VALUES (
                    1, 
                    'John')''')
        cur.execute('''INSERT INTO members VALUES (
                    2, 
                    'Anna')''')
        cur.execute('''INSERT INTO members VALUES (
                    3, 
                    'Carl')''')

def read():

    members = []

    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM members')

        for i in cur.fetchall():
            members.append({'id' : i[0], 'name' : i[1]})
        
        return members
    

def createRandomDatabase():
    with sqlite3.connect('databaseRandom.db') as conn:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS members (
                    id INTEGER,
                    first_name TEXT,
                    last_name TEXT,
                    birth_date TEXT,
                    gender TEXT,
                    email TEXT,
                    phonenumber INTEGER,
                    address TEXT,
                    nationality TEXT,
                    active TEXT,
                    github_username TEXT
                    )''')
        
        # Check if the table already has data
        cur.execute('SELECT COUNT(*) FROM members')
        count = cur.fetchone()[0]

        if count == 0:
            # Only insert data if the table is empty
            cur.executemany('''INSERT INTO members VALUES (
                        :id,:first_name,:last_name,:birth_date,:gender,:email,
                        :phonenumber,:address,:nationality,:active,:github_username)''', random_users)
            conn.commit()
        else:
            print("Table already has data, skipping insertion.")
        

def readRandomDb():

    members = []

    with sqlite3.connect('databaseRandom.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM members')

        for i in cur.fetchall():
            members.append({'id' : i[0], 'first_name' : i[1], 'last_name' : i[2], 'birth_date' : i[3], 
                            'gender' : i[4], 'email' : i[5], 'phonenumber' : i[6], 'address' : i[7],
                            'nationality' : i[8], 'active' : i[9], 'github_username' : i[10]})
        
        return members
    

new_github_usernames = [
    'bklieger-groq',
    'aaronjanse',
    'sharkdp',
    'xifangczy',
    'owenthereal',
    'Externalizable',
    'marcinbor85',
    'kuroni',
    'thu-spmi',
    'SushiGirrl'
]

def updateGithubUsernames():
 with sqlite3.connect('databaseRandom.db') as conn:
     cur = conn.cursor()
     
     # Retrieve all user IDs
     cur.execute('SELECT id FROM members')
     user_ids = [row[0] for row in cur.fetchall()]
     
     if len(user_ids) != len(new_github_usernames):
         raise ValueError("The number of users doesn't match the number of GitHub usernames.")
     
     # Update each user's GitHub username based on their ID
     for user_id, username in zip(user_ids, new_github_usernames):
         cur.execute('''UPDATE members 
                        SET github_username = ? 
                        WHERE id = ?''', (username, user_id))
     
     # Commit the changes to the database
     conn.commit()



createRandomDatabase()


# Call the function to update the GitHub usernames
updateGithubUsernames()

print(readRandomDb())
