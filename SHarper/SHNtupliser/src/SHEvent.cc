#include "SHarper/SHNtupliser/interface/SHEvent.hh"

#include "SHarper/SHNtupliser/interface/TempFuncs.hh"

#include <iomanip>
//note there also exists a SHEvent_CMSSW.cc and SHEvent_standard.cc which define the CMSSW specific functions


ClassImp(SHEvent)

SHEvent::SHEvent():
  superClusArray_("SHSuperCluster",4),
  electronArray_("SHElectron",12),
  mcPartArray_("SHMCParticle",30),
  jetArray_("SHJet",10),
  caloHits_(),
  // isolSuperClusArray_("SHIsolSuperCluster",5),
  // isolClusArray_("SHIsolCluster",20),
  isolTrkArray_("SHIsolTrack",20),
  trigArray_("SHTrigInfo",20),
  muArray_("SHMuon",12),
  preShowerClusArray_("SHPreShowerCluster",20),
  runnr_(0),eventnr_(0),
  isMC_(0),datasetCode_(0),
  weight_(0.),
  metData_(),
  l1Bits_(0x0),
  // l1CandArray_("SHL1Cand",20),
  lumiSec_(0),
  bx_(0),
  orbNr_(0),
  time_(0),
  nrVertices_(-1),
  vertex_(-999,-999,-999),
  beamSpot_(-999,-999,-999),
  preScaleCol_(-1), 
  eleRhoCorr_(-999.),
  vertexArray_("SHVertex",70),
  rhoCorr_(-999.),
  flags_(0),
  caloTowers_()

{
 
}
void SHEvent::copyEventPara(const SHEvent& rhs)
{
  runnr_=rhs.runnr_;
  eventnr_=rhs.eventnr_;
  isMC_=rhs.isMC_;
  datasetCode_=rhs.datasetCode_;
  weight_=rhs.weight_;
  metData_=rhs.metData_;
  genEventPtHat_ = rhs.genEventPtHat_; 
  l1Bits_ =rhs.l1Bits_;
  lumiSec_ =rhs.lumiSec_;
  bx_ =rhs.bx_;
  orbNr_ = rhs.orbNr_;
  time_ = rhs.time_;
  nrVertices_ = rhs.nrVertices_;
  vertex_ = rhs.vertex_;
  beamSpot_ = rhs.beamSpot_;
  pfMet_ = rhs.pfMet_;
  preScaleCol_ =rhs.preScaleCol_;  
  eleRhoCorr_ = rhs.eleRhoCorr_;
  rhoCorr_=rhs.rhoCorr_;
  flags_=rhs.flags_;
  puSum_=rhs.puSum_;
  // puSummary_ =rhs.puSummary_;
}

//I have a memory leak from some where....
void SHEvent::clear()
{
  superClusArray_.Delete();
  electronArray_.Delete();
  mcPartArray_.Delete();
  jetArray_.Delete();
  // isolSuperClusArray_.Delete();
  //isolClusArray_.Delete();
  isolTrkArray_.Delete();
  trigArray_.Delete();
  muArray_.Delete();
  preShowerClusArray_.Delete();
  caloHits_.clear();
  runnr_=0;
  eventnr_=0;
  isMC_=0;
  datasetCode_=0;
  weight_=0.;  
  lumiSec_=0;
  bx_=0;
  orbNr_=0;
  time_=0;
  metData_.clear(); 
  //l1CandArray_.Delete();
  l1Bits_.ResetAllBits();
  nrVertices_=-1;
  vertex_.SetXYZ(-999,-999,-999); 
  beamSpot_.SetXYZ(-999,-999,-999);
  preScaleCol_=-1;
  eleRhoCorr_ = -999.;
  vertexArray_.Delete();
  rhoCorr_ = -999.;
  flags_=0;
  caloTowers_.clear();
  genInfo_.clear();
  puSum_.clear();
  pfCands_.clear();
  pfClusters_.clear();
  recHitClusMap_.clear();
  jetMETExtra_.clear();
}
SHEvent::~SHEvent()
{
  superClusArray_.Delete();
  electronArray_.Delete();
  mcPartArray_.Delete();
  jetArray_.Delete();
  //isolSuperClusArray_.Delete();
  //isolClusArray_.Delete();
  isolTrkArray_.Delete();
  trigArray_.Delete();
  //l1CandArray_.Delete();
  muArray_.Delete();
  preShowerClusArray_.Delete();
  vertexArray_.Delete();
}

