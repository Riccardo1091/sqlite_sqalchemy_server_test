# from flask import Flask
from sqlalchemy import Column, String, create_engine
# from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy

# Avvio classe Base per dare funzionalità extra ad altre classi (solo con SQLALCHEMY direttamente)
# Base = declarative_base()
# app = Flask(__name__)
db = SQLAlchemy() # quando si usa SqlAlchemy con Flask

class Regione(db.Model):
    #__tablename__ = 'regione'

    nome = Column('nome', String, primary_key=True)

    def __init__(self, nome):
        self.nome = nome

    def __repr__(self):
        return f'{self.nome}'
    
    def to_dict(self):
        return {'nome': self.nome}

# engine = create_engine('sqlite:///ang_database.db', echo=True)
# db.metadata.create_all(bind=engine)

# with app.app_context():
#     db.create_all()