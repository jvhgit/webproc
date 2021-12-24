### AUTHORS ###
# Clifton Roozendal
# Floris ten Lohuis
# Jens van Holland

## Version: 2.0.0
## Date: 24-12-2021
# Course: Web Data Processing Systems

### DESCRIPTION ###
# main file, makes use of all the other components

# packages
import gc
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
    # print arguments
    print("--- Arguments ---")
    print(FLAGS)
    # config print
    print(pipeline)

    # running the pipeline
    pipeline.process(FLAGS)

    pass


if __name__ == '__main__':
    # arguments from command line
    parser = argparse.ArgumentParser()

    # arguments add where needed
    parser.add_argument('--data_dir', type=str, default='/app/assignment/data/sample.warc.gz',
                        help="Directory of the xxxx.warc.gz file which will be used to for the entity linking.")

    parser.add_argument('--clean_text', type=int, default=1,
                        help="The cleaning procedure which is used:\n\t1: BeautifulSoup:html.parser (default) \n\t2: html2text", choices=[1, 2])

    parser.add_argument('--extract_model', type=str, default="en_core_web_sm",
                        help="The model which is used to extract:\n\ten_core_web_sm (default)\n\ten_core_web_lg ", choices=["en_core_web_sm", "en_core_web_lg"])

    parser.add_argument('--extract_multithreaded', type=bool, default=False,
                        help="Should extract be run multithreaded (multi-threaded not much faster than using NER pipeline)")

    parser.add_argument('--query_size_ES', type=int, default=20,
                        help="The max number of hits a query can return.")

    parser.add_argument('--search_ES', type=str, default="normal",
                        help="Please do not alter this - the 'fast' implementation is very buggy.", choices=['normal', 'fast'])

    parser.add_argument('--batch_size_NER', type=int, default=8,
                        help="The NER model parses n samples in parallel.\nWe found 8 to be the best value (on 8 threads, intel i7, 16gb RAM)")

    parser.add_argument('--n_threads', type=int, default=4,
                        help="The number of threads to use.\nPlease be carefull - do not set to -1, this will go wrong(!). ")

    parser.add_argument('--sim_cutoff_NER', type=float, default=0.75,
                        help="To reduce the number of queries = entities, we compute similarity.cross-referencing scores and use a threshold (first one is kept). ")

    parser.add_argument('--n_hits_EL', type=int, default=3,
                        help="Does nothing (NOT IMPLEMENTED)")

    parser.add_argument('--output_intermediates', type=bool, default=True,
                        help="Indicates whether intermediates should be output")
    
    parser.add_argument('--output_folder', type=str, default="/app/assignment/results/",
                        help="Indicates whether intermediates should be output")

    parser.add_argument('--save_to', type=str, default="results.txt",
                        help="File name where the output should be written to.")

    FLAGS, _ = parser.parse_known_args()  # unparsed = _

    # building the pipeline
    pipeline = Pipeline()
    pipeline.add(name="clean-text", part=Clean(option=FLAGS.clean_text))
    pipeline.add(name="extract-entity",
                 part=Extract(nlp_model=FLAGS.extract_model,sim_cutoff_NER=FLAGS.sim_cutoff_NER))
    pipeline.add(name="search-entity", part=Search())
    pipeline.add(name="disambiguate-text", part=Decision())

    # processing the warc files
    gc.collect()
    main()
