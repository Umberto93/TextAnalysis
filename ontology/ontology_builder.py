import math
from owlready2 import *
import re


class OntologyBuilder:
    """ Fornisce metodi per gestire la creazione e modifica dell'ontologia. """

    def __init__(self,
                 onto_URI='http://www.fantastic4.org/BigData/FinalProject/of4-ontology.owl',
                 onto_filepath='./of4-ontology.owl'):
        self._onto = get_ontology(onto_URI)
        self._onto_filepath = onto_filepath

    def get_onto(self):
        return self._onto

    def get_onto_filepath(self):
        """ Restituisce il percorso al file in cui risiede l'ontologia. """
        return self._onto_filepath

    def load_onto(self, onto_file_path):
        """
        Consente di effettuare il caricamento dell'ontologia salvata in un file.

        :param onto_file_path: percorso al file in cui risiede l'ontologia da caricare.
        :return: l'ontologia caricata.
        """
        self._onto = get_ontology(onto_file_path).load()
        self.build_ontology_schema()
        self._onto_filepath = onto_file_path
        return self._onto

    def add_individual(self, class_name, name):
        """
        Consente di aggiungere un nuovo individuo all'ontologia.
        Restituisce l'individuo avente come nome 'name' se risulta già presente, altrimenti crea un nuovo individuo
        di classe 'class_name' e nome 'name'.

        :param class_name: identifica la classe ontologica, ovvero il tipo del nuovo individuo.
        :param name: identifica il nome da dare alla nuova istanza.
        :return: l'individuo.
        """
        return self._onto[name] if self._onto[name] else self._onto[class_name](name)

    def get_individual(self, name):
        """
        Consente di recuperare un certo individuo nell'ontologia.

        :param name: identifica il nome dell'individuo che intendiamo recuperare.
        :return: l'individuo cercato.
        """
        return self._onto[name]

    def add_property(self, subject, predicate, object):
        """
        Consente di aggiungere una nuova proprietà a un certo individuo.

        :param subject: individuo al quale desideriamo aggiungere una nuova proprietà.
        :param predicate: proprietà (Object Property o Datatype Property) che vogliamo assegnare all'individuo.
        :param object: valore (individuo o letterale) da assegnare alla proprietà.
        """

        # Il valore di una Object o Datatype Property associata a un certo inividuo è una lista di oggetti (individui
        # o valori). L'aggiunta alla lista deve essere effettuata se e solo se l'oggetto non è presente al suo interno.
        if object not in getattr(subject, predicate):
            getattr(subject, predicate).append(object)

    def add_doc_keys(self, document, keys):
        """
        Effettua l'aggiunta delle keyword al documento dopo averle create o recuperate.

        :param document: individuo, di classe Document, al quale desideriamo aggiungere le keywords.
        :param keys: lista dei valori relativi alle keyword da aggiungere.
        """

        # Creazione istanza delle nuove parole e assegnazione delle relative proprietà
        for key in keys:
            word = self.add_individual('Word', 'word_' + key)
            self.add_property(document, 'has_keyword', word)
            self.add_property(word, 'has_value', key)

    def add_doc_entities(self, document, entities):
        """
        Effettua l'aggiunta delle entità al documento.

        :param document: individuo, di classe Document, al quale desideriamo aggiungere le keywords.
        :param entities:  lista di entità recuperate attraverso l'EntityRecognizer.
        """

        for entity in entities:
            if entity['types']:
                for type in entity['types']:
                    entity_type = re.search('\/(Person|Work|Organisation|Place|Event)$', type, re.IGNORECASE)

                    if entity_type:
                        predicate = entity_type.group(1).lower()
                        self.add_property(document, 'has_entity_' + predicate, entity['dbpediaURI'])

    def save_onto(self):
        """ Consente di effettuare il salvataggio su file dell'ontologia. """
        self._onto.save(file=self._onto_filepath, format="rdfxml")

    def build_ontology_schema(self):
        """
        Consente di creare lo schema ontologico relativo alla nuova ontologia ma viene anche utilizzato per offrire a
        Python la possibilità di conoscere le caratteristiche degli individui presenti nell'ontologia e trattarli come
        normali oggetti. Così facendo, Python sarà in grado di effettuarne la serializzazione.
        """
        with self._onto:
            # DICHIARAZIONE DELLE CLASSI
            class Category(Thing):
                def __getitem__(self, name):
                    return getattr(self, name)

            class Business(Category): pass

            class Entertainment(Category): pass

            class Sport(Category): pass

            class Politics(Category): pass

            class Technology(Category): pass

            class Health(Category): pass

            class Other(Category): pass

            class Document(Thing):
                def __getitem__(self, name):
                    return getattr(self, name)

            class Word(Thing):
                def __getitem__(self, name):
                    return getattr(self, name)

            # DICHIARAZIONE DELLE OBJECT PROPERTY
            class has_document(ObjectProperty): pass

            class is_keyword_of(ObjectProperty): pass

            class has_category(Document >> Category):
                inverse_property = has_document

            class has_keyword(Document >> Word):
                inverse_property = is_keyword_of

            # DICHIARAZIONE DELLE DATATYPE PROPERTY
            class has_entity_event(Document >> str): pass

            class has_entity_organisation(Document >> str): pass

            class has_entity_person(Document >> str): pass

            class has_entity_place(Document >> str): pass

            class has_entity_work(Document >> str): pass

            class has_score_business(Document >> float): pass

            class has_score_entertainment(Document >> float): pass

            class has_score_sport(Document >> float): pass

            class has_score_politics(Document >> float): pass

            class has_score_technology(Document >> float): pass

            class has_score_health(Document >> float): pass

            class has_score_other(Document >> float): pass

            class has_name(Category >> str): pass

            class has_value(Word >> str): pass

            class has_path(Document >> str): pass
