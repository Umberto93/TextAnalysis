import os
import re

from utils.file_manager import FileManager
from ontology.ontology import OntologyBuilder
from preprocessing.keywords_extractor import KeywordsExtractor

from semantic.dandelion_api import DandelionAPI
from semantic.text_processor import TextProcessor
from utils.text_cleaner import get_cleaned_text

"""
    DICHIARAZIONE E INIZIALIZZAZIONE DELLE VARIABILI DI INTERESSE
"""
# Percorso in cui sono contenute le cartelle contenenti i documenti di interesse per le varie categorie
dataset_path = '../dataset'
# Lista delle categorie di interesse
categories = os.listdir(dataset_path)

ke = KeywordsExtractor()
file_manager = FileManager()
ob = OntologyBuilder()
ob.build_ontology_schema()
api = DandelionAPI(
    ['1950484b2eef4aef8784f97bff21b28f',
     '90057b00684745d5b4fe2ae0a82432a9',
     'bda714d81dc54fc8a0bd43398125a4e6'], 3)

# Dichiarazione dizionario contenete le collezioni di documenti per ogni categoria
cat_docs = {}

"""
    INIT DEL SISTEMA CON I DATI CONTENUTI NEL DATASET
"""
for category in categories:
    # Collezione dei documenti contenuti nella directory esaminata
    docs = {}
    # Dizionario delle keywords relative alla collezione di documenti
    docs_keywords = {}
    # Path della cartella contenente i documenti relativa alla categoria esaminata
    cat_dir_path = dataset_path + '/' + category
    # Elenco dei file contenuti nella directory esaminata
    files = os.listdir(cat_dir_path)

    # Lettura file e pulizia del testo contenuto
    for file_name in files:
        text = file_manager.read_file(cat_dir_path + '/' + file_name)
        docs[category + '_doc_' + file_name.split('.')[0]] = get_cleaned_text(text)

    # Assegno la lista di documenti di una specifica categoria al relativo campo
    # nel dizionario categories
    cat_docs[category] = docs
    # Estrazione delle keywords relative alla collezione dei documenti
    docs_keywords = ke.extract(docs)
    # Creazione istanza della categoria e assegnazione delle relative proprietà
    cat = ob.add_individual(category, category + '_01')
    ob.add_property(cat, 'has_name', category + '_01')

    # Creazione istanze dei documenti e assegnazione delle relative proprietà
    for document, keywords in docs_keywords.items():
        file_path = dataset_path + '/' + category + '/' + document.replace(category + '_doc_', '') + '.txt'
        doc = ob.add_individual('Document', document)
        ob.add_property(doc, 'has_category', cat)
        ob.add_property(doc, 'has_score_' + category.lower(), 1)
        ob.add_property(doc, 'has_path', file_path)

        # Creazione istanze delle parole e assegnazione delle relative proprietà
        for key in keywords.keys():
            word = ob.add_individual('Word', 'word_' + key)
            ob.add_property(doc, 'has_keyword', word)
            ob.add_property(word, 'has_value', key)

    # Estrazione delle entità di interesse associate al documento e assegnazione.
    # Ciascuna entità è identificata dal relativo URI in DBpedia e viene assegnata
    # all'istanza del documento attraverso la relativa datatype property.
    for i, (doc_name, doc_text) in enumerate(docs.items()):
        # <!-- QUESTA PARTE SERVE SOLO PER NON FARE TROPPE RICHIESTE MENTRE FACCIAMO LE PROVE --!> #
        if i == 2:
            break
        doc = ob.get_individual(doc_name)
        doc_entities = api.get_entities(doc_text)

        for entity in doc_entities:
            if entity['types']:
                for type in entity['types']:
                    entity_type = re.search('\/(Person|Work|Organisation|Place|Event)$', type, re.IGNORECASE)

                    if entity_type:
                        predicate = entity_type.group(1).lower()
                        ob.add_property(doc, 'has_' + predicate, entity['dbpediaURI'])

# Salvataggio delle modifiche effettuate sull'ontologia
ob.save_onto()
"""
    ################################################################################################################
"""



"""
    SIMULAZIONE DI UTILIZZO DEL SISTEMA DA PARTE DI UN GENERICO UTENTE
"""
tp = TextProcessor(api, dataset_path, cat_docs, ke)
new_doc_txt = 'The Mona Lisa is a 16th century oil painting created by Leonardo. It is held at the Louvre in Paris. The Mona Lisa is a oil painting.'
new_doc_cat, new_doc_score, new_doc_fname, new_doc_keys, new_doc_ents  = tp.process_text(new_doc_txt)

# Recupero l'istanza della categoria a cui appartiene il documento
cat = ob.get_individual(new_doc_cat + '_01')

# Creazione istanza nuovo documento
new_doc_name = new_doc_cat + '_doc_' + new_doc_fname.split('.')[0]
new_doc = ob.add_individual('Document', new_doc_name)

# Assegnazione proprietà al nuovo documento
ob.add_property(new_doc, 'has_category', cat)
ob.add_property(new_doc, 'has_score_' + new_doc_cat.lower(), new_doc_score)
ob.add_property(new_doc, 'has_path', dataset_path + '/' + new_doc_cat + '/' + new_doc_fname)

# Creazione istanza delle nuove parole e assegnazione delle relative proprietà
for key in new_doc_keys.keys():
    word = ob.add_individual('Word', 'word_' + key)
    ob.add_property(new_doc, 'has_keyword', word)
    ob.add_property(word, 'has_value', key)

# Estrazione delle entità di interesse associate al documento e assegnazione.
# Ciascuna entità è identificata dal relativo URI in DBpedia e viene assegnata
# all'istanza del documento attraverso la relativa datatype property.
for ent in new_doc_ents:
    if ent['types']:
        for type in ent['types']:
            ent_type = re.search('\/(Person|Work|Organisation|Place|Event)$', type, re.IGNORECASE)

            if ent_type:
                predicate = ent_type.group(1).lower()
                ob.add_property(new_doc, 'has_' + predicate, ent['dbpediaURI'])

# Salvataggio delle modifiche effettuate sull'ontologia
ob.save_onto()
"""
    ################################################################################################################
"""