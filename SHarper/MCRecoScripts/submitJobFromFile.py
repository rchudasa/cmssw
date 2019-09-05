#!/usr/bin/env python

import os
import optparse

parser = optparse.OptionParser(description='submits jobs to crab')

parser.add_option('--input',help='file listing the dataset')
parser.add_option('--pattern',help='pattern to match in input file')
parser.add_option('--antipattern',help='pattern not to match input file',default="ewerwefewf")
parser.add_option('--dryRun',help="if true, is a dry run, do not actually submit crab jobs",default=True)
parser.add_option('--config',help='cmsRun config file to run',default="shNtupliser_mc_basic.py")
parser.add_option('--shNtupVersion',help='shNtup version')
parser.add_option('--cmsswVersion',help='cmssw version')
parser.add_option('--copyData',help="whether to stage out the data or not",default=True)
parser.add_option('--dbsUrl',help="dbs url global,phys03 etc",default="global")
parser.add_option('--transferLogFiles',help="whether to transfer log files or not",default=False)
parser.add_option('--datasetFormat',help='dataset format')
parser.add_option('--crabDryRun',help='crab dry run',default=False)
parser.add_option('--publish',help="if true, publish the data, otherwise do not",default=False)
options,args = parser.parse_args()
if not options.input or not options.pattern or not options.shNtupVersion or not options.cmsswVersion or not options.config or not options.datasetFormat:
    parser.error("input, pattern, shNtupVersion, config, datasetFormat and cmsswVersion are manditory")
print options.config


crabProjDir='crab_projects'

datasetDefFile =open(options.input)
for line in datasetDefFile:
    if line.find(options.pattern)==-1 or line.find(options.antipattern)!=-1:
        continue

    splitLine = line.split("&")
    datasetPath = splitLine[0].rstrip(" ")
   # datasetFormat = datasetPath.split("/")[-1]
    datasetFormat = options.datasetFormat

 #   print datasetPath,nrJobs,datasetCode
    dataset=datasetPath.split("/")[1]
    datasetId = datasetPath.split("/")[2]
    datasetId = datasetId[datasetId.find("-")+1:]

    nrEvents = int(splitLine[1])
    if nrEvents!=-1:
        totalUnits = int(nrEvents/100)
    else:
        totalUnits = -1
    
    unitsPerJob = int(splitLine[6])
#    nrJobs=int(splitLine[6])
    datasetCode=int(splitLine[5])

    outputFile=dataset+"_"+datasetId+"_"+options.shNtupVersion+".root"
    outputPath="/store/user/sharper/"+options.cmsswVersion+"/"+options.shNtupVersion+"/"+datasetFormat
    publishDataname=datasetId+"_"+datasetFormat+"_"+options.shNtupVersion
    # /store/user/<dir>[/<subdirs>]/<primary-dataset>/<publication-name>/<time-stamp>/<counter>/<file-name>
    import datetime
    currTime=datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    workingDir="MC_"+dataset+"_"+options.cmsswVersion+"_"+options.shNtupVersion+"_"+datasetFormat+"_"+datasetId+"_"+currTime
    workingDirTmp="MC_"+dataset+currTime

    with open(options.config,"r") as configFile:
        configLines = configFile.readlines()
   
    tempConfig="cmssw_temp.py"
    with open(tempConfig,"w") as tempConfigFile:
        for line in configLines:
            line=line.replace("TOSED:OUTPUTFILE",outputFile)
            tempConfigFile.write(line)

  
    
    crabSubmitCmd = "crab submit -c crab_base.py --wait General.requestName="+workingDirTmp+ \
                    " General.transferOutputs="+str(options.copyData)+ \
                    " Data.inputDataset="+datasetPath+ \
                    " Data.inputDBS="+options.dbsUrl+ \
                    " Data.unitsPerJob="+str(unitsPerJob)+ \
                    " Data.totalUnits="+str(totalUnits)+ \
                    " Data.outLFNDirBase="+outputPath+ \
                    " Data.outputDatasetTag="+publishDataname+ \
                    " JobType.psetName="+tempConfig+ \
                    " General.workArea="+crabProjDir+ \
                    " Data.publication="+options.publish+\
                    " General.transferLogs="+str(options.transferLogFiles)
    if options.crabDryRun=="True":
        crabSubmitCmd=crabSubmitCmd.replace("--wait","--dryrun")
    print "will submit:"
    print crabSubmitCmd
    print " "

    if options.dryRun=="False":
        print "submitting for REAL"
        import time
        time.sleep(5)
        import os
        os.system(crabSubmitCmd)
        import shutil
        if os.path.isdir(crabProjDir+"/crab_"+workingDirTmp):
            shutil.move(crabProjDir+"/crab_"+workingDirTmp,crabProjDir+"/"+workingDir)

print "All done"
