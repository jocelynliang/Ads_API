import pandas as pd
import numpy as np
from datetime import datetime
import io
from googleads import adwords

PAGE_SIZE = 100

def getConversion(start_date, end_date, client):
    
    output = io.StringIO()
    
    report_downloader = client.GetReportDownloader(version='v201809')

    report_query = (adwords.ReportQueryBuilder()
                   .Select('Date', 'CampaignName', 'ConversionTypeName', 'Conversions')
                   .From('CAMPAIGN_PERFORMANCE_REPORT')
                   .Where('CampaignStatus').In('ENABLED','PAUSED','REMOVED')
                   .During(start_date + ',' + end_date)
                   .Build())

    report_downloader.DownloadReportWithAwql(report_query, 'CSV', output, skip_report_header=True,
              skip_column_header=False, skip_report_summary=True,
              include_zero_impressions=False)

    output.seek(0)
    
    types= { 'Conversions': np.float64 }

    df_conversion = pd.read_csv(output, low_memory=False, dtype= types, keep_default_na=False)
    
    df_conversion['Day'] = df_conversion['Day'].apply(lambda s: datetime.strptime(s, '%Y-%m-%d').date())
 
    print(df_conversion)
    
    return df_conversion