import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:5000"])

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks', methods=['GET'])
def get_drinks():
    try:
        drinksShortList = [drink.short() for drink in Drink.query.all()]
        return json.dumps({
            'success': True,
            'drinks': drinksShortList
        }), 200
    except Exception as e:
        print(e)
        return json.dumps({
            'success': False,
            'error': f"Error with creating a new drink: {str(e)}"
        }), 500
'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    try:
        drinksLongList = [drink.long() for drink in Drink.query.all()]
        return jsonify({
            'success': True,
            'drinks': drinksLongList
        }), 200
    except:
        return json.dumps({
            'success': False,
            'error': "Error with loading drinks occured"
        }), 500
    

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks_detail(payload):
    body = request.get_json()
    try:
        id = body.get('id')
        title = body.get('title')
        recipe = json.dumps(body.get('recipe'))
        new_drink = Drink(id=id, title=title, recipe=recipe)
        print(new_drink)
        new_drink.insert()

        return jsonify({
            'success': True,
            'drinks': [new_drink.long()]
        }), 200
    except Exception as e:
        print(e)

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drinks_detail(payload, drink_id):
    body = request.get_json()
    try:
        drink_id = Drink.query.filter(Drink.id==drink_id).one_or_none()
        drink_id.title = body.get('title')
        drink_id.recipe = json.dumps(body.get('recipe'))
        drink_id.update()

        return jsonify({
            'success': True,
            'drinks': [drink_id.long()]
        }), 200
    except Exception as e:
        print(e)
        return json.dumps({
            'success': False,
            'error': f"Error with creating a new drink: {str(e)}"
        }), 500

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(payload, drink_id):
    try:
        drink = Drink.query.filter(Drink.id==drink_id).one_or_none()
        print(drink_id)
        drink.delete()

        return jsonify({
            'success': True,
            'drinks': drink_id
        }), 200
    except Exception as e:
        print(e)
        return json.dumps({
            'success': False,
            'error': f"Error with creating a new drink: {str(e)}"
        }), 500

# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
