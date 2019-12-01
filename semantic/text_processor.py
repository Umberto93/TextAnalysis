import os

from utils.file_manager import FileManager
from utils.text_cleaner import get_cleaned_text


class TextProcessor:
    def __init__(self, api, dataset_path, categories, keywords_extractor):
        self._api = api
        self._dataset_path = dataset_path
        self._categories = categories
        self._ke = keywords_extractor
        self._file_manager = FileManager()

    def process_text(self, text):
        """
        Prende un testo come parametro di input e utilizza le API di Dandelion per effettuare l'estrazione
        della categoria di appartenenza (con relativo score) e delle entità contenute. Inoltre, utilizzando
        il TFIDF viene effettuata anche l'estrazione delle relative keywords.
        :param text: testo da processare
        :return:
            doc_cat: categoria di appartenenza del nuovo documento;
            doc_score: percentuale di appartenenza alla categoria indicata, calcolato da Dandelion;
            fname: nome del file in cui è stato salvato il testo passato come parametro in ingresso;
            doc_keys: keywords del nuovo documento;
            doc_ents: entità contenute nel nuovo documento;
        """

        # Uso del classificatore (API Dandelion) per recuperare la categoria a cui appartiene il documento
        # insieme alla relativa percentuale di appartenenza (score).
        doc_cat = self._api.get_categories(text)['name'].capitalize()
        doc_score = self._api.get_categories(text)['score']

        # Costruzione del nome da assegnare al documento in cui salveremo il testo passato come parametro di ingresso.
            # Conto i file contenuti all'interno della directory relativa alla categoria a cui appartiene il documento
        num_docs = len(os.listdir(self._dataset_path + '/' + doc_cat))
            # Aggiungo 1 e ottengo, così, il nome da assegnare al nuovo documento.
        fname = str( num_docs + 1) + '.txt'

        # Se la categoria del testo fornito in input rientra in quelle di interesse, viene effettuato il salvataggio
        # su file.
        if(doc_cat in self._categories.keys()):
            self._file_manager.write_file(self._dataset_path + '/' + doc_cat + '/' + fname, text)

            # Recupero tutti i documenti relativi alla categoria a cui appartiene il nuovo documento
            docs = self._categories[doc_cat]

            # Estrazione delle keywords relative al documento in esame
            doc_istance_name = doc_cat + '_doc_' + fname.split('.')[0]
            docs[doc_istance_name] = get_cleaned_text(text)
            doc_keys = self._ke.extract(docs)[doc_istance_name]

            doc_ents  = self._api.get_entities(docs[doc_istance_name])
            print(doc_ents)
        else:
            # DA GESTIRE
            pass

        return doc_cat, doc_score, fname, doc_keys, doc_ents
