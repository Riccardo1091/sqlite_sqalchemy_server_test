import os
from flask import Flask, jsonify, json, make_response
from flask_cors import CORS
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker

# Avvio creazione delle tabelle in base alla classi definite   
engine = create_engine('sqlite:///ang_database.db', echo=True)

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ang_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # per consumare meno memoria, da approfondire 
# db = SQLAlchemy(app)
from model.regione import Regione
from model.provincia import Provincia
from model.comune import Comune

@app.route('/')
def index():
    return jsonify('Api per Regioni, Province, Comuni attiva')

@app.route('/regioni')
def get_regioni():
    # Avvio sessione legata al motore del database per effettuare modifiche sul database
    Session = sessionmaker(bind=engine)
    # Creare una nuova sessione
    session = Session()

    regioni = session.query(Regione).all()
    regioni_list = [r.to_dict() for r in regioni]

    # chiudi sessione
    session.close()
    return jsonify(regioni_list)

@app.route('/province/<string:regione>/')
@app.route('/province/<string:regione>/<string:caratteri>')
def get_province(regione:str, caratteri:str|None=None):
    
    Session = sessionmaker(bind=engine)
    session = Session()

    if caratteri is None:
        province = session.query(Provincia).filter(Provincia.regione.ilike(regione)).all()
        province_list = [p.to_dict() for p in province]
    else:
        province = session.query(Provincia).filter(Provincia.regione.ilike(regione), Provincia.nome.ilike('%'+caratteri+'%')).all()
        province_list = [p.to_dict() for p in province]

    # chiudi sessione
    session.close()
    return jsonify(province_list)

@app.route('/comuni/<string:provincia>/')
@app.route('/comuni/<string:provincia>/<string:caratteri>')
def get_comuni(provincia:str, caratteri:str|None=None):

    Session = sessionmaker(bind=engine)
    session = Session()

    if caratteri is None:
        comuni = session.query(Comune).filter(Comune.provincia.ilike(provincia)).all()
        comuni_list = [p.to_dict() for p in comuni]
    else:
        comuni = session.query(Comune).filter(Comune.provincia.ilike(provincia), Comune.nome.ilike('%'+caratteri+'%')).all()
        comuni_list = [p.to_dict() for p in comuni]

    session.close()
    return jsonify(comuni_list)

if __name__ == '__main__':
    app.run(port=9000)