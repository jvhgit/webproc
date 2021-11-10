import html2text
import nltk
from bs4 import BeautifulSoup
from warcio.archiveiterator import ArchiveIterator
# import warc
import gzip
import spacy
import re
nlp = spacy.load('en_core_web_sm')

KEYNAME = "WARC-TREC-ID"


def clean_text(text):
    return html2text.html2text(str(text))


def get_entities(text):
    doc = nlp(text)
    return zip(doc.ents, [i.label_ for i in doc.ents])


def clean_entity(entity):
    entity = re.sub(r"\(/.+?\s", " ", entity)
    entity = re.sub(r"#|\*", " ", entity)
    entity = re.sub(r"\s{1,}", " ", entity)
    return entity


def main(index_file=0):
    i = 0
    text = ""
    with open('C:\\Users\\Jensv\\Vrije Universiteit Amsterdam\\wdps\\assignment1\\data\\CC-MAIN-20200918061627-20200918091627-00000.warc.gz', 'rb') as stream:
        for record in ArchiveIterator(stream):
            text = record.raw_stream.read()
            if record.rec_type == 'response':
                if i == index_file:
                    break
                i += 1
    text = clean_text(text)
    clean_tokens, labels = [], []
    for ent, label in get_entities(text):
        print(clean_entity(str(ent)))
        clean_tokens.append(clean_tokens)
        labels.append(label)


main(index_file=90)


# # The goal of this function process the webpage and returns a list of labels -> entity ID


# def find_labels(payload):
#     if payload == '':
#         return

#     # The variable payload contains the source code of a webpage and some additional meta-data.
#     # We firt retrieve the ID of the webpage, which is indicated in a line that starts with KEYNAME.
#     # The ID is contained in the variable 'key'
#     key = None
#     for line in payload.splitlines():
#         if line.startswith(KEYNAME):
#             key = line.split(': ')[1]
#             break

#     # Problem 1: The webpage is typically encoded in HTML format.
#     # We should get rid of the HTML tags and retrieve the text. How can we do it?
#     # regex or other package (BS4 or similar)

#     # Problem 2: Let's assume that we found a way to retrieve the text from a webpage. How can we recognize the
#     # entities in the text?

#     # JJ:
#     # spacy
#     # we need to make decision if we put in whole text or per sentence/paragraph
#     # should be based on computational benefit or recall measure for entities
#     doc = nlp("I'm Jens van Holland")
#     for ent in doc.ents:
#         print(ent.text, ent.label_)

#     # Problem 3: We now have to disambiguate the entities in the text. For instance, let's assugme that we identified
#     # the entity "Michael Jordan". Which entity in Wikidata is the one that is referred to in the text?

#     # To tackle this problem, you have access to two tools that can be useful. The first is a SPARQL engine (Trident)
#     # with a local copy of Wikidata. The file "test_sparql.py" shows how you can execute SPARQL queries to retrieve
#     # valuable knowledge. Please be aware that a SPARQL engine is not the best tool in case you want to lookup for
#     # some strings. For this task, you can use elasticsearch, which is also installed in the docker image.
#     # The file start_elasticsearch_server.sh will start the elasticsearch server while the file
#     # test_elasticsearch_server.py shows how you can query the engine.

#     # A simple implementation would be to first query elasticsearch to retrieve all the entities with a label
#     # that is similar to the text found in the web page. Then, you can access the SPARQL engine to retrieve valuable
#     # knowledge that can help you to disambiguate the entity. For instance, if you know that the webpage refers to persons
#     # then you can query the knowledge base to filter out all the entities that are not persons...

#     # Obviously, more sophisticated implementations that the one suggested above are more than welcome :-)

#     # For now, we are cheating. We are going to returthe labels that we stored in sample-labels-cheat.txt
#     # Instead of doing that, you should process the text to identify the entities. Your implementation should return
#     # the discovered disambiguated entities with the same format so that I can check the performance of your program.
#     cheats = dict((line.split('\t', 2) for line in open(
#         'data/sample-labels-cheat.txt').read().splitlines()))
#     for label, wikidata_id in cheats.items():
#         if key and (label in payload):
#             yield key, label, wikidata_id

# # print(len(doc.ents))
# for ent in doc.ents:
#     print(ent.text, ent.label_)
# print(record.rec_type)

# print(dir(record))
# print(record.raw_stream.read())
# print(dir(record))
# print(record.rec_headers.get_header('WARC-Target-URI'))

# print(ent)
# print(type(ent))
# print(str(ent), "---->" ,clean_entity(str(ent)))
# text[:1000]
# soepie = BeautifulSoup(text, features="html.parser")
# # soepie.get_text()
# doc = nlp(soepie.get_text())

# for ent in doc.ents:
#     print(ent.text, ent.label_)

# nltk.clean_html(text)
# def split_records(stream):
#     payload = ''
#     for line in stream:
#         if line.strip() == "WARC/1.0":
#             yield payload
#             payload = ''
#         else:
#             payload += line
#     yield payload


# def main(INPUT):
#     import sys
#     # try:
#     #     _, INPUT = sys.argv
#     # except Exception as e:
#     #     print('Usage: python starter-code.py INPUT')
#     #     sys.exit(0)

#     with gzip.open(INPUT, 'rt', errors='ignore') as fo:
#         for record in split_records(fo):
#             for key, label, wikidata_id in find_labels(record):
#                 print(key + '\t' + label + '\t' + wikidata_id)