void SHEvent::addMCParticle(int partIndx,int partStdhep,int partIdhep,
			    int partJmo1,int partJmo2,int partNrMo,
			    int partJda1,int partJda2,int partNrDa,
			    const TLorentzVector& p4,const TVector3& pos)
{
  if(partIndx!=nrMCParticles()) std::cout <<"SHEvent::addMCParticle : Error particle should be at index "<<partIndx<<" but will be added in index "<<nrMCParticles()<<std::endl;
  new(mcPartArray_[nrMCParticles()]) SHMCParticle(partIndx,partStdhep,partIdhep,
						  partJmo1,partJmo2,partNrMo,
						  partJda1,partJda2,partNrDa,p4,pos);
}

void SHEvent::addMCParticle(const SHMCParticle& mcPart)
{
  if(mcPart.index()!=nrMCParticles()) std::cout <<"SHEvent::addMCParticle : Error particle should be at index "<<mcPart.index()<<" but will be added in index "<<nrMCParticles()<<std::endl;
  new(mcPartArray_[nrMCParticles()]) SHMCParticle(mcPart);
}

void SHEvent::addJet(const SHJet& jet)
{
  new(jetArray_[nrJets()]) SHJet(jet);
}
void SHEvent::addMuon(const SHMuon& mu)
{
  new(muArray_[nrMuons()]) SHMuon(mu);
}

void SHEvent::addPreShowerCluster(const SHPreShowerCluster& clus)
{
  new(preShowerClusArray_[nrPreShowerClus()]) SHPreShowerCluster(clus);
}

void SHEvent::addElectron(const SHElectron& ele,const SHSuperCluster& superClus)
{
  int superClusIndx = getSuperClusIndx(superClus.rawNrgy(),superClus.eta(),superClus.phi());
  if(superClusIndx==-1){ //super clus has not been added already so add it
    superClusIndx = nrSuperClus();
    new(superClusArray_[superClusIndx]) SHSuperCluster(superClus);
  }  
  new(electronArray_[nrElectrons()]) SHElectron(ele);
  getElectron(nrElectrons()-1)->setSuperClusIndex(superClusIndx); //-1 as it counts from zero
  getElectron(nrElectrons()-1)->setMotherEvent(this);
}

void SHEvent::addElectron(const SHElectron& ele)
{
  int superClusIndx=-1;//as no supercluster is assoicated
  new(electronArray_[nrElectrons()]) SHElectron(ele);
  getElectron(nrElectrons()-1)->setSuperClusIndex(superClusIndx);
  getElectron(nrElectrons()-1)->setMotherEvent(this);
}

void SHEvent::addIsolInfo(const SHEvent& rhs)
{
  //TempFuncs::copyTClonesArray<SHIsolSuperCluster>(isolSuperClusArray_,rhs.isolSuperClusArray_);
  //TempFuncs::copyTClonesArray<SHIsolCluster>(isolClusArray_,rhs.isolClusArray_);
  TempFuncs::copyTClonesArray<SHIsolTrack>(isolTrkArray_,rhs.isolTrkArray_);
}

void SHEvent::addCaloHits(const SHEvent& rhs)
{
  caloHits_ = rhs.caloHits_;
}
void SHEvent::addCaloTowers(const SHEvent& rhs)
{
  caloTowers_ = rhs.caloTowers_;
}

void SHEvent::addIsolTrk(const SHIsolTrack& trk)
{
  new(isolTrkArray_[nrIsolTrks()]) SHIsolTrack(trk);
  
}

// void SHEvent::addIsolTrk(const TVector3& p3,const TVector3& vtxPos,bool posCharge,int vertexNr,float chi2,int ndof,int algosAndQual)
// {
//   new(isolTrkArray_[nrIsolTrks()]) SHIsolTrack(p3,vtxPos,posCharge,vertexNr,chi2,ndof,algosAndQual);
  
// }

void SHEvent::addTrigInfo(const SHTrigInfo& trigInfo)
{
  new(trigArray_[nrTrigs()]) SHTrigInfo(trigInfo);
  
}

// void SHEvent::addL1Cand(const SHL1Cand& l1Cand)
// {
//   new(l1CandArray_[nrL1Cands()]) SHL1Cand(l1Cand);
  
// }
// void SHEvent::addL1Cand(const TLorentzVector& p4,int type)
// {
//   new(l1CandArray_[nrL1Cands()]) SHL1Cand(p4,type);
  
