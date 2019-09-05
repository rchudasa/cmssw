#ifndef SHTRIGINFO
#define SHTRIGINFO

//this is a small class which holds information about a certain trigger
//currently this information is limited to the p4 of objects which pass it

#include "TObject.h"
#include "TLorentzVector.h"

#include <vector>
#include <string>

class SHTrigInfo : public TObject {

private:
  std::vector<TLorentzVector> trigObjs_;
  int trigId_;
  std::string trigName_;
  std::string lastFilterName_;
  bool pass_;
  int preScale_;

public:
  SHTrigInfo(int iTrigId=-1,const std::string& iTrigName="",const std::string& iLastFilterName="",bool iPass=false,int iPreScale=1):trigObjs_(),trigId_(iTrigId),trigName_(iTrigName),lastFilterName_(iLastFilterName),pass_(iPass),preScale_(iPreScale){}
  ~SHTrigInfo(){}
  
  //modifiers
  void setTrigId(int iTrigId){trigId_=iTrigId;}
  void setTrigName(const std::string& iTrigName){trigName_=iTrigName;}
  void setLastFilterName(const std::string& iName){lastFilterName_=iName;}
  void addObj(const TLorentzVector& iP4){trigObjs_.push_back(iP4);} 
  void setPass(bool iPass){pass_=iPass;}
  void setPreScale(int iPreScale){preScale_=iPreScale;}
  void clear(){trigObjs_.clear();}

  //accessors
  int nrPass()const{return trigObjs_.size();}
  int preScale()const{return preScale_;}
  const TLorentzVector & getObjP4(int indx)const{return trigObjs_[indx];}
  int trigId()const{return trigId_;}
  const std::string& name()const{return trigName_;}
  const std::string& lastFilter()const{return lastFilterName_;}

  float maxEtObj()const;

  //trigger pass functions

  //just asks is there an object which has passed the trigger in the event
  bool passTrig()const{return pass_;}
  //does a deltaR matching on the objects p4 to see if there is a trigger object which matches it
  bool passTrig(const TLorentzVector& p4)const{return passTrig(p4.Eta(),p4.Phi());}
  bool passTrig(double eta,double phi)const;
  TLorentzVector getTrigObj(double eta,double phi)const;
  bool passL1Trig(const TLorentzVector& p4)const{return passL1Trig(p4.Eta(),p4.Phi());}
  bool passL1Trig(double eta,double phi,TLorentzVector& matchedP4)const;
  bool passL1Trig(double eta,double phi)const{TLorentzVector matchedP4;return passL1Trig(eta,phi,matchedP4);}
  TLorentzVector getL1TrigObj(double eta,double phi)const{TLorentzVector matchedP4;passL1Trig(eta,phi,matchedP4);return matchedP4;}
  //TLorentzVector getL1TrigObj(double eta,double phi)const{}
  
  
  ClassDef(SHTrigInfo,4)
};

#endif
