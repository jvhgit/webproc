# this script should run first (installs python packages from container and also updates them)
echo "Updating package manager..."
pip3 install --upgrade pip
echo "Installing Python packages and dependencies..."
# add to this line or maybe we need to make requirement file
# when we submit this assignment, it is probably better to include this in de Dockerfile
# since no development needs to be done after that.
pip3 install spacy ipykernel warcio html2text bs4
echo "Downloading NER models from Spacy..."
python3 -m spacy download en_core_web_sm 
python3 -m spacy download en_core_web_lg
echo "Done..."