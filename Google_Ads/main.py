import numpy as np
import pandas as pd
from googleads import adwords
from datetime import datetime, timedelta
from getCampaignInfo import getCampaignInfo
from getConversion import getConversion
from dwh_write import writeData

def main(days=3):
    
    # Define the report date range: past 3 days including today
    start_date = datetime.today() - timedelta(days=days)
    end_date = datetime.today() - timedelta(days=1)
    start_date = start_date.date().isoformat().replace("-","")
    end_date = end_date.date().isoformat().replace("-","")
    
    # get connected
    client = adwords.AdWordsClient.LoadFromStorage('./googleads.yaml')
    client.SetClientCustomerId('3275422553')
    
    # run the functions
    df_campaign = getCampaignInfo(start_date, end_date, client)
    
    df_conversion = getConversion(start_date, end_date, client)
    
    # combine two dataframes and prepare data
    df = df_campaign.merge(df_conversion, on = ['Day', 'Campaign'], how = 'outer')
    
    # replace NaN with None, SQL database cannot read NaN
    df = df.replace({np.nan: None})
    
    # prepare the data into readable format
    res = []
    for i in range(len(df)):
        row = df.iloc[i,:]
        record = ()
        for j in range(len(df.columns)):
            value = (row[j])
            record = record + (value,)
               
        res.append(record)
    print(res)
     
    # write data into DWH
    writeData(res)
    
if __name__ == '__main__':
    main()