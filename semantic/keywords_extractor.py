from math import ceil

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


class KeywordsExtractor:
    """ Questa classe si occupa dell'estrazione delle keyword. """

    def __init__(self):
        self._keywords = {}
        self._countVectorizer = CountVectorizer(max_df=0.85, max_features=10000)
        self._tfidf_transformer = TfidfTransformer()

    def extract(self, category_docs, topn=10):
        """
        Estrae le keyword associate al set di documenti passati in ingresso.

        :param category_docs: dizionario contenente il set di documenti, relativi alla categoria di interesse,
        da cui estrarre le keyword. In particolare:
            - chive: rappresenta il nome del documento;
            - valore: rappresenta il testo su cui è stata effettuata l'operazione di pulizia.
        :param topn: numero di keywords che desideriamo estrarre per ogni documento. Per default vengono estratte
        le prime 10 keyword che hanno il valore più alto di TFIDF.
        :return: dizionario contenente la lista di keyword associate ad ogni documento. In particolare:
            - chiave: rappresenta il nome del documento;
            - valore: lista di keyword associate al documento.
        """
        if not category_docs:
            return {}

        count_matrix = self._countVectorizer.fit_transform(category_docs.values())
        self._tfidf_transformer.fit(count_matrix)

        return self._build_keywords(category_docs, topn)

    def __str__(self):
        """
        Stampa la lista di keyword per ogni documento.

        :return: L'output per la stampa
        """
        output = ''

        for k, v in self._keywords.items():
            output += k + ': ' + str(v) + '\n'

        return output

    def _build_keywords(self, docs, topn):
        """
        Costruisce la lista di keywords.

        :param docs: Una lista contenente il testo dei documenti.
        :return: la lista di keywords estratte.
        """
        self._keywords = {}
        feature_names = self._countVectorizer.get_feature_names()

        for k, v in docs.items():
            tfidf_vector = self._tfidf_transformer.transform(self._countVectorizer.transform([v]))
            sorted_items = self._sort_coo(tfidf_vector.tocoo())
            keywordsDict = self._extract_topn_from_vector(feature_names, sorted_items, topn)
            self._keywords[k] = keywordsDict

        return self._keywords

    def _sort_coo(self, coo_matrix):
        """
        Ordina la matrice delle cooccorrenze in ordine decrescente.

        :param coo_matrix: La matrice delle cooccorrenze.
        :return: Il set di risultati ordinati.
        """
        tuples = zip(coo_matrix.col, coo_matrix.data)
        return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

    def _extract_topn_from_vector(self, feature_names, sorted_items, topn):
        """
        Estrae le n parole chiave dalla matrice delle cooccorrenze.

        :param feature_names: Possibili keywords del dataset.
        :param sorted_items: La matrice delle cooccorrenze.
        :param topn: Le n keywords da estrarre.
        :return: Il dizionario contenente le parole chiave.
        """
        results = {}
        sorted_items = sorted_items[:topn]

        for idx, score in sorted_items:
            key = feature_names[idx]
            value = round(score, 3)
            results[key] = value

        return results
