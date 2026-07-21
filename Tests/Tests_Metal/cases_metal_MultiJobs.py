#!/usr/bin/env ccp4-python


import os,os.path,sys
import glob,shutil
import time
import math

numAllJobs =0
numJobsS   =0
numJobsF   =0

doneNames = []
failNames = []

exe = "acedrg"
inRoot = "inFiles"
inListFN = os.path.join("inFiles", "metalLigands.list")
inListF  = open(inListFN, "r")
aLs        = inListF.readlines()
inListF.close()
for aL in aLs:
    cmdLine = ""
    strs = aL.strip().split()
    if len(strs) >0:
        aC=strs[0]
        aCif = os.path.join(inRoot, aC+".cif")
    if len(strs)==1:
        outRoot = "Test_%s_p"%aC
        logName = outRoot + ".log"
        cmdLine = " %s  -c %s  -o %s -p > %s"\
                  %(exe, aCif, outRoot, logName)
        print(cmdLine)
        numAllJobs += 1
    elif len(strs)==2:
        aPCode= strs[1].strip().split(".")[0]
        aPDB = os.path.join(inRoot, strs[1])
        outRoot = "Test_%s_%s_p"%(aC, aPCode) 
        logName = outRoot + ".log"
        cmdLine = " %s -c %s  -o %s --metalPDB %s -p > %s"\
                  %(exe, aCif, outRoot, aPDB, logName)
        print(cmdLine)
        numAllJobs += 1
    if len(cmdLine) >0:
        lRun=os.system(cmdLine)
        if lRun :
            print("%s runtime error "%outRoot)
            numJobsF   +=1
            failNames.append(outRoot)
        else:
            numJobsS   +=1
            doneNames.append(outRoot)
        
print("Total Number of jobs running", numAllJobs)
print("Total Number of job successfully finished", numJobsS)
if numJobsF > 0:
    print("Total Number of job failed %d. They are: "%numJobsF)
    for aName in failNames:
        print(aName)


