#!/usr/bin/env python

import uproot
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa

def main():
  # Open DAOD file with uproot
  filename = "/mnt/disks/disk-1/root_sample_data/mc16_13TeV.DAOD_TOPQ1.17829204._000001.pool.root.1"
  myfile = uproot.open(filename)  
  mytree = myfile["CollectionTree"]  

  # Read 3 variables into pandas dataframe
  mydf = mytree.pandas.df(["AntiKt10TruthJetsAuxDyn.JetEMScaleMomentum_pt", "AntiKt10TruthJetsAuxDyn.JetEMScaleMomentum_eta", "AntiKt10TruthJetsAuxDyn.JetEMScaleMomentum_phi"])
  print(mydf)
  mydf.rename(columns={"AntiKt10TruthJetsAuxDyn.JetEMScaleMomentum_pt":"AntiKt10TruthJetsAuxDyn_JetEMScaleMomentum_pt",
                       "AntiKt10TruthJetsAuxDyn.JetEMScaleMomentum_eta":"AntiKt10TruthJetsAuxDyn_JetEMScaleMomentum_eta",
                       "AntiKt10TruthJetsAuxDyn.JetEMScaleMomentum_phi":"AntiKt10TruthJetsAuxDyn_JetEMScaleMomentum_phi"},inplace=True)
  print(mydf)

  # Convert the df and save it to parquet file
  table = pa.Table.from_pandas(mydf)
  pq.write_table(table, 'test-conversion-variables.parquet')
  #pq.write_table(table, 'test-conversion-all.parquet', compression='zstd', compression_level=22)

  # Read back parquet file
  table2 = pq.read_table('test-conversion-variables.parquet')
  mydf2 = table2.to_pandas()
  print(mydf2)

if __name__ == "__main__":
  main()

