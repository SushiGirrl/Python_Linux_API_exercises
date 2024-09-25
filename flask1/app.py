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
github_access_token = os.getenv('GITHUB_ACCESS_TOKEN')

# routes CRUD opperationer GET, POST, PUT, PATCH, DELETE

# Function to fetch GitHub repository names for a specific user
def fetch_github_repos(username):

     # If you want to get the repos of the authenticated user, use the /user/repos endpoint
    if username == 'SushiGirrl':
        # This is where you want to include the authorization header to access private repos
        headers = {'Authorization': f'token {github_access_token}' }
        url = 'https://api.github.com/user/repos'  # Use /user/repos for authenticated user
        req = requests.get(url, headers=headers)
    else:
        # Public repositories can be fetched directly
        url = f'https://api.github.com/users/{username}/repos'
        req = requests.get(url)

    # Check if the request was successful
    if req.status_code == 200:
        j = req.json()
        repo_names = [i['name'] for i in j]
        return repo_names, 200  # 200 OK
    else:
        print(f"Error fetching repos for {username}: {req.status_code} {req.json()}")
        return [], req.status_code  # Return the error status code


@app.route('/members')
def read_all():
    # Fetch the member data from the database
    members_data = readRandomDb()

    if not members_data:  # If no members found, return 404
        return jsonify({"error": "No members found"}), 404  # 404 Not Found
    
    # List to hold the data with GitHub repos
    response = []

    # Fetch the GitHub repo names for each member
    for member in members_data:
        github_username = member.get('github_username')
        if github_username:
            repos, status_code = fetch_github_repos(github_username)
            if status_code != 200:
                return jsonify({"error": f"Failed to fetch repos for {github_username}"}), status_code
            member['github_repos'] = repos
        else:
            member['github_repos'] = []
        response.append(member)

    return jsonify(response), 200  # 200 OK

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