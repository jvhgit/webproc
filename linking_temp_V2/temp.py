# with gzip.open(complete_path, 'rt', errors='ignore') as fo:

{a: "1" for a in range(10)}

import spacy
nlp = spacy.load("en_core_web_sm")
texts = ["I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook", "I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook", "I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook", "I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook", "I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook", "I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook", "I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook", "I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook", "I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook","I am Jens van Holland Facebook", "I am not Jens van Holland Facebook"]
docs = nlp.pipe(texts=texts, batch_size = 2, n_process=10, disable=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"])
# doc = nlp("I am Jens van Holland")

import elasticsearch 
import json
q = json.dumps({ "query" : { "query_string" : { "query" : "VU" }}})
q = json.dumps(
    { "query" : 
        { "regexp" : 
            { "hits.schema_name": "VU"
                # {
                #     "value": "VU",
                #     "flags": "ALL",
                #     # "case_insensitive": True,
                #     "max_determinized_states": 10000,
                #     "rewrite": "constant_score" 
                # }
            }
        }
    }
)
e = elasticsearch.Elasticsearch()
e.search(index="wikidata_en", body=q)