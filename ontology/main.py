from owlready2 import default_world, sync_reasoner
import time

default_world.set_backend(filename = "./file.sqlite3")
onto = default_world.get_ontology("../kency/of4-ontology.owl").load()

sync_reasoner(default_world)
graph = default_world.as_rdflib_graph()

of4 = 'http://www.fantastic4.org/BigData/FinalProject/of4-ontology.owl#'
start = time.time()

res = onto.Word.instances()
res = list(filter(lambda w: w.has_value[0].startswith('sna'), res))

end = time.time()
print(end - start)

print(res)

"""print(default_world[str(r[0][0])])
uri_1 = of4 + 'word_google'
uri_2 = of4 + 'word_timewarner'
print(onto.search(has_keyword=[default_world[uri_1], default_world[uri_2]]))"""
