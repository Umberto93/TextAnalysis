import os
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from utils.file_manager import FileManager


class KeywordsExtractor:
    def __init__(self, path, topn=10, lang='english'):
        self._docs = {}
        self._keywords = {}
        self._dirname = ''
        self._path = path
        self._lang = lang
        self._file_manager = FileManager()
        self._countVectorizer = CountVectorizer(max_df=0.85, max_features=10000)
        self._tfidf_transformer = TfidfTransformer()

        self._initialize(topn)

    def get_keywords(self):
        """
        Restituisce la lista di parole chiave.
        :return: La lista di parole chiave.
        """
        return self._keywords

    def _initialize(self, topn=10):
        """
        Estrae le keyworrds dal dataset.
        :param topn: Il numero di parole chiave che si vuole estrarre per ciascun documento.
        :return: La lista di parole chiave estratte per ogni documento.
        """
        files = os.listdir(self._path)
        self._dirname = os.path.basename(self._path)

        for file_name in files:
            self._docs[self._dirname + '_doc_' + file_name.split('.')[0]] = self._get_cleaned_text(self._path + '/' + file_name)

        count_matrix = self._countVectorizer.fit_transform(self._docs.values())
        self._tfidf_transformer.fit(count_matrix)

        self._build_keywords(self._docs, topn)
        return self._keywords

    def extract(self, file_name, topn=10):
        """
        Estrae le keywords di uno specifico documento.
        :param file_name: Nome del documento.
        :param topn: Il numero di parole chiave che si vuole estrarre per ciascun documento.
        :return: La lista di parole chiave estratte per quel documento.
        """
        key = self._dirname + '_doc_' + file_name.split('.')[0]
        self._docs[key] = self._get_cleaned_text(self._path + '/' + file_name)
        count_matrix = self._countVectorizer.fit_transform(self._docs.values())
        self._tfidf_transformer.fit(count_matrix)
        self._build_keywords(self._docs, topn)

        return self._keywords[key]

    def __str__(self):
        """
        Stampa la lista di keyword per ogni documento
        :return: L'output per la stampa
        """
        output = ''

        for k, v in self._keywords.items():
            output += k + ': ' + str(v) + '\n'

        return output

    def _get_cleaned_text(self, path):
        """
        Legge il contenuto di un file ed effettua la pulizia del testo.
        :param path: Il path del file da leggere.
        :return: Il testo pulito.
        """
        tokenizer = RegexpTokenizer(r'\w{4,}')
        stop_words = set(stopwords.words(self._lang))
        lemmatizer = WordNetLemmatizer()
        clean_text = ''

        # Legge il contenuto del file
        text = self._file_manager.read_file(path).lower()
        # Estrae i token dal file rimuovendo i caratteri speciali e
        # le parole con meno di 4 caratteri
        tokens = tokenizer.tokenize(text)

        # Costruisce una nuova stringa a partire dal contenuto del file
        # letto in precedenza ignorando le stop words.
        for word in tokens:
            if not word in stop_words:
                clean_text += lemmatizer.lemmatize(word) + ' '

        return clean_text

    def _build_keywords(self, docs, topn):
        """
        Costruisce la lista di keywords.
        :param docs: Una lista contenente il testo dei documenti.
        :return:
        """
        feature_names = self._countVectorizer.get_feature_names()

        for k, v in docs.items():
            tfidf_vector = self._tfidf_transformer.transform(self._countVectorizer.transform([v]))
            sorted_items = self._sort_coo(tfidf_vector.tocoo())
            keywordsDict = self._extract_topn_from_vector(feature_names, sorted_items, topn)
            self._keywords[k] = keywordsDict

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


if __name__ == '__main__':
    ke = KeywordsExtractor('../dataset/sport')
    fm = FileManager()
    fm.write_file('../dataset/sport/511.txt', fm.read_file('../dataset/511.txt'))
    keys = ke.extract('511.txt', topn=10)
    print(keys)
