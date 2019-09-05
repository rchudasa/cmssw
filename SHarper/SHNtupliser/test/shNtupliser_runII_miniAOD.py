isCrabJob=False #script seds this if its a crab job
useMiniAOD=True

# Import configurations
import FWCore.ParameterSet.Config as cms
import os
import sys
# set up process
process = cms.Process("HEEP")

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(),  
#                            eventsToProcess = cms.untracked.VEventRange("281707:47701394-281707:47701394")

                            )
if isCrabJob:
    datasetCode=DATASETCODE
else:
    from SHarper.SHNtupliser.addInputFiles import addInputFiles
    addInputFiles(process.source,sys.argv[2:len(sys.argv)-1])
    from SHarper.SHNtupliser.datasetCodes import getDatasetCode
    datasetCode=getDatasetCode(process.source.fileNames[0])
    datasetCode=0

if datasetCode==0: isMC=False
else: isMC=True

datasetVersion="TOSED:DATASETVERSION"
if not isCrabJob:
    try:
        datasetVersion=sys.argv[2].split("/")[-1].split("_")[1]
    except IndexError:
        pass

print "isCrab = ",isCrabJob,"isMC = ",isMC," datasetCode = ",datasetCode," useMiniAOD = ",useMiniAOD,"datasetVersion = ",datasetVersion

# initialize MessageLogger and output report
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet(
    reportEvery = cms.untracked.int32(100000),
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
    #process.GlobalTag = GlobalTag(process.GlobalTag, '92X_upgrade2017_realistic_v10', '')
    process.GlobalTag = GlobalTag(process.GlobalTag, '92X_upgrade2017_realistic_v10', '')
else:
#    process.GlobalTag.globaltag = autoCond['run2_data']
    from SHarper.SHNtupliser.globalTags_cfi import getGlobalTagNameData
    globalTagName = getGlobalTagNameData(datasetVersion)
    process.GlobalTag = GlobalTag(process.GlobalTag, globalTagName,'')
    process.GlobalTag = GlobalTag(process.GlobalTag, '92X_dataRun2_Prompt_v9', '')

process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Geometry.CaloEventSetup.CaloTowerConstituents_cfi")
process.load("Configuration.StandardSequences.Services_cff")

# set the number of events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

#CRABHLTNAMEOVERWRITE
hltName="HLT"

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

process.shNtupliser.addGainSwitchInfo = False

process.shNtupliser.minEtToPromoteSC = 20
process.shNtupliser.fillFromGsfEle = True
process.shNtupliser.minNrSCEtPassEvent = cms.double(-1)
process.shNtupliser.outputGeom = cms.bool(False)

process.shNtupliser.hltProcName = cms.string(hltName)
process.shNtupliser.trigResultsTag = cms.InputTag("TriggerResults","",hltName)
process.shNtupliser.trigEventTag = cms.InputTag("hltTriggerSummaryAOD","",hltName)
process.shNtupliser.hbheRecHitsTag = cms.InputTag("reducedHcalRecHits","hbhereco")
process.shNtupliser.oldGsfEleTag = cms.InputTag("gedGsfElectronsReg")
disableLargeCollections=False
if disableLargeCollections:
    print "*******************************************"
    print "*******disabling large collections*********"
    print "*******************************************"
    process.shNtupliser.addPFCands = False
    process.shNtupliser.addPFClusters = False
    process.shNtupliser.addIsolTrks = False


if useMiniAOD:
    from SHarper.HEEPAnalyzer.HEEPAnalyzer_cfi import swapHEEPToMiniAOD
    swapHEEPToMiniAOD(process.shNtupliser)

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("output.root")
)
#if not isMC:
#    process.shNtupliser.oldGsfEleTag = cms.InputTag("slimmedElectronsBeforeGSFix")
#    process.shNtupliser.metTag = cms.InputTag("slimmedMETsMuEGClean")


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
    #process.skimHLTFilter.HLTPaths = cms.vstring("HLT_Ele105_CaloIdVT_GsfTrkIdT_v*","HLT_Ele115_CaloIdVT_GsfTrkIdT_v*","HLT_Ele27_WPLoose_Gsf_v*","HLT_Ele27_eta2p1_WPLoose_Gsf_v*","HLT_Ele27_WPTight_Gsf_v*","HLT_Ele27_eta2p1_WPTight_Gsf_v*","HLT_Ele32_eta2p1_WPTight_Gsf_v*","HLT_Ele35_WPLoose_Gsf_v*","HLT_Ele32_WPTight_Gsf_v*)
    process.skimHLTFilter.HLTPaths = cms.vstring("HLT_*")
