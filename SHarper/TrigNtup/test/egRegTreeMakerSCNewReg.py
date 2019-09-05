isCrabJob=False #script seds this if its a crab job

# Import configurations
import FWCore.ParameterSet.Config as cms
import os
import sys
# set up process
process = cms.Process("HEEP")

import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing ('analysis') 
options.register('isMC',True,options.multiplicity.singleton,options.varType.bool," whether we are running on MC or not")
options.parseArguments()

options.inputFiles='file:/eos/cms/store/group/phys_diffraction/lbyl_2018/mc_flat_pt_photon/reco_lbl_modifier/flatpt_photon/reco_flat_pt_photon/190715_163552/0000/step3_RAW2DIGI_L1Reco_RECO_1.root'#for testing
options.outputFile="EGReg_tree_flatpt_photon_regression_applied.root"

print options.inputFiles
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(options.inputFiles),  
                          )


# initialize MessageLogger and output report
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet(
    reportEvery = cms.untracked.int32(5000),
    limit = cms.untracked.int32(10000000)
)

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )

#Load geometry
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.autoCond import autoCond
from Configuration.AlCa.GlobalTag import GlobalTag

#gt doesnt really matter much as no reco but nice to get it right
#process.GlobalTag = GlobalTag(process.GlobalTag, '105X_mc2017_realistic_v5', '')
process.GlobalTag = GlobalTag(process.GlobalTag, '103X_upgrade2018_realistic_HI_v11', '')


process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Geometry.CaloEventSetup.CaloTowerConstituents_cfi")
process.load("Configuration.StandardSequences.Services_cff")

# set the number of events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
)


process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string(options.outputFile)
)

process.egRegTreeMaker = cms.EDAnalyzer("EGRegTreeMaker",
                                        verticesTag = cms.InputTag("offlinePrimaryVertices"),
                                        rhoTag = cms.InputTag("fixedGridRhoFastjetAll"),
                                        genPartsTag = cms.InputTag("genParticles"),
                                        puSumTag = cms.InputTag("addPileupInfo"),
                                        scTag = cms.VInputTag("particleFlowSuperClusterECAL:particleFlowSuperClusterECALBarrel","particleFlowSuperClusterECAL:particleFlowSuperClusterECALEndcapWithPreshower"),
                                        scAltTag = cms.VInputTag("particleFlowSuperClusterECALNewReg:particleFlowSuperClusterECALBarrel","particleFlowSuperClusterECALNewReg:particleFlowSuperClusterECALEndcapWithPreshower"),
                                        ecalHitsEBTag = cms.InputTag("reducedEcalRecHitsEB"),
                                        ecalHitsEETag = cms.InputTag("reducedEcalRecHitsEE"),
                                        elesTag = cms.InputTag("gedGsfElectrons"),
                                        phosTag = cms.InputTag("gedPhotons"),
                                        elesAltTag = cms.VInputTag(),
                                        phosAltTag = cms.VInputTag()
                                        )

process.particleFlowSuperClusterECALNewReg = cms.EDProducer(
    "EGSuperClusCorrector",
    colls = cms.VPSet(
        cms.PSet(
            coll = cms.InputTag("particleFlowSuperClusterECAL:particleFlowSuperClusterECALBarrel",processName=cms.InputTag.skipCurrentProcess()),
            outputLabel = cms.string("particleFlowSuperClusterECALBarrel")
        ),
        cms.PSet(
            coll = cms.InputTag("particleFlowSuperClusterECAL:particleFlowSuperClusterECALEndcapWithPreshower",processName=cms.InputTag.skipCurrentProcess()),
            outputLabel = cms.string("particleFlowSuperClusterECALEndcapWithPreshower"),
        ),
    ),
    regressionCfg = cms.PSet(
        isHLT = cms.bool(False),
        applySigmaIetaIphiBug = cms.bool(False),
        ecalRecHitsEB = cms.InputTag("reducedEcalRecHitsEB"),
        ecalRecHitsEE = cms.InputTag("reducedEcalRecHitsEE"),
        regressionKeyEB = cms.string('pfscecal_ebCorrection_offline_v2'),
        regressionKeyEE = cms.string('pfscecal_eeCorrection_offline_v2'),
        uncertaintyKeyEB = cms.string('pfscecal_ebUncertainty_offline_v2'),
        uncertaintyKeyEE = cms.string('pfscecal_eeUncertainty_offline_v2'),
        vertexCollection = cms.InputTag("offlinePrimaryVertices")
    )
)

