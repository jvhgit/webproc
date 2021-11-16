import html2text
# import nltk
from bs4 import BeautifulSoup
from warcio.archiveiterator import ArchiveIterator
# import warc
import gzip
import spacy
import re
nlp = spacy.load('en_core_web_sm')

KEYNAME = "WARC-Record-ID"


def clean_text(text, option = 1):
    if option == 1:
        return html2text.html2text(str(text))
    if option == 2:
        return  BeautifulSoup(text, features="html.parser").get_text()


def get_entities(text):
    doc = nlp(text)
    #check and clean the ents
    for ent in doc.ents:
        if  
    return zip(doc.ents, [i.label_ for i in doc.ents])


def clean_entity(entity):
    entity = re.sub(r"\(/.+?\s", " ", entity)
    entity = re.sub(r"#|\*", " ", entity)
    entity = re.sub(r"\s{1,}", " ", entity)
    return entity


def split_records(stream):
    payload = ''
    for line in stream:
        if line.strip() == "WARC/1.0":
            yield payload
            payload = ''
        else:
            payload += line
    yield payload


def main(index_file=0):
    i = 0
    text = ""
    # print("OK")
    with gzip.open("/app/assignment/data/sample.warc.gz", 'rt', errors='ignore') as fo:
        for record in split_records(fo):
            # print(record)
            # print(dir(record))
            text = record
            if i ==  2: break
            i+=1
    
    # with open('/app/assignment/data/sample.warc copy.gz', 'rb') as stream:
    #     for record in ArchiveIterator(stream):
    #         text = record.raw_stream.read()
    #         # print(text)
    #         # if i == 1: break
    #         print(i)
            # i+=1
            # if record.rec_type == 'response':
            #     if i == index_file:
    #         break #do one for now
    #             # i += 1
    # print(text)
    text = clean_text(text, option=2)
    # print(text)
    text_file = open("sample.txt", "w")
    text_file.write(text)
    text_file.close()
    clean_tokens, labels = [], []
    for ent, label in get_entities(text):
        print(clean_entity(str(ent)))
        clean_tokens.append(clean_tokens)
        labels.append(label)


main()
