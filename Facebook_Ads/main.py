import numpy as np
import pandas as pd
import datetime as dt
from GetCampaignInfo import getCampaignInfo
from ProcessData import processData
from WriteData import writeData

def main(days=3):
    data = []
    
    # Get the date for the past 3 days 
    for i in range(1, (days+1)):
        date = dt.datetime.today() - dt.timedelta(days = i)
        date = str(date.date())
       
        # Get campaign info from Facebook  
        list_active, list_inactive = getCampaignInfo(date)
        
        # Process data from Facebook
        df_active = processData(list_active, 'active')
        df_inactive = processData(list_inactive, 'inactive')
        
        frames = [df_active, df_inactive]
        df = pd.concat(frames)
        df = df.replace({np.nan: None})
    
        # Prepare the data frame into readable format
        for i in range(len(df)):
            row = df.iloc[i,:]
            record = ()
            for j in range(len(df.columns)):
                value = (row[j])
                record = record + (value,)             
            data.append(record)
    
    print(data)
    
    # Load into DWH
    writeData(data)
    
    print("The job has been done.")
  
if __name__ == '__main__':
    main()