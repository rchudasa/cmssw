isMC=False

# Import configurations
import FWCore.ParameterSet.Config as cms

# set up process
process = cms.Process("HEEP")

# initialize MessageLogger and output report
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet(
    reportEvery = cms.untracked.int32(500),
    limit = cms.untracked.int32(10000000)
)
process.MessageLogger.suppressWarning.extend(["muonDTDigis"],)

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )

# Load geometry
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

from Configuration.AlCa.autoCond import autoCond
if isMC:
    # process.GlobalTag.globaltag = autoCond['startup']
    process.GlobalTag.globaltag = 'POSTLS161_V12::All'
else:
    #process.GlobalTag.globaltag = autoCond['com10']
    process.GlobalTag.globaltag = 'POSTLS161_V12::All'


# set the number of events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(500)
)



import sys

hltName="HLT"
#do not remove this comment...
#CRABHLTNAMEOVERWRITE


from SHarper.HEEPAnalyzer.HEEPEventParameters_cfi import *
from SHarper.SHNtupliser.shNtupliserParameters_cfi import *


process.shNtupliser = cms.EDAnalyzer("SHL1Ntupliser", heepEventPara,shNtupPara,
                                     l1CaloClustersTag = cms.InputTag("L1CaloClusterEGIsolator"),
                                     l1CaloTowersTag = cms.InputTag("L1CaloTowerProducer")
   
)


process.shNtupliser.datasetCode = 1
process.shNtupliser.sampleWeight = 1
process.shNtupliser.gsfEleTag = "gsfElectrons"
process.shNtupliser.addMet = True
process.shNtupliser.addJets = False
process.shNtupliser.addMuons = False
process.shNtupliser.applyMuonId = False
process.shNtupliser.addCaloTowers = True
process.shNtupliser.addCaloHits = False
process.shNtupliser.addIsolTrks = False
process.shNtupliser.addPFCands = False
process.shNtupliser.minEtToPromoteSC = 0
process.shNtupliser.fillFromGsfEle = True
process.shNtupliser.minNrSCEtPassEvent = cms.double(-1)
process.shNtupliser.outputGeom = cms.bool(False)
process.shNtupliser.useHLTDebug = cms.bool(False)
process.shNtupliser.hltProcName = hltName
process.shNtupliser.trigResultsTag = cms.InputTag("TriggerResults","",hltName)
process.shNtupliser.trigEventTag = cms.InputTag("hltTriggerSummaryAOD","",hltName)
process.shNtupliser.compTwoMenus = cms.bool(False)
process.shNtupliser.secondHLTTag = cms.string("")
process.shNtupliser.electronTag = cms.untracked.InputTag("patElectrons"+patCandID)
process.shNtupliser.tauTag = cms.untracked.InputTag("patTaus"+patCandID)
process.shNtupliser.muonTag = cms.untracked.InputTag("patMuons"+patCandID)
process.shNtupliser.jetTag = cms.untracked.InputTag("patJets"+patCandID)
process.shNtupliser.photonTag = cms.untracked.InputTag("patPhotons"+patCandID)
process.shNtupliser.metTag = cms.untracked.InputTag("patMETs"+patCandID)
process.shNtupliser.hbheRecHitsTag = cms.InputTag("reducedHcalRecHits","hbhereco")

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("output.root")
)


isCrabJob=False #script seds this if its a crab job

#if 1, its a crab job...
if isCrabJob:
    print "using crab specified filename"
    process.TFileService.fileName= "OUTPUTFILE"
    #process.shNtupliser.outputFilename= "OUTPUTFILE"
    process.shNtupliser.datasetCode = DATASETCODE
    process.shNtupliser.sampleWeight = 1
else:
    print "using user specified filename"
    process.TFileService.fileName= sys.argv[len(sys.argv)-1]
    #process.shNtupliser.outputFilename= sys.argv[len(sys.argv)-1]
    process.shNtupliser.datasetCode = 1
    process.shNtupliser.sampleWeight = 1





filePrefex="file:"
if(sys.argv[2].find("/pnfs/")==0):
    filePrefex="dcap://heplnx209.pp.rl.ac.uk:22125"

if(sys.argv[2].find("/store/")==0):
    filePrefex=""
if(sys.argv[2].find("/eos/")==0):
    filePrefex="'root://eoscms/"



