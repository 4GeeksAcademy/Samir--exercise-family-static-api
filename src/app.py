"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

John={
    "last_name": jackson_family.last_name,
    "first_name":"John",
    "age":33,
    "lucky_numbers": [7,13,22]
}

Jane={  
    "last_name": jackson_family.last_name,
    "first_name":"Jane",
    "age":35,
    "lucky_numbers": [10,14,3]
}

Jimmy={ 
    "last_name": jackson_family.last_name,
    "first_name":"Jimmy",
    "age":5,
    "lucky_numbers": [1]
}

jackson_family.add_member(John)
jackson_family.add_member(Jane)
jackson_family.add_member(Jimmy)

# new_member={"name":"michael","age":40,"luck_numbers":[1,2,3]}
# jackson_family.add_member(member=new_member)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = members
    
    return jsonify(response_body), 200

@app.route('/member', methods=['POST'])
def add_member():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Bad Request"}), 400
    member = jackson_family.add_member(data)
    return jsonify(member), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    if not isinstance(id, int):
        return jsonify({"error": "Invalid member ID"}), 400
    result = jackson_family.delete_member(id)
    if result:
        return {"done": True}, 200
    else:
        return jsonify({"error": "Member not found"}), 404
        
    

@app.route('/member/<int:id>', methods=['PATCH'])
def update_member(id):
    data = request.get_json()
    result = jackson_family.update_member(id, data)
    return jsonify(result), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    if not isinstance(id, int):
        return jsonify({"error": "Invalid member ID"}), 400
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"error": "Member not found"}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True) 
