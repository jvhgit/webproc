First run the Dockerfile (in VSCode) + commented statements in that file. (Make sure you do not have a container running already).<br>
It is assumed that ElasticSearch+Trident is on local drive.<br>
Next run in the container (VSCode remote development advised):<br>
(in this order!)<br> 
- sh run_dependencies.sh
- sh run_server.sh
- sh run.sh <br>


In short, there are a few key components for the entity linking, namely:<br>
- The _inking/pipeline.py_ for the **Pipeline** class, which uses classes from other scripts and parses the input (WARC files) through it.
- The _inking/main.py_ for running the entity linker from command line (basically what run.sh runs).
- The _linking/part_of_pipeline/clean.py_ for the **Clean** class, this cleans the html-text.
- The _linking/part_of_pipeline/extract.py_ for the **Extract** class, this extract the entities from the "cleaned" text.
- The _linking/part_of_pipeline/search.py_ for the **Search** class, this searches for the wikilinks of the entities using ElasticSearch.

Each script can be adjusted as long the input is the same (i.e. text, list, dict, etc). 
Running time is an issue for some part - in next versions some things might change due to efficiency and parallelism.  
The output file does not fully work yet, but most of the information is there (so mostly a formatting issue).
