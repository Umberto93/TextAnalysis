from utils.query_builder import QueryBuilder
from owlready2 import *
from utils.file_manager import FileManager
from ontology.ontology_builder import OntologyBuilder


class KencyAPI:
    def __init__(self, onto):
        self._onto = onto
        self._query_builder = QueryBuilder()

    def get_categories(self):
        res = []
        categories = self._onto.Category.instances()

        for cat in categories:
            res.append({
                'id': cat.name,
                'value': cat.has_name[0]
            })

        return res

    def get_documents(self, params):
        for key, value in params.items():
            if type(value) == list:
                params[key] = list(map(lambda x: self._onto[x], value))
            else:
                params[key] = self._onto[value]

        return self._to_obj(self._onto.search(**params))

    def get_related_documents(self, category, keywords, min_kic=2):
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
        words = self._onto.Word.instances()
        filtered_words = filter(lambda w: w.has_value[0].startswith(params['start']), words)

        return list(map(lambda w: {
            'id': w.name,
            'value': w.has_value[0]
        }, filtered_words))

    def _to_obj(self, individuals):
        res = []

        for individual in individuals:
            res.append(self._build_obj(individual, res={}))

        return res

    def _build_obj(self, individual, res={}, inverse=None):
        for prop in individual.get_properties():
            value = individual[prop.name]

            if type(prop) == DataPropertyClass:
                if prop.name == 'has_path':
                    res['has_content'] = self._get_file_content(value[0])

                res['entity_name'] = individual.name
                res[prop.name] = value if len(value) > 1 else value[0]
            else:
                if prop != inverse:
                    res[prop.name] = []

                    for v in value:
                        res[prop.name].append(self._build_obj(v, {}, prop.get_inverse_property()))

        return res

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


if __name__ == '__main__':
    ob = OntologyBuilder()
    onto = ob.load_onto('../kency/of4-ontology.owl')
    k = KencyAPI(onto)
    res = k.get_words_starting_with({
        'start': 'sna'
    })
    print(res)
