### AUTHORS ###
# Clifton Roozendal
# Floris ten Lohuis
# Jens van Holland

## Version: 2.0.0
## Date: 24-12-2021
## Course: Web Data Processing Systems

### DESCRIPTION ###
#Search class, uses Elastic Search to get entities. 
#TODO: add some other disambiguation functions e.g. with Trident


import json
import asyncio
from elasticsearch import Elasticsearch, AsyncElasticsearch
import time
import pandas as pd

class Search:
    # class information
    input_ = "list:amb_entities"
    output_ = "dict:amb_entities"

    def __init__(self, n_results  = 10, query_increment_size = 50) -> None:
        """
        Initialisation function\n
        Input: \n
        \tNone\n
        Output: \n
        \tNone
        """
        self.e = Elasticsearch()
        # if not self.e.ping():
        #     raise ValueError("Connection to Elasticsearch failed")
        self.async_e = AsyncElasticsearch()
        #self.loop = asyncio.get_event_loop()
        self.return_n_results = n_results
        self.query_increment_size = query_increment_size
        self.search_cache = {}
        pass

    def _fastsearch(self, amb_entities, query_size):
        """
        Searches a list of given entities  \n
        Input: \n
        \t amb_entities: (list) a list of entities\n
        Output: \n
        \tam_entities
        See: https://elasticsearch-py.readthedocs.io/en/7.x/async.html
        """
        self.loop = asyncio.get_event_loop()
        results = self.loop.run_until_complete(self._asyncsearchloop(amb_entities, query_size))
        return results

    async def _asyncsearchloop(self, amb_entities, query_size):
        try:
            print(f"Number of queries: {len(amb_entities)}")
            tasks = []
            for ent in amb_entities:
                p = { "query" : { "query_string" : { "query" : ent }}}
                task = self.loop.create_task(self.async_e.search(index="wikidata_en", body=p, size = query_size))
                tasks.append(task)

            results = []
            for fut in asyncio.as_completed(tasks):
                try:
                    response = await fut
                    print(response)
                    results.append(response)
                except Exception as e:
                    # print(e)
                    results.append(False)
                    continue
        finally:
            await self.async_e.close()
            return results

    def _extractresults(self, search_results, warc_ids, ents, ent_labels):
        start = time.time()
        results = []
        i=0
        for response in search_results:
            warc_id = warc_ids[i]
            ent = ents[i]
            ent_label = ent_labels[i]

            i+=1
            if i %100 ==0:
                sec = round(time.time() - start)
                print(f"\t Extracted {i} search results for entities (Elasticsearch) in {sec} seconds ")
            if response:
                for hit in response['hits']['hits']:
                    temp_data = {
                        "label" : hit['_source']['schema_name'],
                        "score" : hit["_score"],
                        "descript" : hit['_source']['schema_description'] if "schema_description" in hit['_source'] else ""  ,
                        "hit_id" : hit['_id'],
                        "warc_id": warc_id,
                        "ent": ent,
                        "ent_label" : ent_label
                    }
                    #add to dataframe
                    results.append(temp_data)
            else:
                temp_data = {
                        "label" : "",
                        "score" : "",
                        "descript" : "",
                        "hit_id" : "",
                        "warc_id": warc_id,
                        "ent": ent,
                        "ent_label" : ent_label
                }
                #add to dataframe
                results.append(temp_data)
        return pd.DataFrame.from_dict(results, orient = 'columns')

    def fastsearch(self, amb_entities, query_size = 15):
        """
        Searches a list of given entities asynchronous (development mode - not stable) \n
        Input: \n
        \t amb_entities: (list) a list of entities\n
        Output: \n
        \tam_entities
        See: https://elasticsearch-py.readthedocs.io/en/7.x/async.html
        """
         #remove doubles and obvious wrongly entities
        start = time.time()
        
        search_results = self._fastsearch(amb_entities['ents'].values, query_size)
        results = self._extractresults(search_results, amb_entities['ids'].values, amb_entities['ents'].values, amb_entities['ent_labels'].values)
        
        stop = time.time()
        print(f"The time for fast search is: {stop - start}")
        return results

    def search(self, amb_entities, query_size = 15):
        """
        Searches a list of given entities \n
        Input: \n
        \t amb_entities: (list) a list of entities\n
        Output: \n
        \tresults of the queries (dict with {wikidatalink:entity} pairs)
        """
        results = []
        i = 0
        start = time.time()
        num_entities = len(amb_entities)
        for ent, warc_id, ent_label in zip(amb_entities['ents'].values, amb_entities['ids'].values, amb_entities['ent_labels'].values):
            i+=1
            if i %100 ==0:
                sec = round(time.time() - start)
                print(f"\t Searched {i}/{num_entities} entities (Elasticsearch) in {sec} seconds ")
            try:
                if ent in self.search_cache.keys():
                    response = self.search_cache[ent]
                else:
                    p = { "query" : { "query_string" : { "query" : ent }}}
                    #p = {'query': { "multi_match" : { "query" : ent }}}
                    response = self.e.search(index="wikidata_en", body=json.dumps(p), size = query_size)
                    self.search_cache[ent] = response
                if response:
                    for hit in response['hits']['hits']:
                        temp_data = {
                             "label" : hit['_source']['schema_name'],
                            "score" : hit["_score"],
                            "descript" : hit['_source']['schema_description'] if "schema_description" in hit['_source'] else ""  ,
                            "hit_id" : hit['_id'],
                            "warc_id": warc_id,
                            "ent": ent,
                            "ent_label" : ent_label
                        }
                        #add to dataframe
                        results.append(temp_data)
            except Exception as e:
                temp_data = {
                        "label" : "",
                        "score" : "",
                        "descript" : "",
                        "hit_id" : "",
                        "warc_id": warc_id,
                        "ent": ent,
                        "ent_label": ent_label
                }
                #add to dataframe
                results.append(temp_data)
                # print(e)
                continue

        stop = time.time()
        print(f"The time for search is: {stop - start}")
        # print(results)
        return pd.DataFrame.from_dict(results, orient = 'columns')
    
    def _forward(self, records):
        """
        Dummy function for streamlining the pipeline\n
        Input: \n
        \t amb_entities: (list) a list of entities\n
        Output: \n
        \tresults of the queries (dict with {wikidatalink:entity} pairs)
        """
        # this is used by the pipeline
        # make sure this returns the acceptable output
        # it seems redudant but _forward is universal parse functions in the pipeline
        print("--> Searching entities in wikidata (Elasticsearch) <--")

        if records['search_ES'] == "fast": #uses async
            results = self.fastsearch(records['amb_entities'], query_size= records['query_size_ES']) #amb_entitis is a pd Dataframe with cols: [ids, ents, ent_labels]

        elif records['search_ES']  == "normal":#does not use async
            results = self.search(records['amb_entities'], query_size= records['query_size_ES']) #amb_entitis is a pd Dataframe with cols: [ids, ents, ent_labels]

        if records['output_intermediates']:
            results.to_csv(records['output_folder'] + '/search_results.csv')

        results = results[results['hit_id'] != ""]

        records['wiki_links'] = results

        print("<STATUS: DONE>\n")

        return records

