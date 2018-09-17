import datetime
import numpy as np
import pandas as pd
from decimal import Decimal

decision = input("enter the company for which you want to generate cdr: ")

if decision == "thinq":
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
		thinq_df['Disposition'] = 'ANSWERED'
		thinq_df['CallerID'] = ''
	thinq_df = thinq_df.reindex_axis(['time','from_ani','to_did','billsec','CallerID','Disposition','total','src_ip'], axis=1)
	thinq_df = thinq_df.rename(index=str, columns={"time": "Date", "from_ani": "Source","to_did": "Destination","billsec": "Seconds","total": "Cost","src_ip": "Peer"})

	thinq_df.to_csv('thinq_cdr.csv', encoding='utf-8' , index=False)
	print("The output cdr was saved as thinq_cdr.csv")

elif decision == "avoxi":
	#Importing avoxi file:
	avoxi_name = input('Enter the name of the avoxi file: ')

	avoxi_raw = pd.read_csv(avoxi_name)

	for index, row in avoxi_raw.iterrows():
		avoxi_raw['Disposition'] = 'ANSWERED'
		avoxi_raw['CallerID'] = ''
		
	avoxi_raw = avoxi_raw[['Date/Time','From','To','Duration', 'CallerID', 'Disposition', 'Cost', 'Number/Ext./SIP Trunk']]
	avoxi_df = avoxi_raw.rename(index=str, columns={"Date/Time": "Date", "From": "Source","To": "Destination","Duration": "Seconds","Number/Ext./SIP Trunk": "Peer"})

	avoxi_df = avoxi_df.sort_values(by='Date', ascending=True) # This now sorts in date order

	avoxi_df.to_csv('avoxi_cdr.csv', encoding='utf-8' , index=False)
	print("The output cdr was saved as avoxi_cdr.csv")
	
elif decision == "didx":
	#Importing avoxi file:
	didx_name = input('Enter the name of the didx file: ')

	didx_raw = pd.read_csv(didx_name)
	
	didx_raw['Peer'] = didx_raw['Destination']
		
	didx_raw = didx_raw[['CallDate','CallFrom','Destination','Duration (sec)', 'CallID', 'Status', 'TotalCost', 'Peer']]
	didx_df = didx_raw.rename(index=str, columns={"CallDate": "Date", "CallFrom": "Source","Duration (sec)": "Seconds","CallID": "CallerID","Status": "Disposition","TotalCost": "Cost"})

	didx_df = didx_df.sort_values(by='Date', ascending=True) # This now sorts in date order
	
	#Date format fix
	j = 0
	i = 0
	dimension = (len(didx_df['Date']) - 1)
	Date = []

	while (i <= dimension):
		Date.append(str(didx_df['Date'][i]))
		i += 1
		
	newdates =[]

	for date in Date:
		d = datetime.datetime.strptime(date, '%d-%m-%Y %H:%M')
		date = d.strftime('%Y-%m-%d %H:%M:00')
		newdates.append(date)
		
	didx_df['Date'] = newdates   		
	#Disposition column fix	
	for index, row in didx_df.iterrows():
		didx_df['CallerID'] = ""
	for answer in didx_df['Disposition']:
		if didx_df['Disposition'][j] == "ANSWER":
			didx_df['Disposition'][j] = "ANSWERED"
			j += 1
		elif didx_df['Disposition'][j] == "CANCEL":
			didx_df['Disposition'][j] = "CANCELLED"
			j += 1
		else: 
			print("There is an unknown value on the disposition column")
			j += 1
			
	didx_df.to_csv('didx_cdr.csv', encoding='utf-8' , index=False)
	print("The output cdr was saved as didx_cdr.csv")
	
elif decision == "migesa":
	#migesa
	migesa_name = input('Enter the name of the migesa file: ')
	migesa_raw = pd.read_csv(migesa_name)

	for index, row in migesa_raw.iterrows():
		migesa_raw['Cost'] = migesa_raw['duration']*(.087/60)
		migesa_raw['Peer'] = "38.100.65.27"
		
	migesa_raw = migesa_raw[['calldate','src','dst','duration', 'clid', 'disposition', 'Cost', 'Peer']]
	migesa_df = migesa_raw.rename(index=str, columns={"calldate": "Date", "src": "Source","dst": "Destination","duration": "Seconds","clid": "CallerID", "disposition": "Disposition"})

	migesa_df.to_csv('migesa_cdr.csv', encoding='utf-8', index=False)
	print("The output cdr was saved as migesa_cdr.csv")
	
else:
	print("Please enter a valid provider")

#df = pd.concat([thinq_df, avoxi_df, migesa_df])

#df.to_csv('out.csv', encoding='utf-8', index=False)