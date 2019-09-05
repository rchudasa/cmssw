

import FWCore.ParameterSet.Config as cms

dPhi1SParams=cms.PSet(
    bins= cms.VPSet(
        cms.PSet(binType=cms.string("AbsEtaClus"),xMin=cms.double(0),xMax=cms.double(1.5),yMin=cms.int32(1),yMax=cms.int32(1),
                 funcType=cms.string("TF1:=pol3"),
                 funcParams=cms.vdouble(0.000981,0.000898,-0.00128,0.000897)),
        cms.PSet(binType=cms.string("AbsEtaClus"),xMin=cms.double(0),xMax=cms.double(1.5),yMin=cms.int32(2),yMax=cms.int32(2),
                 funcType=cms.string("TF1:=pol3"),
                 funcParams=cms.vdouble(0.00222,0.000196,-0.000203,0.000447)),
        cms.PSet(binType=cms.string("AbsEtaClus"),xMin=cms.double(0),xMax=cms.double(1.5),yMin=cms.int32(3),yMax=cms.int32(99999),
                 funcType=cms.string("TF1:=pol3"),
                 funcParams=cms.vdouble(0.00236,0.000691,0.000199,0.000416)),
         cms.PSet(binType=cms.string("AbsEtaClus"),xMin=cms.double(1.5),xMax=cms.double(3.0),yMin=cms.int32(1),yMax=cms.int32(1),
                 funcType=cms.string("TF1:=pol1"),
                 funcParams=cms.vdouble(0.00562,-0.00166)),
        cms.PSet(binType=cms.string("AbsEtaClus"),xMin=cms.double(1.5),xMax=cms.double(3.0),yMin=cms.int32(2),yMax=cms.int32(2),
                 funcType=cms.string("TF1:=pol1"),
                 funcParams=cms.vdouble(0.00866,-0.00271)), 
        cms.PSet(binType=cms.string("AbsEtaClus"),xMin=cms.double(1.5),xMax=cms.double(3.0),yMin=cms.int32(3),yMax=cms.int32(99999),
                 funcType=cms.string("TF1:=pol1"),
                 funcParams=cms.vdouble(0.0132,-0.0048)),
        )
    )

dRZ2SParams=cms.PSet(
    bins= cms.VPSet(
        cms.PSet(binType=cms.string("AbsEtaClus"),xMin=cms.double(0),xMax=cms.double(1.5),yMin=cms.int32(1),yMax=cms.int32(99999),
                 funcType=cms.string("TF2:=[0]+[1]*x+[2]*x*x+[3]*std::max(y-[4],0.)"),
                 funcParams=cms.vdouble(0.00317,-0.00337,0.00395,0.0034,4)),
        cms.PSet(binType=cms.string("AbsEtaClus"),xMin=cms.double(1.5),xMax=cms.double(3.0),yMin=cms.int32(1),yMax=cms.int32(1),
                 funcType=cms.string("TF1:=[0]+[1]*TMath::Gaus(x,[2],[3],1)"),
                 funcParams=cms.vdouble(0.00435,0.00289,1.65,0.22)),
        cms.PSet(binType=cms.string("AbsEtaClus"),xMin=cms.double(1.5),xMax=cms.double(3.0),yMin=cms.int32(2),yMax=cms.int32(2),
                 funcType=cms.string("TF1:=[0]+[1]*TMath::Gaus(x,[2],[3],1)"),
                 funcParams=cms.vdouble(0.00541,0.00404,1.76,0.22)), 
        cms.PSet(binType=cms.string("AbsEtaClus"),xMin=cms.double(1.5),xMax=cms.double(3.0),yMin=cms.int32(3),yMax=cms.int32(3),
                 funcType=cms.string("TF1:=[0]+[1]*TMath::Gaus(x,[2],[3],1)"),
                 funcParams=cms.vdouble(0.00856,0.00351,1.79,0.138)),
        cms.PSet(binType=cms.string("AbsEtaClus"),xMin=cms.double(1.5),xMax=cms.double(3.0),yMin=cms.int32(4),yMax=cms.int32(99999),
                 funcType=cms.string("TF1:=[0]+[1]*TMath::Gaus(x,[2],[3],1)"),
                 funcParams=cms.vdouble(0.00669,0.0123,1.75,0.236))
        )
    )

dPhi2SParams=cms.PSet(
    bins=cms.VPSet(
        cms.PSet(binType=cms.string("AbsEtaClus"),xMin=cms.double(0),xMax=cms.double(3.0),yMin=cms.int32(1),yMax=cms.int32(99999),
                 funcType=cms.string("TF1:=pol0"),
                 funcParams=cms.vdouble(0.00011,)),
        )
)