process.p = cms.Path(process.particleFlowSuperClusterECALNewReg*process.egRegTreeMaker)


process.AODSIMoutput = cms.OutputModule("PoolOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(4),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('AODSIM'),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
    fileName = cms.untracked.string(options.outputFile.replace(".root","_EDM.root")),
    outputCommands = cms.untracked.vstring('drop *',
                                           "keep *_*_*_HEEP",
                                    )                                           
                                   )
#process.out = cms.EndPath(process.AODSIMoutput)
def readLowPtPhoRegresFromDBFile(process,filename=None,prod=False):
    from CondCore.CondDB.CondDB_cfi import CondDB
    if filename:
        CondDBReg = CondDB.clone(connect = 'sqlite_file:{}'.format(filename))
        print "reading in low pt pho regression from {}".format(filename)
    elif prod:
        CondDBReg = CondDB.clone(connect = 'frontier://FrontierProd/CMS_CONDITIONS')
        print "reading in low pt pho regression from production database"
    else:
        CondDBReg = CondDB.clone(connect = 'frontier://FrontierPrep/CMS_CONDITIONS')
        print "reading in low pt pho regression from prep database"

    process.egRegres = cms.ESSource("PoolDBESSource",CondDBReg,
                                     DumpStat=cms.untracked.bool(False),
                                     toGet = cms.VPSet(
cms.PSet(record = cms.string("GBRDWrapperRcd"),
         label = cms.untracked.string("pfscecal_ebCorrection_offline_v2"),
         tag = cms.string("pfscecal_ebCorrection_offline_v2_LbyL2018")),
cms.PSet(record = cms.string("GBRDWrapperRcd"),
         label = cms.untracked.string("pfscecal_eeCorrection_offline_v2"),
         tag = cms.string("pfscecal_eeCorrection_offline_v2_LbyL2018")),
cms.PSet(record = cms.string("GBRDWrapperRcd"),
         label = cms.untracked.string("pfscecal_ebUncertainty_offline_v2"),
         tag = cms.string("pfscecal_ebUncertainty_offline_v2_LbyL2018")),
cms.PSet(record = cms.string("GBRDWrapperRcd"),
         label = cms.untracked.string("pfscecal_eeUncertainty_offline_v2"),
         tag = cms.string("pfscecal_eeUncertainty_offline_v2_LbyL2018")),
    ))

    process.es_prefer_egRegres = cms.ESPrefer("PoolDBESSource","egRegres")
    return process
readLowPtPhoRegresFromDBFile(process,prod=False)

'''
def readSCRegresFromDBFile(process,filename=None,suffex="2017UL"):
    from CondCore.CondDB.CondDB_cfi import CondDB
    if filename:
        CondDBReg = CondDB.clone(connect = 'sqlite_file:{}'.format(filename))
    else:
        CondDBReg = CondDB.clone(connect = 'frontier://FrontierProd/CMS_CONDITIONS')
    process.scRegres = cms.ESSource("PoolDBESSource",CondDBReg,
                                     DumpStat=cms.untracked.bool(False),
                                     toGet = cms.VPSet(
cms.PSet(record = cms.string("GBRDWrapperRcd"),
         label = cms.untracked.string("pfscecal_EBCorrection_offline_v2"),
         tag = cms.string("pfscecal_EBCorrection_offline_v2_{}".format(suffex))),
cms.PSet(record = cms.string("GBRDWrapperRcd"),
         label = cms.untracked.string("pfscecal_EECorrection_offline_v2"),
         tag = cms.string("pfscecal_EECorrection_offline_v2_{}".format(suffex))),
cms.PSet(record = cms.string("GBRDWrapperRcd"),
         label = cms.untracked.string("pfscecal_EBUncertainty_offline_v2"),
         tag = cms.string("pfscecal_EBUncertainty_offline_v2_{}".format(suffex))),
cms.PSet(record = cms.string("GBRDWrapperRcd"),
         label = cms.untracked.string("pfscecal_EEUncertainty_offline_v2"),
         tag = cms.string("pfscecal_EEUncertainty_offline_v2_{}".format(suffex))),
))
    process.es_prefer_scRegres = cms.ESPrefer("PoolDBESSource","scRegres")
    return process
readSCRegresFromDBFile(process,suffex="2018UL")
'''


print process.GlobalTag.globaltag