process.source = cms.Source("PoolSource",
                 #         fileNames = cms.untracked.vstring(filePrefex+sys.argv[2]),
                       #     inputCommands = cms.untracked.vstring("drop *","keep *_source_*_*"),
                            fileNames = cms.untracked.vstring(),
                            skipEvents = cms.untracked.uint32(0)
)
for i in range(2,len(sys.argv)-1):
    print filePrefex+sys.argv[i]
    process.source.fileNames.extend([filePrefex+sys.argv[i],])

#for isolation correction
#from RecoJets.JetProducers.kt4PFJets_cfi import kt4PFJets
#process.kt6PFJetsForIsolation = kt4PFJets.clone( rParam = 0.6, doRhoFastjet = True )
#process.kt6PFJetsForIsolation.Rho_EtaMax = cms.double(2.5)


process.load('SLHCUpgradeSimulations.L1CaloTrigger.SLHCCaloTrigger_cff')
process.L1CaloTriggerSetup.InputXMLFile = cms.FileInPath('SLHCUpgradeSimulations/L1CaloTrigger/data/setupHFNoTowerThres.xml')


# Additional output definition
import HLTrigger.HLTfilters.hltHighLevel_cfi
process.skimHLTFilter = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
#print "MinimumBias dataset, requiring ZeroBias trigger"
#process.skimHLTFilter.HLTPaths = cms.vstring("HLT_ZeroBias_v*")

#print "SingleMu, MU40"
#process.skimHLTFilter.HLTPaths = cms.vstring("HLT_Mu40_v*")


process.p = cms.Path(#process.skimHLTFilter*
                     process.RawToDigi*process.SLHCCaloTrigger*

                     process.shNtupliser)


#from SHarper.HEEPAnalyzer.heepTools import *
#swapCollection(process,"gsfElectrons","gsfElectronsHEEPCorr")
process.L1CaloClusterEGFilter = cms.EDProducer("L1CaloClusterFilter",
    src = cms.InputTag("L1CaloClusterProducer"),
    etMode = cms.int32(1)
)
process.L1CaloClusterEGIsolator = cms.EDProducer("L1CaloClusterEGIsolator",
                                                  caloClustersTag = cms.InputTag("L1CaloClusterFilter"),
                                                  caloTowersTag = cms.InputTag("L1CaloTowerProducer"),
                                                  rhoTag = cms.InputTag("L1RhoProducer"),
                                                  maxTowerIEta=cms.int32(27), #HF is 29 and up
                                                  isolEtCut=cms.int32(-1) # isolEt<=-6 
                                                  )
process.L1EGIsolRho = cms.EDProducer("L1EGIsolRhoProducer",
                                     caloTowersTag = cms.InputTag("L1CaloTowerProducer"),
                                     towerEtThreshold = cms.int32(7) # in GeV
                                    )



process.rawSLHCL1ExtraParticles.EGClusters = cms.InputTag("L1CaloClusterEGIsolator")

process.SLHCCaloTrigger.insert(process.SLHCCaloTrigger.index(process.rawSLHCL1ExtraParticles),process.L1CaloClusterEGFilter)
process.SLHCCaloTrigger.insert(process.SLHCCaloTrigger.index(process.rawSLHCL1ExtraParticles),process.L1CaloClusterEGIsolator)
process.SLHCCaloTrigger.insert(process.SLHCCaloTrigger.index(process.rawSLHCL1ExtraParticles),process.L1CaloJetExpander)




if isMC:
    print "Going to run on MC"

    # adopt to MC
    process.p.remove(process.RawToDigi)
    process.load('Configuration.StandardSequences.RawToDigi_cff')
    process.p.insert(0, process.RawToDigi)

    # bug fix for missing HCAL TPs in MC RAW
    process.p.insert(1, process.valHcalTriggerPrimitiveDigis)
    from SimCalorimetry.HcalTrigPrimProducers.hcaltpdigi_cff import HcalTPGCoderULUT
    HcalTPGCoderULUT.LUTGenerationMode = cms.bool(True)
    process.valRctDigis.hcalDigis             = cms.VInputTag(cms.InputTag('valHcalTriggerPrimitiveDigis'))
    process.L1CaloTowerProducer.HCALDigis =  cms.InputTag("valHcalTriggerPrimitiveDigis")

    


#import PhysicsTools.PythonAnalysis.LumiList as LumiList
#process.source.lumisToProcess = LumiList.LumiList(filename = 'UserCode/L1TriggerUpgrade/test/2012HPF_json_66.txt').getVLuminosityBlockRange()
print process.GlobalTag.globaltag
