isMC=True
pfNoPU=True

patCandID=""
if pfNoPU:
    patCandID="PFlow"

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

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )

# Load geometry
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
#process.GlobalTag.globaltag = cms.string('GR10_P_V5::All')
from Configuration.AlCa.autoCond import autoCond
if isMC:
    process.GlobalTag.globaltag = autoCond['startup'] 
else:
    process.GlobalTag.globaltag = autoCond['com10']

process.load("Configuration.StandardSequences.MagneticField_cff")

process.load("Geometry.CaloEventSetup.CaloTowerConstituents_cfi")

# set the number of events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.load("Configuration.StandardSequences.Services_cff")



import sys

hltName="REDIGI311X"
#do not remove this comment...
#CRABHLTNAMEOVERWRITE
hltName="HLT"
process.load("SHarper.SHNtupliser.shNtupliser_cfi")
process.shNtupliser.datasetCode = 1
process.shNtupliser.sampleWeight = 1
process.shNtupliser.gsfEleTag = "gsfElectrons"
process.shNtupliser.addMet = True
process.shNtupliser.addJets = True
process.shNtupliser.addMuons = True
process.shNtupliser.applyMuonId = True
process.shNtupliser.addCaloTowers = True
process.shNtupliser.addCaloHits = True
process.shNtupliser.addIsolTrks = True
process.shNtupliser.addPFCands = True  
process.shNtupliser.minEtToPromoteSC = 20
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
    process.shNtupliser.sampleWeight = SAMPLEWEIGHT
else:
    print "using user specified filename"
    process.TFileService.fileName= sys.argv[len(sys.argv)-1]
    #process.shNtupliser.outputFilename= sys.argv[len(sys.argv)-1]
    process.shNtupliser.datasetCode = 11000
    process.shNtupliser.sampleWeight = 1



process.egammaFilter = cms.EDFilter("EGammaFilter",
                                      nrElesRequired=cms.int32(-1),
                                      nrPhosRequired=cms.int32(-1),
                                      eleEtCut=cms.double(25),
                                      phoEtCut=cms.double(25),
                                      eleTag=process.shNtupliser.gsfEleTag,
                                      phoTag=process.shNtupliser.recoPhoTag 
                                     )

print "dataset code: ",process.shNtupliser.datasetCode.value()
if process.shNtupliser.datasetCode.value()>=160:
    if process.shNtupliser.datasetCode.value()<1000:
        print "applying filter for 1 ele and disabling large collections"
        process.egammaFilter.nrElesRequired=cms.int32(1)
        process.shNtupliser.addCaloTowers = False
        process.shNtupliser.addCaloHits = False
        process.shNtupliser.addIsolTrks = False
        process.shNtupliser.addPFCands = False


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
)
for i in range(2,len(sys.argv)-1):
    print filePrefex+sys.argv[i]
    process.source.fileNames.extend([filePrefex+sys.argv[i],])

process.load("Configuration.EventContent.EventContent_cff")
process.out = cms.OutputModule("PoolOutputModule",
    process.FEVTEventContent,
    dataset = cms.untracked.PSet(dataTier = cms.untracked.string('RECO')),
     fileName = cms.untracked.string("ihateyoupatdevelopersIreallydo.root"),
)
#process.out.outputCommands = cms.untracked.vstring('drop *','keep *_MEtoEDMConverter_*_RelValTest')
#
#outPath = cms.EndPath(out)


