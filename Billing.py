from datetime import datetime
import numpy as np
import pandas as pd

#Number of thinq files after unzipping (thinq)
thinq_amount = int(input('Enter the amount of thinq files:'))
thinq_iterations = np.arange(thinq_amount)

#Creating Request for thinq file names 
thinq_dataframes = []
files = []
for i in thinq_iterations:
    files.append(str(input("Enter the name of the thinq files:")))    

#thinq concat to unify all thinq files unzipped
for file in files:
    filename = '%s'%(file)
    thinq_dataframes.append(pd.read_csv(filename))
thinq_df = pd.concat(thinq_dataframes)

for index, row in thinq_df.iterrows():
    thinq_df['Disposition'] = 'ANSWERED'py
    thinq_df['CallerID'] = ''
thinq_df = thinq_df.reindex_axis(['time','from_ani','to_did','billsec','CallerID','Disposition','total','src_ip'], axis=1)
thinq_df = thinq_df.rename(index=str, columns={"time": "Date", "from_ani": "Source","to_did": "Destination","billsec": "Seconds","total": "Cost","src_ip": "Peer"})

thinq_df.to_csv('cdr', encoding='utf-8' , index=False)

'''
#Importing avoxi file:
avoxi_name = input('Enter the name of the avoxi file: ')

avoxi_raw = pd.read_csv(avoxi_name)

for index, row in avoxi_raw.iterrows():
    avoxi_raw['Disposition'] = 'ANSWERED'
    avoxi_raw['CallerID'] = ''
    
avoxi_raw = avoxi_raw[['Date/Time','Caller ID (From)','Caller ID (To)','Duration', 'CallerID', 'Disposition', 'Cost', 'Account ID']]
avoxi_df = avoxi_raw.rename(index=str, columns={"Date/Time": "Date", "Caller ID (From)": "Source","Caller ID (To)": "Destination","Duration": "Seconds","Account ID": "Peer"})

avoxi_df.to_csv('thinq_final', encoding='utf-8' , index=False)

#migesa

migesa_name = input('Enter the name of the migesa file: ')
migesa_raw = pd.read_csv(migesa_name)

for index, row in migesa_raw.iterrows():
    migesa_raw['Cost'] = migesa_raw['duration']*(.087/60)
    migesa_raw['Peer'] = "38.100.65.27"
    
migesa_raw = migesa_raw[['calldate','src','dst','duration', 'clid', 'disposition', 'Cost', 'Peer']]
migesa_df = migesa_raw.rename(index=str, columns={"calldate": "Date", "src": "Source","dst": "Destination","duration": "Seconds","clid": "CallerID", "disposition": "Disposition"})

migesa_df.to_csv('out.csv', encoding='utf-8', index=False)
'''

#df = pd.concat([thinq_df, avoxi_df, migesa_df])

#df.to_csv('out.csv', encoding='utf-8', index=False)