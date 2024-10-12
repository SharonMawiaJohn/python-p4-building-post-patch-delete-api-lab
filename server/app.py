#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(  bakeries,   200  )

@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH'])
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()

    if bakery == None:
        response_body = {
            "message": "This record does not exist in our database. Please try again."
        }
        response = make_response(response_body, 404)

        return response
    else:
        if request.method == 'GET':
            bakery_serialized = bakery.to_dict()
            return make_response (bakery_serialized, 200)
        
        elif request.method == 'PATCH':    
            for attr in request.form:
                setattr(bakery, attr, request.form.get(attr))

            db.session.add(bakery)
            db.session.commit()

            bakery_serialized = bakery.to_dict()
            return make_response (bakery_serialized, 200)  
    
@app.route('/baked_goods', methods=['GET', 'POST'])
def baked_goods():    
    if request.method == 'GET':
        baked_dict =[baked_good.to_dict() for baked_good in BakedGood.query.all()]
        response = make_response(
            baked_dict,
            200
        )
        return response
        
    elif request.method == 'POST':
        new_baked_good = BakedGood(
            name=request.form.get("name"),
            price=request.form.get("price"),
        )

        db.session.add(new_baked_good)
        db.session.commit()

        new_baked_good_dict = new_baked_good.to_dict()

        response = make_response(
            new_baked_good_dict,
            201
        )

        return response

@app.route('/baked_goods/<int:id>', methods=['GET', 'DELETE'])
def baked_goods_by_id(id):
    baked_good = BakedGood.query.filter(BakedGood.id == id).first()
    if baked_good == None:
        response_body = {
            "message": "This record does not exist in our database. Please try again."
        }
        response = make_response(response_body, 404)

        return response
    else:    
        if request.method == 'GET':
            baked_dict = baked_good.to_dict()

            response = make_response(
                baked_dict,
                200
            )

            return response
        
        elif request.method == 'DELETE':
            db.session.delete(baked_good)
            db.session.commit()

            response_body = {
                "delete_successful": True,
                "message": "Review deleted."
            }

            response = make_response(
                response_body,
                200
            )

            return response
            


@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    return make_response( baked_goods_by_price_serialized, 200  )
   

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()
    return make_response( most_expensive_serialized,   200  )

if __name__ == '__main__':
    app.run(port=5555, debug=True)