from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Whisky, Whisky_schema, Whiskys_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'jim': 'beam'}

@api.route('/Whiskys', methods = ['POST'])
@token_required
def create_Whisky(current_user_token):
    brand = request.json['brand']
    proof = request.json['proof']
    aged = request.json['aged']
    grain = request.json['grain']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    contact = Whisky(brand, proof, aged, grain, user_token = user_token )

    db.session.add(contact)
    db.session.commit()

    response = Whisky_schema.dump(contact)
    return jsonify(response)

@api.route('/Whiskys', methods = ['GET'])
@token_required
def get_contact(current_user_token):
    a_user = current_user_token.token
    Whiskys = Whisky.query.filter_by(user_token = a_user).all()
    response = Whiskys_schema.dump(Whiskys)
    return jsonify(response)

@api.route('/Whiskys/<id>', methods = ['GET'])
@token_required
def get_Whisky_two(Whisky_user_token, id):
    fan = Whisky_user_token.token
    if fan == Whisky_user_token.token:
        Whisky = Whisky.query.get(id)
        response = Whisky_schema.dump(Whisky)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401

@api.route('/Whisky/<id>', methods = ['POST','PUT'])
@token_required
def update_Whisky(current_user_token,id):
    Whisky = Whisky.query.get(id) 
    Whisky.brand = request.json['brand']
    Whisky.proof = request.json['proof']
    Whisky.aged = request.json['aged']
    Whisky.grain = request.json['grain']
    Whisky.user_token = current_user_token.token

    db.session.commit()
    response = Whisky_schema.dump(Whisky)
    return jsonify(response)

@api.route('/Whiskys/<id>', methods = ['DELETE'])
@token_required
def delete_Whisky(current_user_token, id):
    Whisky = Whisky.query.get(id)
    db.session.delete(Whisky)
    db.session.commit()
    response = Whisky_schema.dump(Whisky)
    return jsonify(response)










