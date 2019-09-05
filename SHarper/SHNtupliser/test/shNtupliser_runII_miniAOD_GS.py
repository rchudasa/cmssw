isCrabJob=False #script seds this if its a crab job
useMiniAOD=True

# Import configurations
import FWCore.ParameterSet.Config as cms

# set up process
process = cms.Process("HEEP")

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(),  

                            )
if isCrabJob:
    datasetCode=DATASETCODE
else:
    import sys
    from SHarper.SHNtupliser.addInputFiles import addInputFiles
    addInputFiles(process.source,sys.argv[2:len(sys.argv)-1])
    from SHarper.SHNtupliser.datasetCodes import getDatasetCode
    datasetCode=getDatasetCode(process.source.fileNames[0])
    datasetCode=0

if datasetCode==0: isMC=False
else: isMC=True

datasetVersion="TOSED:DATASETVERSION"

print "isCrab = ",isCrabJob,"isMC = ",isMC," datasetCode = ",datasetCode," useMiniAOD = ",useMiniAOD

# initialize MessageLogger and output report
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet(
    reportEvery = cms.untracked.int32(10000),
    limit = cms.untracked.int32(10000000)
)

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )

#Load geometry
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.autoCond import autoCond
from Configuration.AlCa.GlobalTag import GlobalTag
if isMC:
    #process.GlobalTag.globaltag = autoCond['run2_mc']
    process.GlobalTag = GlobalTag(process.GlobalTag, '80X_mcRun2_asymptotic_2016_miniAODv2_v1', '') 
else:
#    process.GlobalTag.globaltag = autoCond['run2_data']
    from SHarper.SHNtupliser.globalTags_cfi import getGlobalTagNameData
    globalTagName = getGlobalTagNameData(datasetVersion)
    process.GlobalTag = GlobalTag(process.GlobalTag, globalTagName,'')

process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Geometry.CaloEventSetup.CaloTowerConstituents_cfi")

# set the number of events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.load("Configuration.StandardSequences.Services_cff")



import sys

#CRABHLTNAMEOVERWRITE
hltName="HLT"
patCandID=""
process.load("SHarper.SHNtupliser.shNtupliser_cfi")
process.shNtupliser.datasetCode = 1
process.shNtupliser.sampleWeight = 1

process.shNtupliser.addMet = True
process.shNtupliser.addJets = True
process.shNtupliser.addMuons = False
process.shNtupliser.applyMuonId = True
process.shNtupliser.addCaloTowers = True
process.shNtupliser.addCaloHits = True
process.shNtupliser.addIsolTrks = True
process.shNtupliser.addPFCands = True
process.shNtupliser.addPFClusters = True
process.shNtupliser.addTrigSum = True

process.shNtupliser.minEtToPromoteSC = 20
process.shNtupliser.fillFromGsfEle = True
process.shNtupliser.minNrSCEtPassEvent = cms.double(-1)
process.shNtupliser.outputGeom = cms.bool(False)

process.shNtupliser.hltProcName = cms.string(hltName)
process.shNtupliser.trigResultsTag = cms.InputTag("TriggerResults","",hltName)
process.shNtupliser.trigEventTag = cms.InputTag("hltTriggerSummaryAOD","",hltName)
process.shNtupliser.hbheRecHitsTag = cms.InputTag("reducedHcalRecHits","hbhereco")

if useMiniAOD:
    from SHarper.HEEPAnalyzer.HEEPAnalyzer_cfi import swapHEEPToMiniAOD
    swapHEEPToMiniAOD(process.shNtupliser)

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("output.root")
)
#process.shNtupliser.gsfEleTag = cms.InputTag("gedGsfElectronsTrkIsoCorr")
import os


#if 1, its a crab job...
if isCrabJob:
    print "using crab specified filename"
    process.TFileService.fileName= "OUTPUTFILE"
    #process.shNtupliser.outputFilename= "OUTPUTFILE"
    process.shNtupliser.datasetCode = datasetCode
    process.shNtupliser.sampleWeight = SAMPLEWEIGHT
else:
    print "using user specified filename"
    process.TFileService.fileName= sys.argv[len(sys.argv)-1]
    #process.shNtupliser.outputFilename= sys.argv[len(sys.argv)-1]
    process.shNtupliser.datasetCode = datasetCode
    process.shNtupliser.sampleWeight = 1
  #  print "datset code ",process.shNtupliser.datasetCode

# Additional output definition
import HLTrigger.HLTfilters.hltHighLevel_cfi
process.skimHLTFilter = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
process.skimHLTFilter.throw=cms.bool(False)
datasetName="TOSED:DATASETNAME"


if datasetName=="DoubleEG":
    print "setting up HLT skim for DoubleEG"
    process.skimHLTFilter.HLTPaths = cms.vstring("HLT_DoubleEle33*","HLT_DoubleEle37*","HLT_DoublePhoton60_v*","HLT_DoublePhoton85_v*","HLT_ECALHT800_v*","HLT_Ele23_Ele12_CaloIdL_TrackIdL*")
