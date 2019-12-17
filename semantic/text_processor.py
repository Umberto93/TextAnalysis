import os

from utils.file_manager import FileManager
from utils.cleaner import clean_text, read_cleaned_docs


class TextProcessor:
    """ Processa un testo fornito in input al sistema dall'utente. """

    def __init__(self, dataset_path, user_path, cat_docs, keywords_extractor, text_classifier, entity_recognizer):
        self._dataset_path = dataset_path
        self._user_path = user_path
        self._cat_docs = cat_docs
        self._ke = keywords_extractor
        self._tc = text_classifier
        self._er = entity_recognizer
        self._file_manager = FileManager()

    def set_cat_docs(self, cat_docs):
        self._cat_docs = cat_docs

    def process_text(self, text):
        """
        Prende un testo come parametro di input e utilizza le API di Meaning Cloud per effettuare l'estrazione
        della categoria di appartenenza (con relativo score) e delle API di Dandelion per l'estrazione delle entità
        contenute. Inoltre, utilizzando il TFIDF viene effettuata anche l'estrazione delle relative keywords.

        :param text: testo da processare
        :return:
            - cat: dizionario contenente il nome della categoria in cui è stato classificato il documento e il relativo
            score;
            - fname: nome del file in cui è stato salvato il testo passato come parametro in ingresso;
            - doc_keys: keywords del nuovo documento;
            - doc_ents: entità contenute nel nuovo documento;
        """

        # Uso del classificatore (API Meaning Cloud) per recuperare la categoria a cui appartiene il documento
        # insieme alla relativa percentuale di appartenenza (score).
        cat = self._tc.get_category(text)
        cat_name = cat['name']

        # Salvataggio documento nella relativa cartella utente.
        fname = self._save_doc(cat_name, text)

        # Pulizia testo
        cleaned_text = clean_text(text)
        # Estrazione keywords associate al testo
        doc_keys = self._extract_keywords(cat_name, fname, cleaned_text)
        # Estrazione entità associate al testo
        doc_ents  = self._er.get_entities(cleaned_text)

        return cat, fname, doc_keys, doc_ents

    def _save_doc(self, cat_name, text):
        """
        Salvataggio del documento nella cartella utente relativa alla categoria in cui è stato classificato il documento.

        :param cat_name: categoria a cui appartiene il documento. Il nome della cartella in cui salvare il documento
        deve coincidere con il nome della categoria estratta dal classificatore.
        :param text: testo da salvare nel documento.
        :return: nome del file in cui è stato salvato il testo.
        """

        # Costruzione del nome da assegnare al documento in cui salveremo il testo passato come parametro di ingresso.
            # Conto i file contenuti all'interno della cartella relativa alla categoria a cui appartiene il documento
        num_docs = len(os.listdir(self._user_path + '/' + cat_name))
            # Aggiungo 1 e ottengo, così, il nome da assegnare al nuovo documento.
        fname = 'user_' + str(num_docs + 1) + '.txt'

        self._file_manager.write_file(self._user_path + '/' + cat_name + '/' + fname, text)
        return fname

    def _extract_keywords(self, cat_name, fname, cleaned_text):
        """
        Estrazione delle keyword relative al testo passato come parametro di input.

        :param cat_name: nome della categoria a cui appartiene il testo classificato.
        :param fname: nome del file in cui è stato salvato il testo inziale.
        :param cleaned_text: testo pulito.
        :return: keywords relative al documento in esame.
        """

        # Se non si dispone della collezione di documenti relativi alla categoria in esame, viene effettuata la relativa
        # lettura e la pulizia.
        if not cat_name in self._cat_docs:
            print("lettura documenti...", end=" ")
            self._cat_docs[cat_name] = read_cleaned_docs([self._dataset_path, self._user_path], cat_name)
            print("completata.")

        # Recupero tutti i documenti relativi alla categoria a cui appartiene il nuovo documento
        docs = self._cat_docs[cat_name]

        # Estrazione delle keywords relative al documento in esame
        doc_istance_name = cat_name + '_doc_' + fname.split('.')[0]
        docs[doc_istance_name] = cleaned_text
        doc_keys = self._ke.extract(docs)[doc_istance_name]

        return doc_keys