import json
from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from model.regione import Regione
from model.provincia import Provincia
from model.comune import Comune

# Avvio classe Base per dare funzionalità extra ad altre classi
#Base = declarative_base()

# Avvio creazione delle tabelle in base alla classi definite   
engine = create_engine('sqlite:///ang_database.db', echo=True)
# Base.metadata.create_all(bind=engine)

# Avvio sessione per effettuare modifiche sul database
Session = sessionmaker(bind=engine)

# Creare una nuova sessione
session = Session()

# Creare un nuovo oggetto Regione per ogni regione nel json
with open('jsons/regioni.json', encoding='utf-8') as json_file:
    regioni = json.load(json_file)

    for regione in regioni:
        # Aggiungere l'oggetto alla sessione se non esiste nel database
        instanza = session.query(Regione).filter(Regione.nome==regione['nome']).first()
        if not instanza:
            session.add(Regione(regione['nome']))
        else: print('-----skipped------')

# Creare un nuovo oggetto Provincia per ogni provincia nel json
with open('jsons/province.json', encoding='utf-8') as json_file:
    province = json.load(json_file)

    for provincia in province:
        # Aggiungere l'oggetto alla sessione se non esiste nel database
        instanza = session.query(Provincia).filter(Provincia.nome==provincia['nome']).first()
        if not instanza:
            session.add(Provincia(provincia['nome'], provincia['regione']))
        else: print('-----skipped------')

with open('jsons/comuni.json', encoding='utf-8') as json_file:
    comuni = json.load(json_file)

    for comune in comuni:

        nome = comune['nome']
        provincia = comune['provincia']['nome']
        regione = comune['regione']['nome']

        instanza = session.query(Comune).filter(Comune.nome==nome).first()
        if not instanza:
            session.add(Comune(nome, provincia, regione))
        else: print('-----skipped------')

# Confermare l'operazione
session.commit()

# Chiudere la sessione
session.close()