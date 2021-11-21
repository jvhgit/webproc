### AUTHORS ###
## Clifton Roozendal
## Eduard Bosch
## Floris ten Lohuis
## Jens van Holland

## Version: 1.0.0
## Date: 16-11-2021
## Course: Web Data Processing Systems

### DESCRIPTION ###
# main file, makes use of all the other components

##packages 
import argparse
from part_of_pipeline.clean import Clean
from part_of_pipeline.extract import Extract
from part_of_pipeline.search import Search
from part_of_pipeline.decision import Decision

from pipeline import Pipeline

def main():
    """
    Main function for processing the warc data\n
    Input: \n
    \tNone\n
    Output: \n
    \tNone
    """
    #config print
    print(pipeline)

    #running the pipeline
    pipeline.process(complete_path=FLAGS.data_dir)

    pass

if __name__ == '__main__':
    #arguments from command line
    parser = argparse.ArgumentParser()

    #arguments add where needed
    parser.add_argument('--data_dir', type=str, default='/app/assignment/data/sample.warc.gz',
                        help="Directory of the xxxx.warc.gz file which will be used to for the entity linking.")
    
    parser.add_argument('--clean_text', type=int, default=1,
                        help="The cleaning procedure which is used:\n\t1: html2text (default)\n\t2: BeautifulSoup:html.parser", choices=[1,2])

    parser.add_argument('--extract_model', type=str, default="en_core_web_sm",
                        help="The model which is used to extract:\n\ten_core_web_sm (default)\n\ten_core_web_lg ", choices=["en_core_web_sm","en_core_web_lg"])

    FLAGS, _ = parser.parse_known_args() #unparsed = _

    #building the pipeline
    pipeline = Pipeline()
    pipeline.add(name = "clean-text", part = Clean(option = FLAGS.clean_text))
    pipeline.add(name = "extract-entity", part = Extract(nlp_model= FLAGS.extract_model))
    pipeline.add(name = "search-entity", part = Search())
    pipeline.add(name = "disambiguate-text", part = Decision())
    print(pipeline)
    #processing the warc files
    # main()
   