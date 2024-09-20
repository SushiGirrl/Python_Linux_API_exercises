from flask import Flask, jsonify, request
from members import readRandomDb

app = Flask(__name__)

# routes CRUD opperationer GET, POST, PUT, PATCH, DELETE

@app.route('/members')
def read_all():
    return jsonify(readRandomDb()) 

'''
@app.route('/members/', methods=['POST'])
def  create():
    data = request.get_json()
    random_users.append(data)

    return jsonify(create(data))
'''
    
app.run(debug=True)