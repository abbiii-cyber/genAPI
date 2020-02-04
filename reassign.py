from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
import os
from flask_restful import Api, Resource

app = Flask(__name__)   



app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or '923892yr3eohnouyewfune'

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

api = Api(app)
migrate = Migrate(app, db) 

#creating a database 
class Generate(db.Model):
    s_n = db.Column(db.Integer, primary_key=True)
    pin = db.Column(db.Integer, unique=True, nullable=False)
    

#generating a pin
class Pin_generate(Resource):
    def get(self):
        pin1 = str(int(uuid.uuid4()))[:15]

        #adding the generated pin into the database
        table = Generate(pin=int(pin1))
        db.session.add(table)
        db.session.commit()
        serial_number = Generate.query.filter_by(pin=int(pin1)).first()
        return jsonify ({'SERIAL NUMBER': serial_number.s_n, 'PIN': int(pin1)})

api.add_resource(Pin_generate, '/')


#checking if pin exist in database
@app.route('/<string:pin>', methods=['GET'])
def check_s_n(pin):
    pin = Generate.query.filter_by(pin=pin).all()
    if pin:
         return jsonify({'message': 'Valid PIN'})
    return jsonify({'message': 'Invalid PIN !!!'})






if __name__ == '__main__':
    app.run(debug=True)