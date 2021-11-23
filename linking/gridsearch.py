import subprocess
import os
import sys

#possible options to run gridsearch over
cleanOptions = [1, 2]
extractOptions = ["en_core_web_sm","en_core_web_lg"]

for cleanOption in cleanOptions:
    for extractOption in extractOptions:
            outputFileName = "clean-" + str(cleanOption) + "|extract-" + extractOption + ".txt"
            subprocess.call(["python3", "./linking/main.py", "--clean_text", str(cleanOption), "--extract_model", extractOption])#,"--output_filename", outputFileName])