elif datasetName=="SingleElectron":
    print "setting up HLT skim for SingleElectron"
    process.skimHLTFilter.HLTPaths = cms.vstring("HLT_Ele105_CaloIdVT_GsfTrkIdT_v*","HLT_Ele115_CaloIdVT_GsfTrkIdT_v*","HLT_Ele27_WPLoose_Gsf_v*","HLT_Ele27_eta2p1_WPLoose_Gsf_v*","HLT_Ele27_WPTight_Gsf_v*","HLT_Ele27_eta2p1_WPTight_Gsf_v*","HLT_Ele32_eta2p1_WPTight_Gsf_v*","HLT_Ele35_WPLoose_Gsf_v*")
elif datasetName=="SinglePhoton":
    print "setting up HLT skim for SinglePhoton"
    process.skimHLTFilter.HLTPaths =cms.vstring("HLT_Photon22_v*","HLT_Photon30_v*","HLT_Photon36_v*","HLT_Photon50_v*","HLT_Photon75_v*","HLT_Photon90_v*","HLT_Photon120_v*","HLT_Photon165_HE10_v*","HLT_Photon175_v*","HLT_Photon250_NoHE_v*","HLT_Photon300_NoHE_v*")
elif datasetName=="JetHT":
    print "setting up HLT skim for JetHT"
    process.skimHLTFilter.HLTPaths =cms.vstring("HLT_CaloJet500_NoJetID_v*",)
else:
    print "setting HLT skim to select all"
    process.skimHLTFilter.HLTPaths = cms.vstring("HLT_*")

process.egammaFilter = cms.EDFilter("EGammaFilter",
                                    nrElesRequired=cms.int32(-1),
                                    nrPhosRequired=cms.int32(-1),
                                    nrSCsRequired=cms.int32(-1),
                                    eleEtCut=cms.double(20),
                                    phoEtCut=cms.double(20),
                                    scEtCut=cms.double(-1),
                                    eleTag=process.shNtupliser.gsfEleTag,
                                    phoTag=process.shNtupliser.recoPhoTag,
                                    superClusEBTag = process.shNtupliser.superClusterEBTag,
                                    superClusEETag = process.shNtupliser.superClusterEETag,
                                    caloTowerTag = cms.InputTag("towerMaker"),
                                    genEvtInfoTag=cms.InputTag("generator"),
                                    requireEcalDriven=cms.bool(True)
                                     )

print "dataset code: ",process.shNtupliser.datasetCode.value()

if process.shNtupliser.datasetCode.value()>=130 and process.shNtupliser.datasetCode.value()<1000:
    print "applying filter for 1 ele and disabling large collections"
    process.egammaFilter.nrElesRequired=cms.int32(1)
    process.shNtupliser.nrGenPartToStore = cms.int32(0)
    process.shNtupliser.addPFCands = False
    process.shNtupliser.addPFClusters = False
    process.shNtupliser.addIsolTrks = False

#if process.shNtupliser.datasetCode.value() in [321,322]:
#    print "TTbar detected, disabling mc particles"
#    process.shNtupliser.addMCParts = False
    

if isCrabJob and process.shNtupliser.datasetCode.value()>131:
    process.shNtupliser.addTrigSum = cms.bool(False)

process.load("HEEP.IDCode.heepIdVarValueMapProducer_cfi")

#setup the VID with HEEP 7.0, not necessary if you dont want to use VID
from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
# turn on VID producer, indicate data format  to be
# DataFormat.AOD or DataFormat.MiniAOD, as appropriate
if useMiniAOD:
    switchOnVIDElectronIdProducer(process,DataFormat.MiniAOD)
else:
    switchOnVIDElectronIdProducer(process,DataFormat.AOD)

# define which IDs we want to produce and add them to VID
my_id_modules = ['HEEP.IDCode.heepElectronID_HEEPV70_cff']
for idmod in my_id_modules:
    setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)


process.shNtupliser.oldGsfEleTag = cms.InputTag("slimmedElectronsBeforeGSFix")
 

process.p = cms.Path(#process.primaryVertexFilter*
    process.egammaFilter*
    process.heepIDVarValueMaps*
    process.egmGsfElectronIDSequence* #makes the VID value maps, only necessary if you use VID
    process.shNtupliser)
        
if not isMC:
    process.p.insert(0,process.skimHLTFilter)

if useMiniAOD==False:
    process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
    process.load("HEEP.IDCode.packedCandidatesForTrkIso_cfi")
    process.load("PhysicsTools.PatAlgos.slimming.primaryVertexAssociation_cfi")
    process.p.insert(0,process.primaryVertexAssociation)
    process.p.insert(1,process.packedCandsForTkIso)






#import FWCore.PythonUtilities.LumiList as LumiList
#process.source.lumisToProcess = LumiList.LumiList(filename = 'notFinishedLumis.json').getVLuminosityBlockRange()

#process.AODSIMoutput = cms.OutputModule("PoolOutputModule",
#    compressionAlgorithm = cms.untracked.string('LZMA'),
#    compressionLevel = cms.untracked.int32(4),
#    dataset = cms.untracked.PSet(
#        dataTier = cms.untracked.string('AODSIM'),
#        filterName = cms.untracked.string('')
#    ),
#    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
#    fileName = cms.untracked.string('file:outputTestAOD.root'),
#    outputCommands = cms.untracked.vstring("keep *_*_*_*",)
#)                                        
#process.out = cms.EndPath(process.AODSIMoutput)
print process.GlobalTag.globaltag
