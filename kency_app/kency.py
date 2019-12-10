import os

from owlready2 import DataPropertyClass
from utils.file_manager import FileManager
from utils.cleaner import read_cleaned_docs
from semantic.text_processor import TextProcessor
from ontology.query_builder import QueryBuilder


class Kency:
    def __init__(self, ontology_builder, keyword_extractor, text_classifier, entity_recognizer, dataset_path, user_path):
        self._ob = ontology_builder
        self._ke = keyword_extractor
        self._er = entity_recognizer
        self._dataset_path = dataset_path
        self._user_path = user_path

        # Dizionario contenente la lista di documenti associata ad ogni categoria. In particolare:
            # - chiave: coincide con il nome della categoria;
            # - valore: rappresenta un ulteriore dizionazio in cui le coppie (chiave, valore) coincidono con le coppie
            # (nome_documento, testo_documento).
        self._cat_docs = {}
        # Gestore delle operazioni di lettura e scrittura su file.
        self._file_manager = FileManager()
        # Processa i documenti forniti in input al sistema dall'utente.
        self._tp = TextProcessor(dataset_path, user_path, {}, keyword_extractor, text_classifier, entity_recognizer)

        # Inizializzo il sistema.
        self._init_system()
        # Recupero l'ontologia.
        self._onto = self._ob.get_onto()
        # Creo un'istanza di Query Builder per eseguire query SPARQL.
        self._query_builder = QueryBuilder()

    def get_cat_docs(self):
        return self._cat_docs

    def get_categories(self):
        """ Restituisce tutti gli individui appartenenti alla classe Category. """

        res = []
        categories = self._onto.Category.instances()

        for cat in categories:
            res.append({
                'id': cat.name,
                'value': cat.has_name[0]
            })

        return res

    def get_documents(self, params, include_props=[]):
        """
        Restituisce tutti i gli individui appartenenti alla classe Document che rispettano le condizioni di
        filtraggio specificate.

        :param params: dizionario con cui specificare le condizioni di filtraggio sui documenti.
        :param include_props: lista di proprietà che è di interesse visualizzare nei documenti restituiti
        :return: lista di documenti.
        """

        for key, value in params.items():
            if type(value) == list:
                params[key] = list(map(lambda x: self._onto[x], value))
            else:
                params[key] = self._onto[value]

        docs = self._onto.search(is_a=self._onto['Document'], **params)
        return self._to_obj(docs, include_props=include_props)

    def get_document_details(self, params):
        """
        Restituisce tutte le informazioni inerenti al documento richiesto.

        :param params: dizionario contenente un parametro 'id' il cui valore coincide con il nome dell'individuo
        di classe Document da cercare.
        :return: l'individuo di classe Document richiesto, oppure None se non esiste.
        """

        if 'id' in params.keys() and type(self._onto[params['id']]) == self._onto['Document']:
            return self._build_obj(self._onto[params['id']], res={})

        return None

    def get_related_documents(self, category, keywords, min_kic=3):
        """
        Restituisce tutti i documenti appartenenti alla categoria specificata che condividono un sottoinsieme delle
        keyword passate come parametro.

        :param category: indica la categoria.
        :param keywords: rappresenta la lista di keywords.
        :param min_kic: (min_KeywordInCommon) numero minimo di keyword che un documento deve avere in comune con quelle
        passate come parametro di ingresso affinchè venga preso in considerazione
        :return: lista di individui appartenenti alla classe Document che rispettano le condizioni specificate.
        """

        res = []

        resQuery = list(self._query_builder.get_graph().query("""
        PREFIX of4: <""" + self._onto.base_iri + """>
        SELECT ?doc (COUNT(?doc) AS ?count)
            WHERE { 
                ?doc a of4:Document .
                ?doc of4:has_category ?c .
                ?c a of4:""" + category + """.
                ?doc of4:has_keyword ?k1 .
                ?k1 of4:has_value ?v1 .
                FILTER REGEX (str(?v1), '(""" + '|'.join(keywords) + """)') .
            } GROUP BY ?doc
        """))

        for r in resQuery:
            if int(r[1]) > (min_kic - 1):
                res.append(r[0].replace(self._onto.base_iri, ''))

        return res

    def get_words_starting_with(self, params):
        """
        Restituisce tutte le parole che cominciano con la stringa passata come parametro.

        :param params: dizionario contenente un parametro 'start' il cui valore indica la sottostringa da cercare
        nella parte iniziale delle parole.
        :return: lista di individui della classe Word che cominciano per la stringa passata come parametro.
        """

        if 'start' in params.keys():
            words = self._onto.Word.instances()
            filtered_words = filter(lambda w: w.has_value[0].startswith(params['start']), words)

            return list(map(lambda w: {
                'id': w.name,
                'value': w.has_value[0]
            }, filtered_words))

        return []

    def process_user_text(self, text):
        """
        Consente di processare un testo fornito in input al sistema dall'utenza. Effettua la classificazione,
        l'estrazione delle keyword e il riconoscimento delle entità presenti. Infine aggiunge l'istanza, relativa al
        testo all'interno dell'ontologia.

        :param text: testo da processare
        :return: new_doc_name: nome relativo all'individuo di classe Document appena creato.
        """

        # Setto l'insieme dei docs..
        self._tp.set_cat_docs(self._cat_docs)

        # Inizio il process text
        new_doc_cat, new_doc_fname, new_doc_keys, new_doc_ents = self._tp.process_text(text)

        # Recupero l'istanza della categoria a cui appartiene il documento
        cat = self._ob.get_individual(new_doc_cat['name'] + '_01')

        # Creazione istanza nuovo documento
        new_doc_name = new_doc_cat['name'] + '_doc_' + new_doc_fname.split('.')[0]
        new_doc = self._ob.add_individual('Document', new_doc_name)

        # Assegnazione proprietà al nuovo documento
        self._ob.add_property(new_doc, 'has_category', cat)
        self._ob.add_property(new_doc, 'has_score_' + new_doc_cat['name'].lower(), new_doc_cat['score'])
        self._ob.add_property(new_doc, 'has_path', self._user_path + '/' + new_doc_cat['name'] + '/' + new_doc_fname)

        self._ob.add_doc_keys(new_doc, new_doc_keys.keys())

        # Estrazione delle entità di interesse associate al documento e assegnazione.
        # Ciascuna entità è identificata dal relativo URI in DBpedia e viene assegnata
        # all'istanza del documento attraverso la relativa datatype property.
        self._ob.add_doc_entities(new_doc, new_doc_ents)

        # Salvataggio delle modifiche effettuate sull'ontologia
        self._ob.save_onto()

        return new_doc_name

    def run_query(self, query):
        """
        Permette di eseguire una query SPARQL, specificata dall'utente, sull'ontologia.

        :param query: stringa che indica la query da eseguire.
        :return: un dizionario contenente due campi:
            - message: messaggio contenente informazioni sull'esito della query;
            - success: valore booleano che indica l'esito dell'operazione (True se è andato tutto a buon fine,
            False altrimenti)
            - resQuery: risultato della query (in caso di errore sarà una lista vuota).
        """

        res = {
            'message': '',
            'success': False,
            'resQuery': []
        }

        try:
            res['message'] = 'Query successfully executed.'
            res['resQuery'] = list(self._query_builder.get_graph().query(query))
            res['success'] = True
        except:
            res['message'] = 'Query syntax error.'

        return res

    def _init_system(self):
        """ Effettua l'inizializzazione del sistema occupandosi della creazione o del caricamento dell'ontologia. """

        # Se non esiste il file .owl relativo all'ontologia, viene effettuata la creazione dell'ontologia.
        if not os.path.exists(self._ob.get_onto_filepath()):
            print("Inizializzazione del sistema in corso...")
            self._create_ontology()
            print("Inizializzazione completata.\n")
        else:
            print("Caricamento in corso dell'onologia dal file ", self._ob.get_onto_filepath())
            # Caricamento dell'ontologia creata in precedenza
            self._ob.load_onto(self._ob.get_onto_filepath())
            print("Caricamento completato.\n")

    def _create_ontology(self):
        """ Effettua la creazione dell'ontologia a partire dal dataset e dai documeti caricati dall'utente. """

        # Creazione dello schema ontologico
        self._ob.build_ontology_schema()

        # Lista delle categorie di interesse
        categories = os.listdir(self._dataset_path)

        # Creazione della popolazione (Knowledge Base).
        for category in categories:
            print("Elaborazione documenti relativi alla categoria ", category, " in corso...", end=" ")
            # Lettura documenti relativi alla categoria in esame e pulizia del testo.
            docs = read_cleaned_docs([self._dataset_path, self._user_path], category)

            # Assegnazione lista documenti relativi a una specifica categoria, al relativo campo
            # nel dizionario cat_docs
            self._cat_docs[category] = docs

            # Estrazione delle keywords relative alla collezione dei documenti
            docs_keywords = self._ke.extract(docs)

            # Creazione istanza della categoria e assegnazione delle relative proprietà
            cat = self._ob.add_individual(category, category + '_01')
            self._ob.add_property(cat, 'has_name', category)

            # Creazione istanze dei documenti e assegnazione delle relative proprietà
            for document, keywords in docs_keywords.items():
                file_path = self._dataset_path + '/' + category + '/' + document.replace(category + '_doc_',
                                                                                         '') + '.txt'
                doc = self._ob.add_individual('Document', document)
                self._ob.add_property(doc, 'has_category', cat)
                self._ob.add_property(doc, 'has_score_' + category.lower(), 1)
                self._ob.add_property(doc, 'has_path', file_path)

                self._ob.add_doc_keys(doc, keywords.keys())

            # Estrazione delle entità di interesse associate al documento e assegnazione.
            # Ciascuna entità è identificata dal relativo URI in DBpedia e viene assegnata
            # all'istanza del documento attraverso la relativa datatype property.
            for doc_name, doc_text in docs.items():
                doc = self._ob.get_individual(doc_name)
                doc_entities = self._er.get_entities(doc_text)
                self._ob.add_doc_entities(doc, doc_entities)

            print("completata.")

        # Salvataggio delle modifiche effettuate sull'ontologia
        self._ob.save_onto()

    def _to_obj(self, individuals, include_props=[]):
        """
        Restituisce una rappresentazione JSON della lista di individui passata come parametro.

        :param individuals: lista di individui da convertire in JSON.
        :param include_props: lista di proprietà relativi agli individui che ci interessa includere nella
        rappresentazione JSON. Se lasciata al valore di Default restituisce tutte le proprietà agganciate
        all'individuo considerato.
        :return: lista contenente le rappresentazioni JSON degli individui contenuti in individuals.
        """

        res = []

        for individual in individuals:
            res.append(self._build_obj(individual, res={}, include_props=include_props))

        return res

    def _build_obj(self, individual, res={}, inverse=None, include_props=[]):
        """
        Restituisce la rappresentazione JSON dell'individuo passato come parametro di input.

        :param individual: individuo da convertire in JSON
        :param res: dizionario in cui le coppie (chiave, valore) costituiscono la rappresentazione JSON
        dell'individuo passato come input.
        :param inverse: Inverse Property che desideriamo escludere. Per default è settata a None.
        :param include_props: lista di proprietà relative all'individuo che ci interessa convertire in JSON.
        Se lasciata al valore di Default restituisce tutte le proprietà agganciate all'individuo considerato.
        :return: un dizionario in cui le coppie (chiave, valore) costituiscono la rappresentazione JSON
        dell'individuo passato come input.
        """

        res['entity_name'] = individual.name

        if include_props:
            iterator = self._properties_iterator(individual, include_props)
        else:
            iterator = individual.get_properties()

        for prop in iterator:
            value = individual[prop.name]

            if type(prop) == DataPropertyClass:
                if prop.name == 'has_path':
                    res['has_content'] = self._get_file_content(value[0])

                res[prop.name] = value if len(value) > 1 else value[0]
            else:
                if prop != inverse:
                    res[prop.name] = []

                    for v in value:
                        res[prop.name].append(self._build_obj(v, res={}, inverse=prop.get_inverse_property()))

        return res

    def _properties_iterator(self, individual, include_props):
        """
        Restituisce un iteratore su un sottoinsieme delle proprietà associate ad un individuo.
        :param individual: individuo avente le proprietà di interesse.

        :param include_props: lista contenente i nomi delle proprietà di interesse.
        :return: un iteratore sulle proprietà di interesse.
        """

        for prop in individual.get_properties():
            if prop.name in include_props:
                yield prop

    def _get_file_content(self, filepath):
        """
        Legge il contenuto di un documento testuale.
        :param filepath: relative path del file da leggere
        :return: contenuto testuale del file.
        """
        fileManager = FileManager()

        # Project Root path
        ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

        # Lettura file e restituzione del contenuto
        return fileManager.read_file(os.path.join(ROOT_DIR, filepath))
