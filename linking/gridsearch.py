import subprocess
import os
import sys

def GetEnv():
    #append a dir thats not on the sys path
    sys.path.append('/app/assignment/linking/part_of_pipeline')

    #convert the sys.path into env variable format
    pypath = ''
    for d in sys.path:
        pypath = pypath + d + ';'

    #create a temp copy of the env variables
    myenv = os.environ.copy()

    #set PYTHONPATH to match this scripts sys.path
    myenv['PYTHONPATH'] = pypath

    return myenv

my_env = GetEnv()

#possible options to run gridsearch over
cleanOptions = [1, 2]
extractOptions = ["en_core_web_sm","en_core_web_lg"]

for cleanOption in cleanOptions:
    for extractOption in extractOptions:
            outputFileName = "clean/" + str(cleanOption) + "|extract/" + extractOption + ".csv"
            subprocess.call(["python", "./linking/main.py"], env=my_env)#, "--clean_text="+str(cleanOption)])

