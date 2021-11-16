First run the Dockerfile (in VSCode) + commented statements in that file. (Make sure you do not have a container running already).<br>
It is assumed that ElasticSearch+Trident is on local drive.<br>
Next run in the container (VSCode remote development advised):<br>
(in this order!)<br> 
- sh run_dependencies.sh
- sh run_server.sh
- sh run.sh <br>