elif datasetName=="SinglePhoton":
    print "setting up HLT skim for SinglePhoton"
    process.skimHLTFilter.HLTPaths =cms.vstring("HLT_Photon22_v*","HLT_Photon30_v*","HLT_Photon36_v*","HLT_Photon50_v*","HLT_Photon75_v*","HLT_Photon90_v*","HLT_Photon120_v*","HLT_Photon165_HE10_v*","HLT_Photon175_v*","HLT_Photon250_NoHE_v*","HLT_Photon300_NoHE_v*")
elif datasetName=="JetHT":
    print "setting up HLT skim for JetHT"
    process.skimHLTFilter.HLTPaths =cms.vstring("HLT_CaloJet500_NoJetID_v*",)
else:
    print "setting HLT skim to select all"
    process.skimHLTFilter.HLTPaths = cms.vstring("HLT_*")

process.skimHLTFilter.HLTPaths = cms.vstring("HLT_*")

process.egammaFilter = cms.EDFilter("EGammaFilter",
                                    nrElesRequired=cms.int32(-1),
                                    nrPhosRequired=cms.int32(-1),
                                    nrSCsRequired=cms.int32(-1),
                                    eleEtCut=cms.double(10),
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

if process.shNtupliser.datasetCode.value()>=140 and process.shNtupliser.datasetCode.value()<1000:
    print "applying filter for 1 ele and disabling large collections"
    process.egammaFilter.nrElesRequired=cms.int32(1)
    process.shNtupliser.nrGenPartToStore = cms.int32(0)
    process.shNtupliser.addPFCands = False
    process.shNtupliser.addPFClusters = False
    process.shNtupliser.addIsolTrks = False

if isCrabJob and process.shNtupliser.datasetCode.value()>140:
    process.shNtupliser.addTrigSum = cms.bool(False)

#setup the VID with HEEP 7.0, not necessary if you dont want to use VID
from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
# turn on VID producer, indicate data format  to be
# DataFormat.AOD or DataFormat.MiniAOD, as appropriate
if useMiniAOD:
    switchOnVIDElectronIdProducer(process,DataFormat.MiniAOD)
else:
    switchOnVIDElectronIdProducer(process,DataFormat.AOD)

# define which IDs we want to produce and add them to VID
my_id_modules = ['RecoEgamma.ElectronIdentification.Identification.heepElectronID_HEEPV70_cff']
for idmod in my_id_modules:
    setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)


process.load('SHarper.SHNtupliser.regressionApplicationMiniAOD_cff')

process.packedPFCandidates = cms.EDProducer("EGPackedPFCandCorrector",
                                     eles = cms.InputTag("slimmedElectrons2"),
                                     srcCands = cms.InputTag("packedPFCandidates",processName=cms.InputTag.skipCurrentProcess())
)


process.packedGenParticlesForJetsNoNu = cms.EDFilter("CandPtrSelector", 
                                                     src = cms.InputTag("packedGenParticles"), 
                                                     cut = cms.string("abs(pdgId) != 12 && abs(pdgId) != 14 && abs(pdgId) != 16")
                                                     )

## Define GenJets
from RecoJets.JetProducers.ak4GenJets_cfi import ak4GenJets
process.ak4GenJetsNoNu = ak4GenJets.clone(src = 'packedGenParticlesForJetsNoNu')
## Select charged hadron subtracted packed PF candidates (this function of fromPV works on miniaod)
process.pfCHS = cms.EDFilter("CandPtrSelector", src = cms.InputTag("packedPFCandidates"), cut = cms.string("fromPV"))
from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJets
## Define PFJetsCHS
process.ak4PFJetsCHS = ak4PFJets.clone(src = 'pfCHS', doAreaFastjet = True)
process.slimmedMETs = cms.EDProducer("PFMETProducer",
                                     src = cms.InputTag("packedPFCandidates"),
                                     alias = cms.string('pfMet'),
                                     globalThreshold = cms.double(0.0),
                                     calculateSignificance = cms.bool(False),
                                     )

process.patJetCorrFactors = cms.EDProducer("JetCorrFactorsProducer",
    emf = cms.bool(False),
    extraJPTOffset = cms.string('L1FastJet'),
    flavorType = cms.string('J'),
    levels = cms.vstring('L1FastJet', 
        'L2Relative', 
        'L3Absolute', 
        'L2L3Residual'),
    payload = cms.string('AK4PFchs'),
    primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
    rho = cms.InputTag("fixedGridRhoFastjetAll"),
    src = cms.InputTag("ak4PFJetsCHS"),
    useNPV = cms.bool(True),
    useRho = cms.bool(True)
)



