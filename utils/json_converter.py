import os
import owlready2

from utils.file_manager import FileManager

class JSONConverter:
    """  Questa effettua la conversione in formato JSON di un oggetto. """
    def __init__(self):
        pass

    def to_json(self, obj):
        """
        Restituisce la rappresentazione JSON dell'oggetto passato come parametro in input
        :param obj: oggetto da serializzare in JSON
        :return: oggetto serializzato in JSON
        """

        # Converto la lista di attributi e valori associati all'oggetto in un dizionario.
        obj = obj.__dict__

        # Per ogni coppia (chiave, valore), ovvero (proprietà, lista di valori), invoco il metodo _list_to_json().
        for prop, individual_list in obj.items():
            obj[prop] = self._list_to_json(individual_list)

        # Verifico la presenza della proprietà Path sull'oggetto in esame.
        if (obj['path'] and len(obj['path']) > 0):
            # Recupero il path del file
            filepath = obj['path'][0]
            # Recupero il contenuto del file e aggiungo all'oggetto la coppia (K, V): (text, text_content)
            obj['text'] = self._get_file_content(filepath)

        return obj

    def _list_to_json(self, list_obj):
        """
        Converte la lista di individui o lista di valori, passata in input associata ad una certa proprietà, nel relativo
        formtato JSON.
        :param list_obj: lista di individui o valori da convertire
        :return: rappresentazione JSON di list_obj
        """

        # Verifico se list_obj non è una lista di Individui
        if (type(list_obj) is not owlready2.prop.IndividualValueList):
            # Se possibile, converto list_obj in un dizionario
            if (hasattr(list_obj, '__dict__')):
                list_obj = list_obj.__dict__
            return list_obj
        # Se list_obj è una IndividualValueList inizio a convertire i relativi elementi in formato JSON
        else:
            # Lista vuota contenente le rappresentazioni JSON degli individui in list_obj
            individuals = []

            for item in list_obj:
                # Inserisco nella lista la relativa rappresentazione JSON dell'oggetto 'item' in esame
                individuals.append(self._list_to_json(item))
            return individuals


    def _get_file_content(self, filepath):
        """
        Legge il contenuto di un documento testuale.
        :param filepath: relative path del file da leggere
        :return: contenuto testuale del file.
        """

        fileManager = FileManager()

        # Project Root path
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

        # Lettura file e restituzione del contenuto
        return fileManager.read_file(ROOT_DIR + filepath)
