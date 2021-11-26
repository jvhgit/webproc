### AUTHORS ###
## Clifton Roozendal
## Floris ten Lohuis
## Jens van Holland

## Version: 1.0.1
## Date: 21-11-2021
## Course: Web Data Processing Systems

### DESCRIPTION ###
#Search class, uses Elastic Search to get entities. 
#TODO: add some other disambiguation functions e.g. with Trident


import json
import asyncio
from elasticsearch import Elasticsearch, AsyncElasticsearch
import time
import elasticsearch
import tqdm.asyncio
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
        self.async_e = AsyncElasticsearch()
        self.return_n_results = n_results
        self.query_increment_size = query_increment_size
        pass
    
    ## MOVE THIS TO extract.py ! ##
    # def _remove(self, amb_entities):
    #     """
    #     Removes obviously wrong entities (doubles, single characters, weird characters?) \n
    #     Input: \n
    #     \t amb_entities: (list) a list of entities\n
    #     Output: \n
    #     \tam_entities
    #     """

    #     #
    #     temp_result = list(set(amb_entities)) #property of set is no doubles allowed->than cast to list again

    #     return temp_result

    async def _search(self, query):
        """
        Removes obviously wrong entities (doubles, single characters, weird characters?) \n
        Input: \n
        \t amb_entities: (list) a list of entities\n
        Output: \n
        \tam_entities
        See: https://elasticsearch-py.readthedocs.io/en/7.x/async.html
        """
        # print(help(self.async_e.search))
        try: 
            response = await self.e.search(
                index="wikidata_en",
                body=query[0],
                # size= self.return_n_results
                # size = 20
                # retry_on_timeout=True
                timeout = '15s'
            )
            # async with response:
            id_labels = {}
            if response:
                for hit in response['hits']['hits']:
                    label = hit['_source']['schema_name']
                    id = hit['_id']
                    id_labels.setdefault(id, set()).add(label)
            return {query[1]:id_labels}
        except :
            return {}

    # async def test(self, json_queries):
    #     query_group = asyncio.gather(*[self._search(q) for q in json_queries])
    #     for g in tqdm.asyncio.tqdm.as_completed(query_group):
    #         await g

    def fastsearch(self, amb_entities):
        """
        Removes obviously wrong entities (doubles, single characters, weird characters?) \n
        Input: \n
        \t amb_entities: (list) a list of entities\n
        Output: \n
        \tam_entities
        See: https://elasticsearch-py.readthedocs.io/en/7.x/async.html
        """
         #remove doubles and obvious wrongly entities
        start = time.time()
        # amb_entities = self._remove(amb_entities)
        results = []
        #set queries
        json_queries = [(json.dumps({ "query" : { "query_string" : { "query" : ent }}}), ent) for ent in amb_entities.ents ]
        print(json_queries[0])
        print(f"Number of queries: {len(json_queries)}")
        total_num_increments = len(json_queries) // self.query_increment_size + 1
        for increment in range(total_num_increments):
            query_group = asyncio.gather(*[self._search(q) for q in json_queries[increment*self.query_increment_size:(increment +1)*self.query_increment_size]])
            loop = asyncio.get_event_loop()
            results.append(loop.run_until_complete(query_group))
            stop = time.time()
            print(f"The time for search  is: {stop - start} (increment {increment}/{total_num_increments})")
            time.sleep(1)
            break
        print(results)

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
        start = time.time()

        #remove doubles and obvious wrongly entities
        # amb_entities = self._remove(amb_entities)
        i = 0
        start = time.time()
        num_entities = len(amb_entities)
        for ent, warc_id in zip(amb_entities['ents'].values, amb_entities['ids'].values ):
            i+=1
            if i %100 ==0:
                sec = round(time.time() - start)
                print(f"\t Searched {i}/{num_entities} entities (Elasticsearch) in {sec} seconds ")
                # if i == 100: #during test runs
                #     break
            #TODO: we need to find a way to make the quering more efficient (i.e. batches possible?)
            p = { "query" : { "query_string" : { "query" : ent }}}
            try:
                response = self.e.search(index="wikidata_en", body=json.dumps(p), size = query_size)
                # response_data = [] 
                if response:
                    for hit in response['hits']['hits']:
                        temp_data = {
                            "label" : hit['_source']['schema_name'],
                            "score" : hit["_score"],
                            "descript" : hit['_source']['schema_description'] if "schema_description" in hit['_source'] else ""  ,
                            "hit_id" : hit['_id'],
                            "warc_id": warc_id
                        }
                        #add to dataframe
                        results.append(temp_data)
            except Exception as e:
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
        #DOES NOT WORK :(
        if records['search_ES'] == "fast": #uses async
            records['wiki_links'] = self.fastsearch(records['amb_entities']) #amb_entitis is a pd Dataframe with cols: [ids,ents]
            return records

        elif records['search_ES']  == "normal":#does not use async
            records['wiki_links'] = self.search(records['amb_entities'], query_size= records['query_size_ES'])
        print("<STATUS: DONE>\n")

        return records