// }
//we only store hits which actually have information
void SHEvent::addEcalHits(const std::vector<SHCaloHit> & hitVec)
{
  for(size_t hitNr=0;hitNr<hitVec.size();hitNr++){
    if(hitVec[hitNr].nrgy()>=-100){
      caloHits_.addHit(hitVec[hitNr]);
    }
  }
}

//we only store hits which actually have information
void SHEvent::addHcalHits(const std::vector<SHCaloHit> & hitVec)
{
  for(size_t hitNr=0;hitNr<hitVec.size();hitNr++){
    if(hitVec[hitNr].nrgy()>=-100){
      caloHits_.addHit(hitVec[hitNr]);
    }
  }
} 

int SHEvent::nrGoodVertices()const
{
  int nrGoodVtxs = 0;
  for(int vtxNr=0;vtxNr<nrVertices();vtxNr++){
    if(getVertex(vtxNr)->isGood()) nrGoodVtxs++;
  }
  return nrGoodVtxs;
}

const SHSuperCluster* SHEvent::getSuperClus(int clusNr)const
{
  SHSuperCluster* clus = (SHSuperCluster*) superClusArray_[clusNr];
  return clus;
}

const SHPreShowerCluster* SHEvent::getPreShowerClus(int clusNr)const
{
  SHPreShowerCluster* clus = (SHPreShowerCluster*) preShowerClusArray_[clusNr];
  return clus;
}

SHSuperCluster* SHEvent::getSuperClus_(int clusNr)
{
  SHSuperCluster* clus = (SHSuperCluster*) superClusArray_[clusNr];
  return clus;
}

const SHMCParticle* SHEvent::getMCParticle(int partNr)const
{
  SHMCParticle* part = (SHMCParticle*) mcPartArray_[partNr];
  return part;
}

const SHMuon* SHEvent::getMuon(int muNr)const
{
  SHMuon* mu = (SHMuon*) muArray_[muNr];
  return mu;
}
const SHVertex* SHEvent::getVertex(int vertexNr)const
{
  SHVertex* vertex = (SHVertex*) vertexArray_[vertexNr];
  return vertex;
}
const SHElectron* SHEvent::getElectron(int eleNr)const
{
  SHElectron* ele = (SHElectron*) electronArray_[eleNr];
  ele->setMotherEvent(this);
  ele->setRhoCorr(eleRhoCorr());
  return ele;
}

const SHJet* SHEvent::getJet(int jetNr)const
{
  SHJet* jet = (SHJet*) jetArray_[jetNr];
  return jet;
}

SHJet* SHEvent::getJet(int jetNr)
{
  SHJet* jet = (SHJet*) jetArray_[jetNr];
  return jet;
}

const SHIsolTrack* SHEvent::getIsolTrk(int trkNr)const
{
  SHIsolTrack* trk = (SHIsolTrack*) isolTrkArray_[trkNr];
  return trk;
}

const SHTrigInfo* SHEvent::getTrigInfo(int trigNr)const
{
  SHTrigInfo* trigInfo = (SHTrigInfo*) trigArray_[trigNr];
  return trigInfo;
}

// const SHL1Cand* SHEvent::getL1Cand(int candNr)const
// {
//   SHL1Cand* l1Cand = (SHL1Cand*) l1CandArray_[candNr];
//   return l1Cand;
// }

//non const acccess
SHElectron* SHEvent::getElectron(int eleNr)
{
  SHElectron* ele = (SHElectron*) electronArray_[eleNr];
  ele->setMotherEvent(this);
  return ele;
}

// const SHIsolCluster* SHEvent::getIsolClus(int clusNr)const
// {
//   SHIsolCluster* clus = (SHIsolCluster*) isolClusArray_[clusNr];
//   return clus;
// }

// const SHIsolSuperCluster* SHEvent::getIsolSuperClus(int clusNr)const
// {
//   SHIsolSuperCluster* clus = (SHIsolSuperCluster*) isolSuperClusArray_[clusNr];
//   return clus;
// }


int SHEvent::getSuperClusIndx(float rawNrgy,float eta,float phi)const
{
  for(int superClusNr=0;superClusNr<nrSuperClus();superClusNr++){
    const SHSuperCluster* superClus = getSuperClus(superClusNr);
    float dNrgyAbs = fabs(superClus->rawNrgy()-rawNrgy);
    float dEtaAbs = fabs(superClus->eta()-eta);
    float dPhiAbs = fabs(superClus->phi()-phi);
    if(dNrgyAbs<1.0E-3 && dEtaAbs<1.0E-3 && dPhiAbs<1.0E-3) return superClusNr;
  }
  return -1;//didnt find it
}

