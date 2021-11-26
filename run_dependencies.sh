# this script should run first (installs python packages from container and also updates them)
echo "Updating package manager..."
pip3 install --upgrade pip
echo "Installing Python packages and dependencies..."
pip3 install spacy ipykernel warcio html2text bs4 numpy elasticsearch pandas asyncio elasticsearch[async] trident

# export PATH=$PATH:/home/wdps/.local/bin
# add to this line or maybe we need to make requirement file
# when we submit this assignment, it is probably better to include this in de Dockerfile
# since no development needs to be done after that.
