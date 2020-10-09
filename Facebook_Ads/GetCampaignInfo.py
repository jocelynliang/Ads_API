import os
import json
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi    


def getCampaignInfo(date):
    
    # Get connected with Facebook
    if os.path.exists('./facebook_credential.json'):
        credentials = json.load(open('facebook_credential.json'))
    else:
        print("Credential file not exist. Please check.")
    
    access_token = credentials['access_token']
    ad_account_id = credentials['ad_account_id']
    app_secret = credentials['app_secret']
    app_id = credentials['app_id']
    
    FacebookAdsApi.init(access_token = access_token)
    
    # Set columns 
    fields = ['campaign_name', 'impressions', 'clicks', 'spend', 'cpc', 'ctr', 'actions', #onsite_conversion.lead_grouped = leads on Facebook
              'action_values']

    # Set filter for both active and inactive campaigns
    active_filter = {'field':'campaign.delivery_info','operator':'IN','value':['active']}
    inactive_filter = {'field':'campaign.delivery_info','operator':'NOT_IN','value':['active']}
    
    # Set parameters
    active_params = {
        'time_range': {'since':date,'until':date},
        'filtering': [active_filter],
        'level': 'campaign',
        'breakdowns': []
    }

    inactive_params = {
        'time_range': {'since':date,'until':date},
        'filtering': [inactive_filter],
        'level': 'campaign',
        'breakdowns': [],
    }

    res_active = AdAccount(ad_account_id).get_insights(fields = fields, params = active_params)
    
    res_inactive = AdAccount(ad_account_id).get_insights(fields = fields, params = inactive_params)

    return res_active, res_inactive
    



