#pip install python-dotenv

from flask import Flask, jsonify, request
from members import readRandomDb
import sqlite3
from dotenv import load_dotenv
import os
import requests

app = Flask(__name__)

# Load all environment variables from the .env file
load_dotenv()

# routes CRUD opperationer GET, POST, PUT, PATCH, DELETE

# Function to fetch GitHub repository names for a specific user
def fetch_github_repos(username):
    url = f'https://api.github.com/users/{username}/repos'
    req = requests.get(url)
    j = req.json()

    repo_names = [i['name'] for i in j]
    return repo_names

@app.route('/members')
def read_all():
    # Fetch the member data from the database
    members_data = readRandomDb()
    
    # List to hold the data with GitHub repos
    response = []

    # Fetch the GitHub repo names for each member
    for member in members_data:
        github_username = member.get('github_username')
        if github_username:
            member['github_repos'] = fetch_github_repos(github_username)
        else:
            member['github_repos'] = []
        response.append(member)

    return jsonify(response)

'''
@app.route('/members/', methods=['POST'])
def  create():
    data = request.get_json()
    random_users.append(data)

    return jsonify(create(data))
'''


# Function to update a specific member's GitHub username by ID
@app.route('/members/update_username/<int:id>/<new_username>', methods=['PUT'])
def update_username(id, new_username):
    # Update the database directly using the function parameters
    with sqlite3.connect('databaseRandom.db') as conn:
        cur = conn.cursor()

        # Check if the member exists
        cur.execute('SELECT * FROM members WHERE id = ?', (id,))
        member = cur.fetchone()

        if not member:
            return jsonify({"error": "Member not found"}), 404  # 404 Not Found

        # Update the github_username
        cur.execute('UPDATE members SET github_username = ? WHERE id = ?', (new_username, id))
        conn.commit()

    return jsonify({"id": id, "github_username": new_username}), 200  # 200 OK

    
app.run(debug=True)