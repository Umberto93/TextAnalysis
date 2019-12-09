from kency_app.kency import Kency
from ontology.ontology_builder import OntologyBuilder

from semantic.text_classifier import TextClassifier
from semantic.entity_recognizer import EntityRecognizer
from semantic.keywords_extractor import KeywordsExtractor


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


print("===============================================================================================================")
print(" OPERAZIONE DI TEXT PROCESSING")
print("===============================================================================================================")
# OPERAZIONE DI TEXT PROCESSING
print("\nCASO 1] L'utente chiede al sistema di processare un testo fornito in input.")
new_doc_txt = 'The Mona Lisa is a 16th century oil painting created by Leonardo. It is held at the Louvre in Paris.'
print("Testo: ", new_doc_txt)
print("Processamento del testo in corso...")
kency.process_user_text(new_doc_txt)
print("Testo processato con sucesso.")
print("\n")


print("===============================================================================================================")
print(" OPERAZIONI SUI DOCUMENTI ")
print("===============================================================================================================")
# OPERAZIONI SUI DOCUMENTI
    # RECUPERO DOCUMENTI DI UNA CERTA CATEGORIA CHE CONDIVIDONO UN SUB-SET DELLE KEYWORD FORNITE IN INPUT
print("\nCASO 1] L'utente chiede al sistema di visualizzare i documenti di una certa categoria che condividono almeno")
print("due delle keywords fornite in input.")
cat = 'Entertainment'
keys = ['lisa', 'leonardo']
print("cat: ", cat)
print("keys: ", keys)
print("Recupero documenti in corso...")
docs = kency.get_related_documents(cat, keys)
for doc in docs:
    print(doc)
print("Documenti recuperati con sucesso.")

    # VISUALIZZARE DETTAGLI DI UN DOCUMENTO
print("\nCASO 2] L'utente chiede al sistema di visualizzare i dettagli di un certo documento.")
doc = 'Entertainment_doc_user_1'
print("nome istanza: ", doc)
print("Recupero dettagli del documento in corso...")
doc_res = kency.get_document_details(params={'id': doc})
print("Documento: ", doc_res)
print("Documento recuperato con sucesso.")

    # VISUALIZZARE ELENCO DOCUMENTI DI UNA CERTA CATEGORIA
print("\nCASO 3] L'utente chiede al sistema di visualizzare la lista di documenti di una certa categoria.")
print("Recupero documenti della categoria \'Other\' in corso...")
cat_docs = kency.get_documents(params={'has_category': 'Other_01'})
for doc in cat_docs:
    print(doc)
print("Documenti recuperati con successo.")
print("\n")


print("===============================================================================================================")
print(" OPERAZIONI SULLE PAROLE ")
print("===============================================================================================================")
# OPERAZIONI SULLE PAROLE
    # VISUALIZZARE ELENCO DELLE PAROLE CHE INIZIANO PER ...
print("\nCASO 1] L'utente chiede al sistema di visualizzare tutte le parole che iniziano per (search-string).")
print("Recupero dettagli in corso...")
words = kency.get_words_starting_with(params={'start':'sna'})
for word in words:
    print(word)
print("Parole recuperate con successo.")
print("\n")


print("===============================================================================================================")
print(" OPERAZIONI SULLE CATEGORIE ")
print("===============================================================================================================")
# OPERAZIONI SULLE CATEGORIE
    # VISUALIZZARE ELENCO DELLE CATEGORIE
print("\nCASO 1] L'utente chiede al sistema di visualizzare tutte le categorie.")
print("Recupero dettagli in corso...")
categories = kency.get_categories()
for cat in categories:
    print(cat)
print("Categorie recuperate con successo.")

