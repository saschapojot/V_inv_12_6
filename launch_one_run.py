import re
import subprocess
import sys

import json
argErrCode=2
if (len(sys.argv)!=2):
    print("wrong number of arguments")
    print("example: python launch_one_run.py /path/to/mc.conf")
    exit(argErrCode)




confFileName=str(sys.argv[1])
invalidValueErrCode=1
summaryErrCode=2
loadErrCode=3
confErrCode=4


#################################################
#parse conf, get jsonDataFromConf
confResult=subprocess.run(["python3", "./init_run_scripts/parseConf.py", confFileName], capture_output=True, text=True)
confJsonStr2stdout=confResult.stdout
# print(confJsonStr2stdout)
if confResult.returncode !=0:
    print("Error running parseConf.py with code "+str(confResult.returncode))
    # print(confResult.stderr)
    exit(confErrCode)
match_confJson=re.match(r"jsonDataFromConf=(.+)$",confJsonStr2stdout)
if match_confJson:
    jsonDataFromConf=json.loads(match_confJson.group(1))
else:
    print("jsonDataFromConf missing.")
    exit(confErrCode)
# print(jsonDataFromConf)

##################################################
#read summary file, get jsonFromSummary
parseSummaryResult=subprocess.run(["python3","./init_run_scripts/search_and_read_summary.py", json.dumps(jsonDataFromConf)],capture_output=True, text=True)
# print(parseSummaryResult.stdout)
if parseSummaryResult.returncode!=0:
    print("Error in parsing summary with code "+str(parseSummaryResult.returncode))
    # print(parseSummaryResult.stdout)
    # print(parseSummaryResult.stderr)
    exit(summaryErrCode)

match_summaryJson=re.match(r"jsonFromSummary=(.+)$",parseSummaryResult.stdout)
if match_summaryJson:
    jsonFromSummary=json.loads(match_summaryJson.group(1))
# print(jsonFromSummary)

##################################################

###############################################
#load previous data, to get L, y0,z0,y1,
#get loadedJsonData
loadResult=subprocess.run(["python3","./init_run_scripts/load_previous_data.py", json.dumps(jsonDataFromConf), json.dumps(jsonFromSummary)],capture_output=True, text=True)
# print(loadResult.stdout)
if loadResult.returncode!=0:
    print("Error in loading with code "+str(loadResult.returncode))
    exit(loadErrCode)

match_loadJson=re.match(r"loadedJsonData=(.+)$",loadResult.stdout)
if match_loadJson:
    loadedJsonData=json.loads(match_loadJson.group(1))
else:
    print("loadedJsonData missing.")
    exit(loadErrCode)


###############################################

###############################################
#construct parameters that are passed to mc
TStr=jsonDataFromConf["T"]
funcName=jsonDataFromConf["potential_function_name"]
loopToWrite=jsonDataFromConf["loop_to_write"]
UStr=loadedJsonData["U"]
LStr=loadedJsonData["L"]
y0Str=loadedJsonData["y0"]
z0Str=loadedJsonData["z0"]
y1Str=loadedJsonData["y1"]
loopLastFile=loadedJsonData["loopLastFile"]

initValsStr=f"{LStr},"+f"{y0Str},"+f"{z0Str},"+f"{y1Str}"

coefsStr=jsonDataFromConf["coefs"]
newFlushNum=jsonFromSummary["newFlushNum"]
TDirRoot=jsonFromSummary["TDirRoot"]
U_dist_dataDir=jsonFromSummary["U_dist_dataDir"]

params2cppInFile=[
    TStr+"\n",
    coefsStr+"\n",
    funcName+"\n",
    initValsStr+"\n",
    loopToWrite+"\n",
    newFlushNum+"\n",
    loopLastFile+"\n",
    TDirRoot+"\n",
    U_dist_dataDir+"\n"


]

cppInParamsFileName=TDirRoot+"/cppIn.txt"
with open(cppInParamsFileName,"w+") as fptr:
    fptr.writelines(params2cppInFile)