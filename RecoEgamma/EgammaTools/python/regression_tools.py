import FWCore.ParameterSet.Config as cms

def readEleRegresFromDBFile(process,filename=None,suffix="2017UL",prod=False):
    print "reading in ele regression with tag {} from prod {}".format(suffix,prod)
    from CondCore.CondDB.CondDB_cfi import CondDB
    if filename:
        CondDBReg = CondDB.clone(connect = 'sqlite_file:{}'.format(filename))
        print "reading in ele regression with tag {} from file {}".format(suffix,filename)
    elif prod:
        CondDBReg = CondDB.clone(connect = 'frontier://FrontierProd/CMS_CONDITIONS')
        print "reading in ele regression with tag {} from production database".format(suffix)
    else:
        CondDBReg = CondDB.clone(connect = 'frontier://FrontierPrep/CMS_CONDITIONS')
        print "reading in ele regression with tag {} from prep database".format(suffix)

    process.eleRegres = cms.ESSource("PoolDBESSource",CondDBReg,
                                     DumpStat=cms.untracked.bool(False),
                                     toGet = cms.VPSet(
cms.PSet(record = cms.string("GBRDWrapperRcd"),
         label = cms.untracked.string("electron_eb_ecalOnly_1To300_0p2To2_mean"),
         tag = cms.string("electron_eb_ecalOnly_1To300_0p2To2_mean_{}".format(suffix))),
cms.PSet(record = cms.string("GBRDWrapperRcd"),
         label = cms.untracked.string("electron_ee_ecalOnly_1To300_0p2To2_mean"),
         tag = cms.string("electron_ee_ecalOnly_1To300_0p2To2_mean_{}".format(suffix))),
cms.PSet(record = cms.string("GBRDWrapperRcd"),
         label = cms.untracked.string("electron_eb_ecalOnly_1To300_0p0002To0p5_sigma"),
         tag = cms.string("electron_eb_ecalOnly_1To300_0p0002To0p5_sigma_{}".format(suffix))),
cms.PSet(record = cms.string("GBRDWrapperRcd"),
         label = cms.untracked.string("electron_ee_ecalOnly_1To300_0p0002To0p5_sigma"),
         tag = cms.string("electron_ee_ecalOnly_1To300_0p0002To0p5_sigma_{}".format(suffix))),
cms.PSet(record = cms.string("GBRDWrapperRcd"),
         label = cms.untracked.string("electron_eb_ecalTrk_1To300_0p2To2_mean"),
         tag = cms.string("electron_eb_ecalTrk_1To300_0p2To2_mean_{}".format(suffix))),
cms.PSet(record = cms.string("GBRDWrapperRcd"),
         label = cms.untracked.string("electron_ee_ecalTrk_1To300_0p2To2_mean"),
         tag = cms.string("electron_ee_ecalTrk_1To300_0p2To2_mean_{}".format(suffix))),
cms.PSet(record = cms.string("GBRDWrapperRcd"),
         label = cms.untracked.string("electron_eb_ecalTrk_1To300_0p0002To0p5_sigma"),
         tag = cms.string("electron_eb_ecalTrk_1To300_0p0002To0p5_sigma_{}".format(suffix))),
cms.PSet(record = cms.string("GBRDWrapperRcd"),
         label = cms.untracked.string("electron_ee_ecalTrk_1To300_0p0002To0p5_sigma"),
         tag = cms.string("electron_ee_ecalTrk_1To300_0p0002To0p5_sigma_{}".format(suffix))),
                                     )
    )
    
    process.es_prefer_eleRegres = cms.ESPrefer("PoolDBESSource","eleRegres")
    return process


def readPhoRegresFromDBFile(process,filename=None,suffix="2017UL",prod=False):
    from CondCore.CondDB.CondDB_cfi import CondDB
    if filename:
        CondDBReg = CondDB.clone(connect = 'sqlite_file:{}'.format(filename))
        print "reading in pho regression with tag {} from file {}".format(suffix,filename)
    elif prod:
        CondDBReg = CondDB.clone(connect = 'frontier://FrontierProd/CMS_CONDITIONS')
        print "reading in pho regression with tag {} from production database".format(suffix)
    else:
        CondDBReg = CondDB.clone(connect = 'frontier://FrontierPrep/CMS_CONDITIONS')
        print "reading in pho regression with tag {} from prep database".format(suffix)
    process.phoRegres = cms.ESSource("PoolDBESSource",CondDBReg,
                                     DumpStat=cms.untracked.bool(False),
                                     toGet = cms.VPSet(
cms.PSet(record = cms.string("GBRDWrapperRcd"),
         label = cms.untracked.string("photon_eb_ecalOnly_5To300_0p2To2_mean"),
         tag = cms.string("photon_eb_ecalOnly_5To300_0p2To2_mean_{}".format(suffix))),
cms.PSet(record = cms.string("GBRDWrapperRcd"),
         label = cms.untracked.string("photon_ee_ecalOnly_5To300_0p2To2_mean"),
         tag = cms.string("photon_ee_ecalOnly_5To300_0p2To2_mean_{}".format(suffix))),
cms.PSet(record = cms.string("GBRDWrapperRcd"),
         label = cms.untracked.string("photon_eb_ecalOnly_5To300_0p0002To0p5_sigma"),
         tag = cms.string("photon_eb_ecalOnly_5To300_0p0002To0p5_sigma_{}".format(suffix))),
cms.PSet(record = cms.string("GBRDWrapperRcd"),
         label = cms.untracked.string("photon_ee_ecalOnly_5To300_0p0002To0p5_sigma"),
         tag = cms.string("photon_ee_ecalOnly_5To300_0p0002To0p5_sigma_{}".format(suffix))),
                                     )
                                 )
    process.es_prefer_phoRegres = cms.ESPrefer("PoolDBESSource","phoRegres")
    return process

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
cms.PSet(record = cms.string("GBRDWrapperRcd"),
         label = cms.untracked.string("photon_eb_ecalOnly_1To20_0p2To2_mean"),
         tag = cms.string("photon_eb_ecalOnly_1To20_0p2To2_mean_LbyL2018")),
cms.PSet(record = cms.string("GBRDWrapperRcd"),
         label = cms.untracked.string("photon_ee_ecalOnly_1To20_0p2To2_mean"),
         tag = cms.string("photon_ee_ecalOnly_1To20_0p2To2_mean_LbyL2018")),
cms.PSet(record = cms.string("GBRDWrapperRcd"),
         label = cms.untracked.string("photon_eb_ecalOnly_1To20_0p0002To0p5_sigma"),
         tag = cms.string("photon_eb_ecalOnly_1To20_0p0002To0p5_sigma_LbyL2018")),
cms.PSet(record = cms.string("GBRDWrapperRcd"),
         label = cms.untracked.string("photon_ee_ecalOnly_1To20_0p0002To0p5_sigma"),
         tag = cms.string("photon_ee_ecalOnly_1To20_0p0002To0p5_sigma_LbyL2018")),
    ))
    
    process.es_prefer_egRegres = cms.ESPrefer("PoolDBESSource","egRegres")
    return process