// int SHEvent::getIsolClusIndx(float rawNrgy,float eta,float phi)const
// {
//   for(int clusNr=0;clusNr<nrIsolClus();clusNr++){
//     const SHIsolCluster* clus = getIsolClus(clusNr);
//     float dNrgyAbs = fabs(clus->nrgy()-rawNrgy);
//     float dEtaAbs = fabs(clus->eta()-eta);
//     float dPhiAbs = fabs(clus->phi()-phi);
//     if(dNrgyAbs<1.0E-10 && dEtaAbs<1.0E-10 && dPhiAbs<1.0E-10) return clusNr;
//   }
//   return -1;//didnt find it
// }




void SHEvent::dropTrackerOnlyEles()
{
  bool anyTrackerDrivenEle=false;
  for(int eleNr=0;eleNr<nrElectrons() && !anyTrackerDrivenEle;eleNr++){
    const SHElectron* ele = getElectron(eleNr);
    if(!ele->isEcalDriven()) anyTrackerDrivenEle=true;
  }
  if(anyTrackerDrivenEle){

    //okay it is late and I am tired, hence crap hack
    std::vector<std::pair<const SHElectron*,const SHSuperCluster*> >  ecalEles;
    for(int eleNr=0;eleNr<nrElectrons();eleNr++){
      const SHElectron* ele = getElectron(eleNr);
      if(ele->isEcalDriven()) ecalEles.push_back(std::pair<const SHElectron*,const SHSuperCluster*>(new SHElectron(*ele),ele->superClus()));
    }
    electronArray_.Delete();
    for(size_t eleNr=0;eleNr<ecalEles.size();eleNr++){
      addElectron(*ecalEles[eleNr].first,*ecalEles[eleNr].second);
      delete ecalEles[eleNr].first;
    }
  }    

}

void SHEvent::flushTempData()const
{
  caloHits_.flushIndxTable();
  caloTowers_.flushIndxTable();
  genInfo_.flushIndxTable();
}


void SHEvent::printTruth(int nrLines)const
{
  if(nrMCParticles()>0){
    std::cout << std::setw(2)<<" "<< std::setw(6) << "indx" << std::setw(8) << "stdhep" << std::setw(6) << "idhep" 
	      << std::setw(6) << "jmo1" << std::setw(6) << "jmo2" << std::setw(6) << "jda1" << std::setw(6) << "jda2" 
	      << std::setw(6) << "Px" << std::setw(10) << "Py" << std::setw(10) << "Pz" << std::setw(10) <<"E" 
	      << std::setw(10) << "Pt" <<std::setw(15)<< "Mass" << "\n";
    for(int i=0;i<nrMCParticles() && (i<nrLines || nrLines==-1);i++){
      const SHMCParticle *mcPart = getMCParticle(i);
      std::cout << *mcPart <<std::endl;
    }
  }
}



bool SHEvent::passTrig(const std::string& trigName,double eta,double phi)const
{
  for(int trigNr=0;trigNr<nrTrigs();trigNr++){
    const SHTrigInfo* trig= getTrigInfo(trigNr);
    if( (trig->trigId()==-1 || trig->trigId()==2) && trigName==trig->name()) {
      //  std::cout <<"found trig "<<trigName<<" nr pass "<<trig->nrPass()<<" eta "<<eta<<" phi "<<phi<<" pass "<<trig->passTrig(eta,phi)<<std::endl;
      return trig->passTrig(eta,phi);
    }
  }
  return false;
}


const SHTrigInfo* SHEvent::getTrig(const std::string& trigName)const
{
  for(int trigNr=0;trigNr<nrTrigs();trigNr++){
    const SHTrigInfo* trig= getTrigInfo(trigNr);
    if(trig->name().find(trigName)!=std::string::npos) return trig; //close enough
  }
  return NULL;
}

TLorentzVector  SHEvent::getTrigObj(const std::string& trigName,double eta,double phi)const
{
  for(int trigNr=0;trigNr<nrTrigs();trigNr++){
    const SHTrigInfo* trig= getTrigInfo(trigNr);
    if(trig->trigId()==-1 && trigName==trig->name()) {
      //  std::cout <<"found trig "<<trigName<<" nr pass "<<trig->nrPass()<<" eta "<<eta<<" phi "<<phi<<" pass "<<trig->passTrig(eta,phi)<<std::endl;
      return trig->getTrigObj(eta,phi);
    }
  }
  TLorentzVector returnVal;
  returnVal.SetPtEtaPhiM(0.001,0,0,0);
  return returnVal;
}

