import pandas as pd
import sys

rename=sys.argv[1]
seedf=sys.argv[2]
outf=sys.argv[3]
df = pd.read_csv(rename, header=None, sep="\t")
df_seed= pd.read_csv(seedf, sep="\t")

seed=[item.replace("<","").replace(">","") for item in df_seed.iloc[:,0].tolist()]
df=df.iloc[:,:2]

print(seed[:50])
df.columns=['Old IRI', 'New IRI']
print(df.head())
print(len(df))
df=df[df['Old IRI'].isin(seed)]
print(len(df))
df.to_csv(outf,sep="\t",index=False)