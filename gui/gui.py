import eel

from kency_app.kency import Kency
from ontology.ontology_builder import OntologyBuilder

from semantic.text_classifier import TextClassifier
from semantic.entity_recognizer import EntityRecognizer
from semantic.keywords_extractor import KeywordsExtractor

eel.init('web')

"""
    DICHIARAZIONE E INIZIALIZZAZIONE DELLE VARIABILI DI INTERESSE
"""
# Percorso in cui sono contenute le cartelle contenenti i documenti di interesse per le varie categorie
dataset_path = '../dataset'

# Percorso in cui sono contenute le cartelle contenenti i documenti inseriti dall'utente e processati
user_path = '../user_docs'

ob = OntologyBuilder()
ke = KeywordsExtractor()
tc = TextClassifier(['17bcd095be24d7870cf09b5d93f344bc'], 3)
er = EntityRecognizer(
    ['1950484b2eef4aef8784f97bff21b28f',
     '90057b00684745d5b4fe2ae0a82432a9',
     'bda714d81dc54fc8a0bd43398125a4e6'], 3)

print("BENVENUTO IN KENCY\n")

print("===============================================================================================================")
print(" INIT DEL SISTEMA ")
print("===============================================================================================================")
kency = Kency(ob, ke, tc, er, dataset_path, user_path)

@eel.expose
def py_request(pathname, params=None, include=[]):
    if pathname == '/articles':
        return kency.get_documents(params, include_props=include)
    if pathname == '/article':
        return kency.get_document_details(params)
    if pathname == '/related':
        return kency.get_related_documents(params['category'], params['keywords'])
    if pathname == '/keywords':
        return kency.get_words_starting_with(params)
    if pathname == '/processing':
        return kency.process_user_text(params['content'])
    if pathname == '/query':
        return kency.run_query(params['query'])
    if pathname == '/categories':
        return kency.get_categories()


eel.start('index.html', mode='chrome-app')
