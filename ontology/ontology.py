from owlready2 import *

onto = get_ontology("ontology.owl")
onto.load()

instances = [x for x in onto.individuals()]
print(instances)

doc03 = onto.document('doc_05')
doc06 = onto.document('doc_06')
instances = [x for x in onto.individuals()]
print(instances)

onto.save(file = "ontology_output.owl", format = "rdfxml")
