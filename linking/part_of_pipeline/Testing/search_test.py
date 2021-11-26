import json
import asyncio
from elasticsearch import Elasticsearch, AsyncElasticsearch
import time    

class Search:
    # class information
    input_ = "list:amb_entities"
    output_ = "dict:amb_entities"

    def __init__(self) -> None:
        """
        Initialisation function\n
        Input: \n
        \tNone\n
        Output: \n
        \tNone
        """
        self.e = Elasticsearch(timeout=60)
        self.async_e = AsyncElasticsearch()
        pass

    def search(self, amb_entities):
        """
        Searches a list of given entities \n
        Input: \n
        \t amb_entities: (list) a list of entities\n
        Output: \n
        \tresults of the queries (dict with {wikidatalink:entity} pairs)
        """
        results = []
        start = time.time()

        #remove doubles and obvious wrongly entities
        #amb_entities = self._remove(amb_entities)
        queryString = []
        for ent in amb_entities:
            queryString.append({"query_string" :{ "query" : ent }})
            #TODO: we need to find a way to make the quering more efficient (i.e. batches possible?)
            #p = { "query" : { "query_string" : { "query" : ent }}}
        p = { "query" : { "bool" : { "should" : queryString}}}
        #try:
        response = self.e.search(index="wikidata_en", body=json.dumps(p))
        stop = time.time()
        print(f"The time up to current search is: {stop - start}")
        id_labels = {}
        if response:
            for hit in response['hits']['hits']:
                label = hit['_source']['schema_name']
                id = hit['_id']
                id_labels.setdefault(id, set()).add(label)
        results.append({ent: id_labels})
            #except:
            #    continue
            #TODO: a lot of duplicates (might also impact computation time)
        stop = time.time()
        print(f"The time for search is: {stop - start}")
        # print(results)
        return results

#Code
entities = ["This","is","a","test","for","our","search","model"] * 100
searcher = Search()
results = searcher.search(entities)

for result in results:
    print(result)