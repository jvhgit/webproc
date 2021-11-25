#get image
FROM karmaresearch/wdps_assignment
# USER root

RUN pip3 install --no-cache-dir --upgrade pip
    pip3 install --no-cache-dir spacy ipykernel warcio html2text bs4 numpy pandas elasticsearch elasticsearch[async]

RUN python3 -m spacy download en_core_web_sm
RUN python3 -m spacy download en_core_web_lg
# sudo apt-get install wget
#password: wdps
#  pip3 install -e git@github.com:facebookresearch/BLINK.git 
#run line below first before other
# RUN docker run -ti --privileged centos sysctl vm.max_map_count=262144 
# RUN docker run -ti --karmaresearch/wdps_assignment vm.max_map_count=262144 
# RUN docker run -ti -v D:/University/Web Data Processing Systems/Data/assignment-all-splitted/assignment-all-splitted/assignment -p 9200:9200 karmaresearch/wdps_assignment
# RUN docker run -ti --privileged webproc sysctl -w vm.max_map_count=262144
# RUN docker run -ti -v D:/University/Web Data Processing Systems/Data/assignment-all-splitted/assignment-all-splitted/assignment -p 9200:9200 webproc
# export PATH=/home/wdps/.local/bin$PATH
# https://stackoverflow.com/questions/51445846/elasticsearch-max-virtual-memory-areas-vm-max-map-count-65530-is-too-low-inc