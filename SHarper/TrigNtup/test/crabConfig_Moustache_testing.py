from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

#config.section_('General')
config.General.requestName = 'flat_photon_lowpt_regression_moustache_sc'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

#config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'egRegTreeMakerSCNewReg.py'
#config.JobType.maxMemoryMB = 4000
config.Data.outputPrimaryDataset = 'flat_photon_lowpt_regression_moustache_sc_ntuples'
config.Data.userInputFiles = open('input_moustacheSC_v2.txt').readlines()
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
#NJOBS = 2000  # This is not a configuration parameter, but an auxiliary variable that we use in the next line.
#config.Data.totalUnits = config.Data.unitsPerJob * NJOBS

#config.section_('Data')
config.Data.outLFNDirBase = '/store/group/phys_diffraction/lbyl_2018/mc_flat_pt_photon/reco_lbl_modifier'
config.Data.allowNonValidInputDataset = True
config.Data.publication = True
config.Data.outputDatasetTag = 'flat_photon_lowpt_regression_moustache_sc'
config.Site.storageSite = 'T2_CH_CERN'
