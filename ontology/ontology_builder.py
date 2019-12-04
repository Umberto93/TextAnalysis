from owlready2 import *


class OntologyBuilder:
    def __init__(self,
                 onto_URI='http://www.fantastic4.org/BigData/FinalProject/of4-ontology.owl',
                 onto_filepath='./of4-ontology.owl'):
        self._onto = get_ontology(onto_URI)
        self._onto_filepath = onto_filepath

    def get_onto(self):
        return self._onto

    def load_onto(self, onto_file_path):
        self._onto = get_ontology(onto_file_path)
        self._onto.load()
        self.build_ontology_schema()
        self._onto_filepath = onto_file_path
        return self._onto

    def add_individual(self, category, name):
        return self._onto[category](name)

    def get_individual(self, name):
        return self._onto[name]

    def add_property(self, subject, predicate, object):
        getattr(subject, predicate).append(object)

    def save_onto(self):
        self._onto.save(file=self._onto_filepath, format="rdfxml")

    def build_ontology_schema(self):
        with self._onto:
            # ONTOLOGY CLASS DECLARATION
            class Category(Thing):
                def __getitem__(self, name):
                    return getattr(self, name)

                pass

            class Business(Category):
                pass

            class Entertainment(Category):
                pass

            class Sport(Category):
                pass

            class Politics(Category):
                pass

            class Technology(Category):
                pass

            class Health(Category):
                pass

            class Document(Thing):
                def __getitem__(self, name):
                    return getattr(self, name)

                pass

            class Word(Thing):
                def __getitem__(self, name):
                    return getattr(self, name)

                pass

            # OBJECT PROPERTY DECLARATION
            class has_document(ObjectProperty):
                pass

            class is_keyword_of(ObjectProperty):
                pass

            class has_category(Document >> Category):
                inverse_property = has_document
                pass

            class has_keyword(Document >> Word):
                inverse_property = is_keyword_of
                pass

            # DATATYPE PROPERTY DECLARATION
            class has_event(Document >> str):
                pass

            class has_organisation(Document >> str):
                pass

            class has_person(Document >> str):
                pass

            class has_place(Document >> str):
                pass

            class has_work(Document >> str):
                pass

            class has_score_business(Document >> float):
                pass

            class has_score_entertainment(Document >> float):
                pass

            class has_score_sport(Document >> float):
                pass

            class has_score_politics(Document >> float):
                pass

            class has_score_technology(Document >> float):
                pass

            class has_score_health(Document >> float):
                pass

            class has_name(Category >> str):
                pass

            class has_value(Word >> str):
                pass

            class has_path(Document >> str):
                pass


if __name__ == '__main__':
    ob = OntologyBuilder()
    ob.build_ontology_schema()
    ontology = ob.get_onto()
    print(ontology)

    d = ontology.Document('doc_01')
    print(d)
    w1 = ontology.Word('word_01')
    print(w1)
    w2 = ontology.Word('word_02')
    print(w2)

    getattr(d, 'path').append('../dataset/ciao.txt')
    getattr(w1, 'has_value').append('deficit')
    getattr(d, 'has_keyword').append(w1)
    getattr(w2, 'has_value').append('play')
    getattr(d, 'has_keyword').append(w2)
    getattr(d, 'has_category').append(ontology.Business('Business_01'))
    getattr(ontology.Business_01, 'has_name').append('Business')

    ob.save_onto()