process.patJets = cms.EDProducer("PATJetProducer",
    JetFlavourInfoSource = cms.InputTag(""),
    JetPartonMapSource = cms.InputTag(""),
    addAssociatedTracks = cms.bool(False),
    addBTagInfo = cms.bool(False),
    addDiscriminators = cms.bool(False),
    addEfficiencies = cms.bool(False),
    addGenJetMatch = cms.bool(False),
    addGenPartonMatch = cms.bool(False),
    addJetCharge = cms.bool(False),
    addJetCorrFactors = cms.bool(True),
    addJetFlavourInfo = cms.bool(False),
    addJetID = cms.bool(False),
    addPartonJetMatch = cms.bool(False),
    addResolutions = cms.bool(False),
    addTagInfos = cms.bool(False),
    discriminatorSources = cms.VInputTag(),
    efficiencies = cms.PSet(

    ),
    embedGenJetMatch = cms.bool(True),
    embedGenPartonMatch = cms.bool(False),
    embedPFCandidates = cms.bool(False),
    genJetMatch = cms.InputTag(""),
    genPartonMatch = cms.InputTag(""),
    getJetMCFlavour = cms.bool(False),
    jetChargeSource = cms.InputTag("patJetCharge"),
    jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetCorrFactors")),
    jetIDMap = cms.InputTag("ak4JetID"),
    jetSource = cms.InputTag("ak4PFJetsCHS"),
    partonJetSource = cms.InputTag("NOT_IMPLEMENTED"),
    resolutions = cms.PSet(

    ),
    tagInfoSources = cms.VInputTag(),
    trackAssociationSource = cms.InputTag("ak4JetTracksAssociatorAtVertexPF"),
    useLegacyJetMCFlavour = cms.bool(False),
    userData = cms.PSet(
        userCands = cms.PSet(
            src = cms.VInputTag("")
        ),
        userClasses = cms.PSet(
            src = cms.VInputTag("")
        ),
        userFloats = cms.PSet(
            src = cms.VInputTag()
        ),
        userFunctionLabels = cms.vstring(),
        userFunctions = cms.vstring(),
        userInts = cms.PSet(
            src = cms.VInputTag()
        )
    )
)


process.jetReclusterMC = cms.Sequence(process.packedGenParticlesForJetsNoNu*process.ak4GenJetsNoNu)
process.jetRecluster = cms.Sequence(process.pfCHS*process.ak4PFJetsCHS*process.patJetCorrFactors*process.patJets*process.slimmedMETs)

#process.shNtupliser.jetTag = cms.InputTag("patJets")


process.p = cms.Path(#process.primaryVertexFilter*
    process.regressionApplication*
    process.egammaFilter*
#    process.jetReclusterMC*
    process.packedPFCandidates*process.jetRecluster*

    process.egmGsfElectronIDSequence* #makes the VID value maps, only necessary if you use VID
    process.shNtupliser)
        
if not isMC:
    process.p.insert(0,process.skimHLTFilter)

if not isMC and False:
    print "overriding"
    from CondCore.DBCommon.CondDBSetup_cfi import *
    process.l1Menu = cms.ESSource("PoolDBESSource",CondDBSetup,
                                  connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS"),
                                  toGet = cms.VPSet(cms.PSet(record = cms.string("L1TGlobalPrescalesVetosRcd"),
                                                             tag = cms.string("L1TGlobalPrescalesVetos_Stage2v0_hlt")),
                                                    cms.PSet(record = cms.string("L1TUtmTriggerMenuRcd"),
                                                             tag = cms.string("L1TUtmTriggerMenu_Stage2v0_hlt"))
                                                    )                              )
    process.es_prefer_l1Menu = cms.ESPrefer("PoolDBESSource","l1Menu")

if not isCrabJob:
    import FWCore.PythonUtilities.LumiList as LumiList
#    process.source.lumisToProcess = LumiList.LumiList(filename = 'crab_projects/crab_Data_DoubleEG_8026_SHv29D_276831-277420_MINIAOD_03Feb2017-v1_20170210_133745_lumis_job69.json').getVLuminosityBlockRange()
#    process.source.lumisToProcess = LumiList.LumiList(filename = 'crab_projects/crab_Data_DoubleEG_8026_SHv29D_281207-284035_MINIAOD_03Feb2017_ver2-v1_20170212_180554_lumis_job172.json').getVLuminosityBlockRange()

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
process.output = cms.OutputModule("PoolOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(4),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string(''),
        filterName = cms.untracked.string('')
    ),
    dropMetaData = cms.untracked.string('ALL'),
    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
    fastCloning = cms.untracked.bool(False),
    fileName = cms.untracked.string('testOutput.root'),
    outputCommands = cms.untracked.vstring("keep *")
)
process.pOut = cms.EndPath(process.output)
