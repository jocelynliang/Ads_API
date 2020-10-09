import pandas as pd
import numpy as np
from datetime import datetime
import io
from googleads import adwords

PAGE_SIZE = 100

def p2f(x):
    return float(x.strip('%'))/100

def getCampaignInfo(start_date, end_date, client):
    
    output = io.StringIO()
    
    report_downloader = client.GetReportDownloader(version='v201809')

    report_query = (adwords.ReportQueryBuilder()
                  .Select('Date', 'CampaignName', 'CampaignStatus','AdNetworkType1','Impressions',
                          'Clicks','Cost', 'Ctr', 'AverageCpc')
                  .From('CAMPAIGN_PERFORMANCE_REPORT')
                  .Where('CampaignStatus').In('ENABLED','PAUSED','REMOVED')
                  .During(start_date + ',' + end_date)  
                  .Build())

    report_downloader.DownloadReportWithAwql(report_query, 'CSV', output, skip_report_header=True,
              skip_column_header=False, skip_report_summary=True,
              include_zero_impressions=False)

    output.seek(0)
    
    types= { 'Clicks': np.float64, 'Impressions': np.float64,
             'Cost': np.float64, 'Ctr': np.float64, 'AverageCpc': np.float64 }

    df_campaign = pd.read_csv(output,low_memory=False, dtype= types, keep_default_na=False)

    df_campaign['Day'] = df_campaign['Day'].apply(lambda s: datetime.strptime(s, '%Y-%m-%d').date())
    df_campaign['Cost'] = df_campaign['Cost']/1000000
    df_campaign['CTR'] = df_campaign['CTR'].apply(lambda s: p2f(s))
    df_campaign['Avg. CPC'] = df_campaign['Avg. CPC']/1000000
 
    print(df_campaign)
    
    return df_campaign

