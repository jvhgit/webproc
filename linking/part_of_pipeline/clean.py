### AUTHORS ###
## Clifton Roozendal
## Floris ten Lohuis
## Jens van Holland

## Version: 1.0.0
## Date: 26-11-2021
## Course: Web Data Processing Systems

### DESCRIPTION ###
#Clean class for cleaning html text with bs4 or html2text

## packages
import html2text
from bs4 import BeautifulSoup
import multiprocessing
import pandas as pd
import re

class Clean:
    # class information
    input_ = "str:html"
    output_ = "str:clean"

    def __init__(self, option = 2) -> None:
        """
        Initialisation function\n
        Input: \n
        \t option: (int) parsing option 1: html2text (default), 2: bs4 \n
        Output: \n
        \tNone
        """

        self.option = option 
        pass

    def _parsehtml2text(self, text):
        return html2text.html2text(str(text))

    def _parsebeautifulsoup(self, text):        
        #Reads the html to text and removes certain style elements

        bs = BeautifulSoup(text, features="html.parser")

        # kill all script and style elements
        for script in bs(["script", "style"]):
            script.extract()    # remove

        # get text
        parsed = bs.get_text()

        return parsed

    def _clean(self, parsed):

        #remove meta-data about http website
        if parsed.startswith('HTTP/'):
            cleaned_text = parsed.split('\n\n',1)
            if len(cleaned_text) > 1:
                cleaned_text = cleaned_text[1]
            else:
                cleaned_text = ""
        else:
            cleaned_text = parsed

        cleaned_text = cleaned_text.replace("("," ").replace(")"," ").replace("["," ").replace("]"," ")

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in cleaned_text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        cleaned_text = '\n'.join(chunk for chunk in chunks if chunk)

        return cleaned_text


    def clean(self, text):

        if self.option == 1:    parsed_text = self._parsehtml2text(text)
        elif self.option == 2:  parsed_text = self._parsebeautifulsoup(text)
        # elif self.option == 3:
            #maybe make some custom parser with regex or some other package#
        pass

        return self._clean(parsed_text)
    
    def _forward(self, records):
        """
        Dummy function for streamlining the pipeline\n
        Input: \n
        \t text: (str) html text of a given warc file  \n
        Output: \n
        \t(mostly) cleaned text (in terms of html lingo)
        """
        # this is used by the pipeline
        # make sure this returns the acceptable output
        # it seems redudant but _forward is universal parse functions in the pipeline
        print("--> Cleaning HTML-text <--")
        with multiprocessing.Pool(records['n_threads']) as p:
                temp = p.map(self.clean, records['html_text'] )
        print("<STATUS: DONE>\n")

        if records['output_intermediates']:
            pd.DataFrame(
                {
                    "html" : temp
                }
            ).to_csv(records['output_folder'] + 'clean_results.tsv', sep='\t')

        records['text'] = temp

        return records

