#ifdef __CLING__
R__LOAD_LIBRARY(libDelphes)
#include "classes/DelphesClasses.h"
#include "external/ExRootAnalysis/ExRootTreeReader.h"
#include "external/ExRootAnalysis/ExRootResult.h"
#else
class ExRootTreeReader;
class ExRootResult;
#endif

float deltaR(GenParticle * g, Jet * j)
{

return sqrt(pow(g->Phi-j->Phi,2)+pow(g->Eta-j->Eta,2));

}

void doplots(TFile * f, string s, bool hasPileup)
{

  TChain *chain = new TChain("Delphes");
  string filename = s+".root";
  chain->Add(filename.c_str());
  ExRootTreeReader *treeReader = new ExRootTreeReader(chain);
  TClonesArray *branchJet = 0;
  if (hasPileup) branchJet = treeReader->UseBranch("JetPUPPIAK8");
  else branchJet = treeReader->UseBranch("JetAK8");
  TClonesArray *branchParticle = treeReader->UseBranch("Particle");
  TClonesArray *branchWeight = treeReader->UseBranch("Weight");
  Long64_t allEntries = treeReader->GetEntries();
  cout << "Total Events "<<s<<" "<<allEntries << endl;

  int nbin=1000;
  f->cd();
  f->mkdir(s.c_str());
  f->cd(s.c_str());

  TH1F *hTau32Barrel_W=new TH1F("hTau32Barrel_W",";#tau_{21};Fraction of events",nbin,0,1);
  TH1F *hMassBarrel_W=new TH1F("hMassBarrel_W",";Mass [Gev];Fraction of events",nbin,0,200);
  TH1F *hSDMassBarrel_W=new TH1F("hSDMassBarrel_W",";SD Mass [GeV];Fraction of events",nbin,0,200);

  TH1F *hTau32Barrel_Z=new TH1F("hTau32Barrel_Z",";#tau_{21};Fraction of events",nbin,0,1);
  TH1F *hMassBarrel_Z=new TH1F("hMassBarrel_Z",";Mass [Gev];Fraction of events",nbin,0,200);
  TH1F *hSDMassBarrel_Z=new TH1F("hSDMassBarrel_Z",";SD Mass [GeV];Fraction of events",nbin,0,200);

  TH1F *hTau32HGCAL_W=new TH1F("hTau32HGCAL_W",";#tau_{21};Fraction of events",nbin,0,1);
  TH1F *hMassHGCAL_W=new TH1F("hMassHGCAL_W",";Mass [Gev];Fraction of events",nbin,0,200);
  TH1F *hSDMassHGCAL_W=new TH1F("hSDMassHGCAL_W",";SD Mass [GeV];Fraction of events",nbin,0,200);

  TH1F *hTau32HGCAL_Z=new TH1F("hTau32HGCAL_Z",";#tau_{21};Fraction of events",nbin,0,1);
  TH1F *hMassHGCAL_Z=new TH1F("hMassHGCAL_Z",";Mass [Gev];Fraction of events",nbin,0,200);
  TH1F *hSDMassHGCAL_Z=new TH1F("hSDMassHGCAL_Z",";SD Mass [GeV];Fraction of events",nbin,0,200);

  TH1F *hPtBarrel=new TH1F("hPtBarrel",";p_{T} [GeV];Fraction of events",nbin,0,1000);
  TH1F *hEtaBarrel=new TH1F("hEtaBarrel",";#Eta;Fraction of events",nbin,-5,5);
  TH1F *hPtHGCAL=new TH1F("hPtHGCAL",";p_{T} [GeV];Fraction of events",nbin,0,1000);
  TH1F *hEtaHGCAL=new TH1F("hEtaHGCAL",";#Eta;Fraction of events",nbin,-5,5);

  // TProfile *hPtBarrel=new TH1F("hBarrel",";p_{T} [GeV];Fraction of events",nbin,0,1000);
  // TProfile *hPtHGCAL=new TH1F("hPtHGCAL",";p_{T} [GeV];Fraction of events",nbin,0,1000);

  Jet *jet;
  GenParticle *particle;

  float lowHG=1.5;
  float highHG=3.0;

  for(Long64_t entry = 0; entry < allEntries; ++entry)
  {
    treeReader->ReadEntry(entry);
    if(entry % 1000==0)std::cout<<"Running on event no: "<<entry<<"---completed : "<<(float(entry)/float(allEntries))*100<<" %"<<std::endl;

    int foundZ=-1;
    int foundW=-1;
    for(Int_t j = 0; j < branchParticle->GetEntriesFast(); ++j)
    {
      if (foundW>-1 && foundZ>-1) break;
      particle = (GenParticle*) branchParticle->At(j);
      if (abs(particle->PID)==23) foundZ=j;
      if (abs(particle->PID)==24) foundW=j;
    }

    GenParticle *particleZ;
    GenParticle *particleW;

    if (foundW>-1) particleW=(GenParticle *)branchParticle->At(foundW);
    if (foundZ>-1) particleZ=(GenParticle *)branchParticle->At(foundZ);

    int foundZmatch=-1;
    int foundWmatch=-1;
    float drZ=100; float drW=100;

    for(Int_t i = 0; i < branchJet->GetEntriesFast(); ++i)
    {
      jet = (Jet*) branchJet->At(i);

      if (foundW>-1)
      {
        if (deltaR(particleW,jet)<drW)
        {
          drW=deltaR(particleW,jet);
          foundWmatch=i;
        }
      }
      if (foundZ>-1)
      {
        if (deltaR(particleZ,jet)<drZ)
        {
          drZ=deltaR(particleZ,jet);
          foundZmatch=i;
        }
      }
    }
    float weight = ((Weight*)branchWeight->At(0))->Weight;
    if(foundZmatch>-1 && drZ<0.8)
    {
      Jet* the_z = (Jet*)branchJet->At(foundZmatch);
      if (fabs(the_z->Eta)<1.5)
      {
        hPtBarrel->Fill(the_z->PT,weight);
        hEtaBarrel->Fill(the_z->Eta,weight);
        hTau32Barrel_Z->Fill(the_z->Tau[2]/the_z->Tau[1] ,weight);
        hMassBarrel_Z->Fill(the_z->Mass ,weight);
        hSDMassBarrel_Z->Fill(the_z->SoftDroppedJet.M() ,weight);
      }
      if (fabs(the_z->Eta)<3.0 && fabs(the_z->Eta)>1.5)
      {
        hPtHGCAL->Fill(the_z->PT,weight);
        hEtaHGCAL->Fill(the_z->Eta,weight);
        hTau32HGCAL_Z->Fill(the_z->Tau[2]/the_z->Tau[1] ,weight);
        hMassHGCAL_Z->Fill(the_z->Mass ,weight);
        hSDMassHGCAL_Z->Fill(the_z->SoftDroppedJet.M() ,weight);
      }
    }
    if(foundWmatch>-1 && drW<0.8)
    {
      Jet* the_w = (Jet*)branchJet->At(foundWmatch);
      if (fabs(the_w->Eta)<1.5)
      {
        hPtBarrel->Fill(the_w->PT,weight);
        hEtaBarrel->Fill(the_w->Eta,weight);
        hTau32Barrel_W->Fill(the_w->Tau[2]/the_w->Tau[1] ,weight);
        hMassBarrel_W->Fill(the_w->Mass ,weight);
        hSDMassBarrel_W->Fill(the_w->SoftDroppedJet.M() ,weight);
      }
      if (fabs(the_w->Eta)<3.0 && fabs(the_w->Eta)>1.5)
      {
        hPtHGCAL->Fill(the_w->PT,weight);
        hEtaHGCAL->Fill(the_w->Eta,weight);
        hTau32HGCAL_W->Fill(the_w->Tau[2]/the_w->Tau[1] ,weight);
        hMassHGCAL_W->Fill(the_w->Mass ,weight);
        hSDMassHGCAL_W->Fill(the_w->SoftDroppedJet.M() ,weight);
      }
    }


  }
}

void Granularity()
{

  gSystem->Load("libDelphes");

  TFile *f=new TFile("Granularity.root","RECREATE");

  doplots(f,"WZ_M800_PU0_G0X",false);
  doplots(f,"WZ_M1600_PU0_G0X",false);

  doplots(f,"WZ_M800_PU0_G1X",false);
  doplots(f,"WZ_M1600_PU0_G1X",false);

  doplots(f,"WZ_M800_PU0_G2X",false);
  doplots(f,"WZ_M1600_PU0_G2X",false);

  doplots(f,"WZ_M800_PU0_G6X",false);
  doplots(f,"WZ_M1600_PU0_G6X",false);

  doplots(f,"WZ_M800_PU200_G1X",true);
  doplots(f,"WZ_M1600_PU200_G1X",true);

  doplots(f,"WZ_M800_PU200_G2X",true);
  doplots(f,"WZ_M1600_PU200_G2X",true);

  doplots(f,"WZ_M800_PU200_G6X",true);
  doplots(f,"WZ_M1600_PU200_G6X",true);

  ExRootResult *result = new ExRootResult();

 



f->Write();
}
