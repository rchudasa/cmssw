#!/usr/bin/env bash

#nrEventsPerJob=10000 #dont think this does anything

datasetFile=$1
datasetPattern=$2
live=$3
datasetAntiPattern=$4
tag=$5
#for entry in `grep $dataset $datasetFile | awk -F "&" '{print $1}'`
for entry in `grep $datasetPattern $datasetFile | grep -v $datasetAntiPattern | sed 's| ||g'`
do
#line=`grep $e`ntry $datasetFile`
line=$entry

datasetPath=`echo $line | awk -F "&" '{print $1}'`
dataset=`echo $datasetPath | awk -F "/" '{print $2}'`
nrEvents=`echo $line | awk -F "&" '{print $2}'`
dataFormat=`echo $datasetPath | awk -F "/" '{print $NF}'`

weight=`echo $line | awk -F "&" '{print $4*$5}'`
cmsswVersion=`echo $datasetPath | awk -F "/" '{print $3}' | awk -F "-" '{print $2"-"$3}'`
outputFile=${dataset}_${cmsswVersion}_HLT.root


#the output directory /pnfs/pp.rl.ac.uk/data/cms/store/user/harper/$outputPath

outputPath=720/MuEGCor/${dataset}/${cmsswVersion}/${tag}/
#outputPath=612SLHC2/SHL1v1/NoTowerThres/${cmsswVersion}/${dataset}/
#the output directory /pnfs/pp.rl.ac.uk/data/cms/store/user/harper/$outputPath


#baseCfg="shNtupliser_mc.py"
baseCfg="runHLT.py"
#baseCfg="runSHNtupliser_base.cfg"

#nrJobs=`echo $nrEvents/$nrEventsPerJob + 1 | bc`
nrJobs=`echo $line | awk -F "&" '{print $7}'`
datasetCode=`echo $line | awk -F "&" '{print $6}'`

#echo out: $outputPath  
#echo sub: $subDirs


subDirs=`echo $outputPath | awk -F "/" '{for(i=1;i<NF-1;i++) printf("%s/",$i);print $(NF-1)}' | sed 's|/|_|g'` 
workingDir=`echo $datasetPath | awk -F "/" '{print "crabJob_MC_"$2}' `.${subDirs}.`date +%y%m%d`_`date +%H%M%S`
#workingDir=`echo $datasetPath | awk -F "/" '{print "crabJob_MC_"$2}' `.`date +%y%m%d`_`date +%H%M%S`

 echo sub: $subDirs
if [[ "$live" == "ON" ]] ; then
echo about to submit for real ./submitCrabJob.sh $datasetPath $nrEvents $nrJobs $outputFile $outputPath $datasetCode $weight $baseCfg $workinDir
sleep 5s
./submitCrabJob.sh $datasetPath $nrEvents $nrJobs $outputFile $outputPath $datasetCode $weight  $baseCfg $workingDir
#sleep 30m
else
echo ./submitCrabJob.sh $datasetPath $nrEvents $nrJobs $outputFile $outputPath $datasetCode $weight $baseCfg $workingDir


fi

done
