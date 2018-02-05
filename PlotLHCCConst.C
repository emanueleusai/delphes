#ifdef __CLING__
R__LOAD_LIBRARY(libDelphes)
#include "classes/DelphesClasses.h"
#include "external/ExRootAnalysis/ExRootTreeReader.h"
#include "external/ExRootAnalysis/ExRootResult.h"
#else
class ExRootTreeReader;
class ExRootResult;
#endif



void PlotLHCCConst(){

  gSystem->Load("libDelphes");
  TChain *chainQCDP2 = new TChain("Delphes");
  //chainQCDP2->Add("root://cmseos.fnal.gov//store/user/snowmass/noreplica/TDRMiniAOD_Checks/Delphes342pre11/QCD_Mdijet-1000toInf_TuneCUETP8M1_14TeV-pythia8_200PU/QCD_Mdijet-1000toInf_TuneCUETP8M1_14TeV-pythia8_*.root");//inputFile);
  chainQCDP2->Add("QCD_Mdijet-1000toInf_TuneCUETP8M1_14TeV-pythia8_1.root");//inputFile);



  TChain *chainQCDP0 = new TChain("Delphes");
  //chainQCDP0->Add("root://cmseos.fnal.gov//store/user/snowmass/noreplica/TDRMiniAOD_Checks/Delphes342pre11/QCD_Mdijet-1000toInf_TuneCUETP8M1_14TeV-pythia8_200PU_NoHGCAL/QCD_Mdijet-1000toInf_TuneCUETP8M1_14TeV-pythia8_*.root");
  chainQCDP0->Add("QCD_Mdijet-1000toInf_TuneCUETP8M1_14TeV-pythia8_1.root");


  TChain *chainRSGP2 = new TChain("Delphes");
  //chainRSGP2->Add("root://cmseos.fnal.gov//store/user/snowmass/noreplica/TDRMiniAOD_Checks/Delphes342pre11/RSGluonToTT_M-3000_TuneCUETP8M1_14TeV-pythia8_200PU/RSGluonToTT_M-3000_TuneCUETP8M1_14TeV-pythia8_*.root");
  chainRSGP2->Add("QCD_Mdijet-1000toInf_TuneCUETP8M1_14TeV-pythia8_1.root");

  TChain *chainRSGP0 = new TChain("Delphes");
  //chainRSGP0->Add("root://cmseos.fnal.gov//store/user/snowmass/noreplica/TDRMiniAOD_Checks/Delphes342pre11/RSGluonToTT_M-3000_TuneCUETP8M1_14TeV-pythia8_200PU_NoHGCAL/RSGluonToTT_M-3000_TuneCUETP8M1_14TeV-pythia8_*.root");
  chainRSGP0->Add("QCD_Mdijet-1000toInf_TuneCUETP8M1_14TeV-pythia8_1.root");




  TFile *f=new TFile("LHCCHistograms.root","RECREATE");

  TH1F *hConstsQCDP2Barrel=new TH1F("hConstsQCDP2Barrel","hConstsQCDP2Barrel",32,0,160);
  TH1F *hConstsQCDP2Endcap=new TH1F("hConstsQCDP2Endcap","hConstsQCDP2Endcap",32,0,160); 
  TH1F *hConstsQCDP0Barrel=new TH1F("hConstsQCDP0Barrel","hConstsQCDP0Barrel",32,0,160);
  TH1F *hConstsQCDP0Endcap=new TH1F("hConstsQCDP0Endcap","hConstsQCDP0Endcap",32,0,160);

  TH1F *hTau32RSGP2Barrel=new TH1F("hTau32RSGP2Barrel","hTau32RSGP2Barrel",50,0,1);
  TH1F *hTau32RSGP2Endcap=new TH1F("hTau32RSGP2Endcap","hTau32RSGP2Endcap",50,0,1);
  
  TH1F *hTau32RSGP0Barrel=new TH1F("hTau32RSGP0Barrel","hTau32RSGP0Barrel",50,0,1);
  TH1F *hTau32RSGP0Endcap=new TH1F("hTau32RSGP0Endcap","hTau32RSGP0Endcap",50,0,1);  

  TH1F *hTau32QCDP2Barrel=new TH1F("hTau32QCDP2Barrel","hTau32QCDP2Barrel",50,0,1);
  TH1F *hTau32QCDP2Endcap=new TH1F("hTau32QCDP2Endcap","hTau32QCDP2Endcap",50,0,1);

  TH1F *hTau32QCDP0Barrel=new TH1F("hTau32QCDP0Barrel","hTau32QCDP0Barrel",50,0,1);
  TH1F *hTau32QCDP0Endcap=new TH1F("hTau32QCDP0Endcap","hTau32QCDP0Endcap",50,0,1);










  ExRootTreeReader *treeReaderQCDP2 = new ExRootTreeReader(chainQCDP2);
  ExRootTreeReader *treeReaderQCDP0 = new ExRootTreeReader(chainQCDP0);
  ExRootTreeReader *treeReaderRSGP2 = new ExRootTreeReader(chainRSGP2);
  ExRootTreeReader *treeReaderRSGP0 = new ExRootTreeReader(chainRSGP0);



  ExRootResult *result = new ExRootResult();

  //TClonesArray *branchParticle = treeReader->UseBranch("Particle");
  //TClonesArray *branchElectron = treeReader->UseBranch("Electron");
  //TClonesArray *branchPhoton = treeReader->UseBranch("Photon");
  //TClonesArray *branchMuon = treeReader->UseBranch("MuonLoose");
  //TClonesArray *branchEFlowTrack = treeReader->UseBranch("EFlowTrack");
  //TClonesArray *branchEFlowPhoton = treeReader->UseBranch("EFlowPhoton");
  //TClonesArray *branchEFlowNeutralHadron = treeReader->UseBranch("EFlowNeutralHadron");
  TClonesArray *branchJetQCDP2 = treeReaderQCDP2->UseBranch("JetPUPPIAK8");
  TClonesArray *branchJetQCDP0 = treeReaderQCDP0->UseBranch("JetPUPPIAK8");
  TClonesArray *branchJetRSGP2 = treeReaderRSGP2->UseBranch("JetPUPPIAK8");
  TClonesArray *branchJetRSGP0 = treeReaderRSGP0->UseBranch("JetPUPPIAK8");

  



  Long64_t allEntriesQCDP2 = treeReaderQCDP2->GetEntries();
  Long64_t allEntriesQCDP0 = treeReaderQCDP0->GetEntries();
  Long64_t allEntriesRSGP2 = treeReaderRSGP2->GetEntries();
  Long64_t allEntriesRSGP0 = treeReaderRSGP0->GetEntries();



  cout << "Total Events QCD P2 " << allEntriesQCDP2 << endl;
  cout << "Total Events QCD P0 " << allEntriesQCDP0 << endl;
  cout << "Total Events RSG P2 " << allEntriesRSGP2 << endl;
  cout << "Total Events RSG P0 " << allEntriesRSGP0 << endl;




  //GenParticle *particle;
  //Electron *electron;
  //Photon *photon;
  //Muon *muon;

  //Track *track;
  //Tower *tower;

  Jet *jetQCDP2;
  Jet *jetQCDP0;
  Jet *jetRSGP2;
  Jet *jetRSGP0;
  //TObject *object;

 // TLorentzVector momentum;

 // Float_t Eem, Ehad;
 // Bool_t skip;

  Long64_t entryQCDP2;
  Long64_t entryQCDP0;
  Long64_t entryRSGP2;
  Long64_t entryRSGP0;




 // Int_t i, j, pdgCode;
  /////////////////////////////////////////////////////////////////////////////QCD P2
  for(entryQCDP2 = 0; entryQCDP2 < allEntriesQCDP2; ++entryQCDP2)
  {//event loop
    treeReaderQCDP2->ReadEntry(entryQCDP2);

   // cout<<"QCDP2 event num: "<<entryQCDP2<<endl;

  if(entryQCDP2 % 1000==0)std::cout<<"Running on QCDP2  event no: "<<entryQCDP2<<"---completed : "<<(float(entryQCDP2)/float(allEntriesQCDP2))*100<<" %"<<std::endl;


  for(Int_t i = 0; i < branchJetQCDP2->GetEntriesFast(); ++i){//jet loop

     jetQCDP2 = (Jet*) branchJetQCDP2->At(i);

     if(i>0)continue;
     if(jetQCDP2->PT < 500.) continue;
     if(jetQCDP2->PT >700.) continue;   


   if(fabs(jetQCDP2->Eta)<0.9){

     hConstsQCDP2Barrel->Fill(jetQCDP2->Constituents.GetEntriesFast());      
     hTau32QCDP2Barrel->Fill(jetQCDP2->Tau[2]/jetQCDP2->Tau[1]);
        }//barrel

   
   if(fabs(jetQCDP2->Eta) > 1.56){//endcap

      hConstsQCDP2Endcap->Fill(jetQCDP2->Constituents.GetEntriesFast());
      hTau32QCDP2Endcap->Fill(jetQCDP2->Tau[2]/jetQCDP2->Tau[1]);


        }//endcap


  }//jet loop

  }//event loop

  ////////////////////////////////////////////////////////////////////////////////QCDP2



  //////////////////////////////////////////////////////////////QCD P0
  for(entryQCDP0 = 0; entryQCDP0 < allEntriesQCDP0; ++entryQCDP0)
  {//event loop
    treeReaderQCDP0->ReadEntry(entryQCDP0);

  

  if(entryQCDP0 % 1000==0)std::cout<<"Running on QCDP0  event no: "<<entryQCDP0<<"---completed : "<<(float(entryQCDP0)/float(allEntriesQCDP0))*100<<" %"<<std::endl;


  for(Int_t i = 0; i < branchJetQCDP0->GetEntriesFast(); ++i){//jet loop

     jetQCDP0 = (Jet*) branchJetQCDP0->At(i);

     if(i>0)continue;
     if(jetQCDP0->PT < 500.) continue;
     if(jetQCDP0->PT >700.) continue;


   if(fabs(jetQCDP0->Eta)<0.9){

     hConstsQCDP0Barrel->Fill(jetQCDP0->Constituents.GetEntriesFast());
     hTau32QCDP0Barrel->Fill(jetQCDP0->Tau[2]/jetQCDP0->Tau[1]);
        }//barrel


   if(fabs(jetQCDP0->Eta) > 1.56){//endcap

      hConstsQCDP0Endcap->Fill(jetQCDP0->Constituents.GetEntriesFast());
      hTau32QCDP0Endcap->Fill(jetQCDP0->Tau[2]/jetQCDP0->Tau[1]);


        }//endcap


  }//jet loop

  }//event loop  



  /////////////////////////////////////////////////////////////QCDP0

  /////////////////////////////////////////////////////////////////RSGP2
  
  for(entryRSGP2 = 0; entryRSGP2 < allEntriesRSGP2; ++entryRSGP2)
  {//event loop
    treeReaderRSGP2->ReadEntry(entryRSGP2);

  

  if(entryRSGP2 % 1000==0)std::cout<<"Running on RSGP2  event no: "<<entryRSGP2<<"---completed : "<<(float(entryRSGP2)/float(allEntriesRSGP2))*100<<" %"<<std::endl;


  for(Int_t i = 0; i < branchJetRSGP2->GetEntriesFast(); ++i){//jet loop

     jetRSGP2 = (Jet*) branchJetRSGP2->At(i);

     if(i>0)continue;
     if(jetRSGP2->PT < 500.) continue;
     if(jetRSGP2->PT >700.) continue;


   if(fabs(jetRSGP2->Eta)<0.9){

     //hConstsRSGP2Barrel->Fill(jetRSGP2->Constituents.GetEntriesFast());
     hTau32RSGP2Barrel->Fill(jetRSGP2->Tau[2]/jetRSGP2->Tau[1]);
        }//barrel


   if(fabs(jetRSGP2->Eta) > 1.56){//endcap

      //hConstsRSGP2Endcap->Fill(jetRSGP2->Constituents.GetEntriesFast());
      hTau32RSGP2Endcap->Fill(jetRSGP2->Tau[2]/jetRSGP2->Tau[1]);


        }//endcap


  }//jet loop

  }//event loop

  /////////////////////////////////////////////////////////RSGP2
  //


  /////////////////////////////////////////////////////RSGP0
  for(entryRSGP0 = 0; entryRSGP0 < allEntriesRSGP0; ++entryRSGP0)
  {//event loop
    treeReaderRSGP0->ReadEntry(entryRSGP0);

  

  if(entryRSGP0 % 1000==0)std::cout<<"Running on RSGP0  event no: "<<entryRSGP0<<"---completed : "<<(float(entryRSGP0)/float(allEntriesRSGP0))*100<<" %"<<std::endl;


  for(Int_t i = 0; i < branchJetRSGP0->GetEntriesFast(); ++i){//jet loop

     jetRSGP0 = (Jet*) branchJetRSGP0->At(i);

     if(i>0)continue;
     if(jetRSGP0->PT < 500.) continue;
     if(jetRSGP0->PT >700.) continue;


   if(fabs(jetRSGP0->Eta)<0.9){

     //hConstsRSGP0Barrel->Fill(jetRSGP0->Constituents.GetEntriesFast());
     hTau32RSGP0Barrel->Fill(jetRSGP0->Tau[2]/jetRSGP0->Tau[1]);
        }//barrel


   if(fabs(jetRSGP0->Eta) > 1.56){//endcap

      //hConstsRSGP0Endcap->Fill(jetRSGP0->Constituents.GetEntriesFast());
      hTau32RSGP0Endcap->Fill(jetRSGP0->Tau[2]/jetRSGP0->Tau[1]);


        }//endcap


  }//jet loop

  }//event loop




  ////////////////////////////////////////////////RSGP0






f->Write();
}
