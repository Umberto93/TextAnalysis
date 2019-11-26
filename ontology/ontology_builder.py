from owlready2 import *


class OntologyBuilder:
    def __init__(self, path, file_name):
        self._path = path
        self._file_name = file_name
        self._onto = get_ontology(self._path + self._file_name).load()

    def get_onto(self):
        return self._onto

    def add_individual(self, category, name):
        return self._onto[category](name)

    def get_individual(self, name):
        return self._onto[name]

    def add_property(self, subject, predicate, object):
        getattr(subject, predicate).append(object)

    def save(self):
        self._onto.save(file=self._path + self._file_name, format="rdfxml")


if __name__ == '__main__':
    ob = OntologyBuilder('', 'ontology_output.owl')
    #doc = ob.add_individual('Document', 'doc_01')
    doc = ob.get_individual('doc_01')
    word = ob.add_individual('Word', 'word_igor')
    ob.add_property(doc, 'has_keyword', word)
    ob.save()
