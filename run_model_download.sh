echo "Downloading NER models from Spacy (takes a bit of time)..."
python3 -m spacy download en_core_web_sm
python3 -m spacy download en_core_web_lg
echo "Done..."