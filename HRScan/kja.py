import pandas
df = pd.read_excel('data.xlsx', sheet_name=None)  
for key in df: 
   df[key].to_csv('%s.csv' %key)