process.load("PhysicsTools.PatAlgos.patSequences_cff")
from RecoJets.JetProducers.kt4PFJets_cfi import *
if pfNoPU:
    # Get a list of good primary vertices, in 42x, these are DAF vertices
    from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector
    process.goodOfflinePrimaryVertices = cms.EDFilter(
        "PrimaryVertexObjectFilter",
        filterParams = pvSelector.clone( minNdof = cms.double(4.0), maxZ = cms.double(24.0) ),
        src=cms.InputTag('offlinePrimaryVertices')
        )


    # Configure PAT to use PF2PAT instead of AOD sources
    # this function will modify the PAT sequences. It is currently 
    # not possible to run PF2PAT+PAT and standart PAT at the same time
    from PhysicsTools.PatAlgos.tools.pfTools import *
    postfix = "PFlow"
    print "pf2pat running"
    usePF2PAT(process,runPF2PAT=True, jetAlgo='AK5', runOnMC=True, postfix=postfix,
              jetCorrections=('AK5PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute','L2L3Residual']),
              pvCollection=cms.InputTag('goodOfflinePrimaryVertices'),
            

              )
    
    process.pfPileUpPFlow.checkClosestZVertex = cms.bool(False)
    process.patseq = cms.Sequence(    
        process.goodOfflinePrimaryVertices*
        getattr(process,"patPF2PATSequence"+postfix)
        )

    removeSpecificPATObjects(process, ['Taus'],postfix=postfix)

else:
    removeSpecificPATObjects(process, ['Taus'])
   
    #PAT for some reason wants to re-run this
    process.kt6PFJets = kt4PFJets.clone(
        rParam = cms.double(0.6),
        doAreaFastjet = cms.bool(True),
        doRhoFastjet = cms.bool(True)
    )
    inputJetCorrLabel = ('AK5PF', ['L1Offset', 'L2Relative', 'L3Absolute'])
  
    # add pf met
    from PhysicsTools.PatAlgos.tools.metTools import *
    addPfMET(process, 'PF')

    # Add PF jets
    from PhysicsTools.PatAlgos.tools.jetTools import *
    switchJetCollection(process,cms.InputTag('ak5PFJets'),
                        doJTA        = True,
                        doBTagging   = True,
                        jetCorrLabel = inputJetCorrLabel,
                        doType1MET   = True,
                        genJetCollection=cms.InputTag("ak5GenJets"),
                        doJetID      = True,
                        btagdiscriminators=['jetBProbabilityBJetTags','jetProbabilityBJetTags','trackCountingHighPurBJetTags','trackCountingHighEffBJetTags'],
                        )
    process.patJets.addTagInfos = True
    process.patJets.tagInfoSources  = cms.VInputTag(
        cms.InputTag("secondaryVertexTagInfosAOD"),
    )
     
#process.patJetCorrFactors.levels = cms.vstring('L1Offset', 'L2Relative', 'L3Absolute', 'L2L3Residual')
process.patJetCorrFactors.levels = cms.vstring('L1Offset', 'L2Relative', 'L3Absolute')


#from PhysicsTools.PatAlgos.tools.coreTools import *
#removeSpecificPATObjects(process, ['Taus'])

from CommonTools.ParticleFlow.Tools.pfIsolation import setupPFElectronIso
process.eleIsoSequence = setupPFElectronIso(process, 'gsfElectrons')


#for isolation correction from RecoJets.JetProducers.kt4PFJets_cfi import kt4PFJets
process.kt6PFJetsForIsolation = kt4PFJets.clone( rParam = 0.6, doRhoFastjet = True )
process.kt6PFJetsForIsolation.Rho_EtaMax = cms.double(2.5)

#process.load("SHarper.HEEPAnalyzer.gsfElectronsHEEPCorrs_cfi")
#process.load("RecoEgamma.ElectronIdentification.electronIdSequence_cff")

 

if  pfNoPU:
    process.p = cms.Path(#process.primaryVertexFilter*
 #       process.gsfElectronsHEEPCorr*process.eIdSequence*
        process.egammaFilter*
        process.pfParticleSelectionSequence* process.eleIsoSequence* 
        process.patseq*
        process.kt6PFJetsForIsolation*
        process.shNtupliser)
else:
    
    process.p = cms.Path(#process.primaryVertexFilter*
        #process.gsfElectronsHEEPCorr*process.eIdSequence*
        process.egammaFilter*
        process.pfParticleSelectionSequence* process.eleIsoSequence* 
        process.patDefaultSequence*
        process.kt6PFJetsForIsolation*
        process.shNtupliser)


#from SHarper.HEEPAnalyzer.heepTools import *
#swapCollection(process,"gsfElectrons","gsfElectronsHEEPCorr")
