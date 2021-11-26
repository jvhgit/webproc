#1) build container with this file (vscode rightclick on file -> build image), we assume that the parent folder is called  "webproc"
FROM karmaresearch/wdps_assignment

#Python packages
RUN pip3 install --no-cache-dir --upgrade pip
RUN pip3 install --no-cache-dir spacy ipykernel warcio html2text bs4 numpy pandas elasticsearch elasticsearch[async]

#NER models
RUN python3 -m spacy download en_core_web_sm
# RUN python3 -m spacy download en_core_web_lg

#2) Run the container and add volume (run below in powershell) (example below)
# we assume that elasticsearch and trident are local
# docker run -ti -v C:/Users/Jensv/git/webproc:/app/assignment -p 9200:9200 webproc

#3) Run following command in linux container shell to start elasticsearch server (takes a minute or 2)
# ./assets/elasticsearch-7.9.2/bin/elasticsearch -d
# you can verify the start by going to https://localhost:9200/

#4) To run the entity linker, to the following:
# python3 linking/main.py
# this runs with all the default arguments
# for more information on the commandline arguments see: linking/main.py


### ignore below ###
#run line below first before other
# RUN docker run -ti --privileged centos sysctl vm.max_map_count=262144 
# RUN docker run -ti --karmaresearch/wdps_assignment vm.max_map_count=262144 
# RUN docker run -ti -v D:/University/Web Data Processing Systems/Data/assignment-all-splitted/assignment-all-splitted/assignment -p 9200:9200 karmaresearch/wdps_assignment
# RUN docker run -ti --privileged webproc sysctl -w vm.max_map_count=262144
# RUN docker run -ti -v D:/University/Web Data Processing Systems/Data/assignment-all-splitted/assignment-all-splitted/assignment -p 9200:9200 webproc
# export PATH=/home/wdps/.local/bin$PATH


# https://stackoverflow.com/questions/51445846/elasticsearch-max-virtual-memory-areas-vm-max-map-count-65530-is-too-low-inc