bool SHEvent::passL1Trig(const std::string& trigName,double eta,double phi)const
{
  for(int trigNr=0;trigNr<nrTrigs();trigNr++){
    const SHTrigInfo* trig= getTrigInfo(trigNr);
    if(trig->trigId()==-1 && trigName==trig->name()) {
      //  std::cout <<"found trig "<<trigName<<" nr pass "<<trig->nrPass()<<" eta "<<eta<<" phi "<<phi<<" pass "<<trig->passTrig(eta,phi)<<std::endl;
      return trig->passL1Trig(eta,phi);
    }
  }
  return false;
}


bool SHEvent::passTrig(const std::string& trigName)const
{
  for(int trigNr=0;trigNr<nrTrigs();trigNr++){
    const SHTrigInfo* trig= getTrigInfo(trigNr);
    if(trig->name().find(trigName)!=std::string::npos) { //close enough
      //  std::cout <<"found trig "<<trigName<<" nr pass "<<trig->nrPass()<<" eta "<<eta<<" phi "<<phi<<" pass "<<trig->passTrig(eta,phi)<<std::endl;
      return trig->passTrig();
    }
  }
  return false;
}

void SHEvent::printTrigs()const
{
  // std::cout <<"nr triggers fired "<<nrTrigs()<<std::endl;
  for(int i=0;i<nrTrigs();i++){
    if(getTrigInfo(i)->passTrig()||true) std::cout <<" trig "<<i<<" name: "<<getTrigInfo(i)->name()<<" trig code "<<getTrigInfo(i)->trigId()<<" global pass "<<getTrigInfo(i)->passTrig()<<" nr pass "<<getTrigInfo(i)->nrPass()<<" prescale "<<getTrigInfo(i)->preScale()<<std::endl;
  }
}
void SHEvent::printTrigsPassed()const
{
  // std::cout <<"nr triggers fired "<<nrTrigs()<<std::endl;
  for(int i=0;i<nrTrigs();i++){
    if(getTrigInfo(i)->passTrig()) std::cout <<" trig "<<i<<" name: "<<getTrigInfo(i)->name()<<" trig code "<<getTrigInfo(i)->trigId()<<" global pass "<<getTrigInfo(i)->passTrig()<<" nr pass "<<getTrigInfo(i)->nrPass()<<" prescale "<<getTrigInfo(i)->preScale()<<std::endl;
  }
}

void SHEvent::removeDupEles(std::vector<int>& dupEleNrs)
{
  std::vector<SHElectron*> goodEle;
  std::vector<SHElectron*> dupEle;
  for(int eleNr=0;eleNr<nrElectrons();eleNr++){
    if(!std::binary_search(dupEleNrs.begin(),dupEleNrs.end(),eleNr)) goodEle.push_back(getElectron(eleNr));
    else dupEle.push_back(getElectron(eleNr));
  }

  electronArray_.Clear();
  
  for(size_t eleNr=0;eleNr<goodEle.size();eleNr++){
    addElectron(*goodEle[eleNr],*goodEle[eleNr]->superClus());
  }
 
  //I think root has plans for the memory allocated and still owns it

  //for(size_t dupEleNr=0;dupEleNr<dupEle.size();dupEleNr++){
  //   delete dupEle[dupEleNr];
  // }


}


void SHEvent::fixElesNrgy()
{
  for(int eleNr=0;eleNr<nrElectrons();eleNr++){
    SHElectron* ele = getElectron(eleNr);
   
      //  ele->setNewNrgy(ele->nrgy()*fEtCorr_(ele->rawEt(),ele->type()));
    ele->setNewNrgy(ele->clusNrgy());
  }
}

float SHEvent::fEtCorr_(float et,int type)const
{
  float par[5][5] =
    {
      { 0.974507, 1.16569, -0.000884133, 0.161423, -125.356 },
      { 0.974507, 1.16569, -0.000884133, 0.161423, -125.356 },
      { 0.96449, 0.991457, 0.000237869, 0.159983, -4.38755 },
      { 0.97956, 0.883959, 0.000782834, -0.106388, -124.394 },
      { 0.97213, 0.999528, 5.61192e-06, 0.0143269, -17.1776 }
    } ;
  if ( et > 200 )  et =200 ; 
  if ( et < 5 )  return 1. ; 
  if ( 5 <= et && et < 10 )  return par[type][0] ; 
  if ( et <= et && et <= 200 ) return (par[type][1]  + et*par[type][2])*(1- par[type][3]*exp(et/par[type][4]));
  else return 1.;
}
