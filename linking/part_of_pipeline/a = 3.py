# https://medium.com/@mishra.thedeepak/doc2vec-simple-implementation-example-df2afbbfbad5
import nltk
nltk.download("punkt")

from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.models import KeyedVectors
from nltk.tokenize import word_tokenize
word_tokenize("#hi Twitter hashtag")

import spacy
nlp = spacy.load('en_core_web_sm')

sentences = ["Based on Ocular Professor § Powered by WordPress"]
doc = nlp("Based on Ocular Professor § Powered by WordPress")
doc.ents
from gensim.utils import tokenize
list(tokenize("#hi Twitter hashtag"))
candidates = [("Twitter1", "micro-blogging Internet service"),
("Twitter2", "Twitter client"),
("Twitter3", "#hi Twitter hashtag"),
("Twitter4", "Twitter user"),
("Twitter5", "Twitter Legend"),
("Twitter6", "491st strip of the webcomic xkcd"),
("Twitter7", "API of Twitter")]

tokenized_sen = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(sentences)]
tokenized_candidates =  [TaggedDocument(words=word_tokenize(k[1].lower()), tags=[str(i)]) for i, k in enumerate(candidates)]

import gensim.downloader as api
models = [
    "fasttext-wiki-news-subwords-300",
    "glove-wiki-gigaword-300",
    "glove-wiki-gigaword-100",
    "glove-wiki-gigaword-50",
    "conceptnet-numberbatch-17-06-300"
]
model = api.load(models[1])
type(model)
# vecs = model.wv
a = " rss § atom § rdf Photos aggregator dynamic content Search: Add album/Contact us News Reviews shaggyshoo has added a photo to the pool: annecy. france. France image Pool 2012-02-10 16:22:52 February 10th, 2012 Tags cloud 2008 amateur photographer baby blue car cat con ct ds el est flickr hot ice image la lady man me men mer nb ol one people photo photos photos pictures amateur photographer pictures port q ran red riot Tunis Tunisia up us vie xtWP Cumulus Flash tag cloud by Roy Tanck and Luke Morton requires Flash Player 9 or better.  Twits from 'photobabble' No public Twitter messages. Based on Ocular Professor § Powered by WordPress"
a = open("temp.txt", 'rt').read().replace("\n", " ")
# a = " No public Twitter messages. Based "
model['#']
import numpy as np
vecs = []
# for word in a.lower().split(r" "):
for word in word_tokenize(a):
    try:
         vecs.append(model[word])
    except KeyError:
        continue
vecs= np.array(vecs).sum(axis = 0)

ent_vecs = []
for _, descript in candidates:
    print(descript)
    temp = []
    # for word in descript.split(r" "):
    for word in word_tokenize(descript):
        try:
            temp.append(model[word])
        except KeyError:
            continue
    ent_vecs.append(np.array(temp).sum(axis = 0))


# ent_vecs= np.array(ent_vecs)
from scipy.spatial.distance import cosine, hamming, jaccard, euclidean, correlation
print(cosine(vecs, ent_vecs[0]))
print(cosine(vecs, ent_vecs[1]))
print(cosine(vecs, ent_vecs[2]))
print(cosine(vecs, ent_vecs[3]))
print(cosine(vecs, ent_vecs[4]))
print(cosine(vecs, ent_vecs[6]))

print(euclidean(vecs, ent_vecs[0]))
print(euclidean(vecs, ent_vecs[1]))
print(euclidean(vecs, ent_vecs[2]))
print(euclidean(vecs, ent_vecs[3]))
print(euclidean(vecs, ent_vecs[4]))
print(euclidean(vecs, ent_vecs[6]))

print(correlation(vecs, ent_vecs[0]))
print(correlation(vecs, ent_vecs[1]))
print(correlation(vecs, ent_vecs[2]))
print(correlation(vecs, ent_vecs[3]))
print(correlation(vecs, ent_vecs[4]))
print(correlation(vecs, ent_vecs[6]))
# print(cosine(vecs, ent_vecs[7]))

# # # len(model['hi'])
# # dir(model)

# # from gensim.similarities import docsim
# # dir(docsim)

# # info = api.info()
# # for model_name, model_data in sorted(info['models'].items()):
# #     print(
# #         '%s (%d records): %s' % (
# #             model_name,
# #             model_data.get('num_records', -1),
# #             model_data['description'][:40] + '...',
# #         )
# #     )


# ####trident
# import trident
# QUERY_FORMAT = """PREFIX wd: <http://www.wikidata.org/entity/> 
# SELECT ?o 
# WHERE { wd:Q918 schema:description ?o.}"""
# # # PREFIX schema: <http://schema.org/> 
# # schema:description ?o. FILTER ( lang(?o) = "en" ) }"
# #Retrieve first 10 entities of type (P31) city (Q515)
# query="PREFIX wde: <http://www.wikidata.org/entity/> "\
#     "select ?s where {  wde:Q918 ?s. } "

# query = """
# prefix wde: <http://www.wikidata.org/entity/>
# SELECT ?item  WHERE {
#   ?item wde:Q918 .
# } limit 10
# """

# query = """
# prefix wdt: <http://www.wikidata.org/prop/direct/>
# prefix wd: <http://www.wikidata.org/entity/>
# PREFIX wikibase: <http://wikiba.se/ontology#>
# SELECT ?Name ?itemDescription ?Birthday WHERE {
#   ?item wdt:P569 ?Birthday .
#   ?item wdt:P27 wd:Q30 .
#   OPTIONAL { ?item wdt:P570 ?dummy0 }
#   FILTER(!bound(?dummy0))
# }
# ORDER BY ASC(?time0)
# """

# # query="""PREFIX wde: <http://www.wikidata.org/entity/> 
# #     PREFIX wdp: <http://www.wikidata.org/prop/direct/> 
# #     select ?s where { ?s wdp:P31 wde:Q515 . } LIMIT 10"""
# # # PREFIX wdt: <http://www.wikidata.org/prop/direct/> 
# #
# 	# SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
# #
# KBPATH = "assets/wikidata-20200203-truthy-uri-tridentdb"
# wdp:P31 
#    "PREFIX wdp: <http://www.wikidata.org/prop/direct/> "\
# "PREFIX wdpn: <http://www.wikidata.org/prop/direct-normalized/> "\
# LIMIT 10
# db = trident.Db(KBPATH)
# print(db.sparql(query))

# import requests
import asyncio
import aiohttp
import time
# https://stackoverflow.com/questions/51912599/get-records-for-a-list-of-multiple-entities-on-wikidata
url = 'https://query.wikidata.org/sparql'
query = '''
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX schema: <http://schema.org/>

SELECT ?o
WHERE 
{
  wd:Q918 schema:description ?o.
  FILTER ( lang(?o) = "en" )
}
'''
l = [query]*10
rs = (grequests.get(u) for u in l)
grequests.map(rs)

# r = requests.get(url, params = {'format': 'json', 'query': query})
# data = r.json()
# print(data)
from elasticsearch import Elasticsearch, AsyncElasticsearch
import json
q = json.dumps({ "query" : { "query_string" : { "query" : 'Twitter' }}})
e = Elasticsearch()
e.search( body=q, size =15)