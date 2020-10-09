import pandas as pd

pd.set_option("display.max_columns", 100)

# Define funtions to process the list of actions
def getLeads(list_actions):
    if type(list_actions) == list:
        for i in range(len(list_actions)):
            if list_actions[i]['action_type'] == "onsite_conversion.lead_grouped":
                lead = list_actions[i]['value']
                return lead
        
def getLeadsType(list_actions):
    if type(list_actions) == list:
        for i in range(len(list_actions)):
            if list_actions[i]['action_type'] == "onsite_conversion.lead_grouped":
                lead_type = "On-Facebook Lead"
                return lead_type

def processData(facebook_cursor, status):
    # Convert to data frame
    df = pd.DataFrame.from_dict(data = facebook_cursor, orient = 'columns')
      
    # Process data frame
    if df.empty:
        return df
 
    if 'actions' in df.columns:
        lead = df.actions.apply(lambda s: getLeads(s))
        lead_type = df.actions.apply(lambda s: getLeadsType(s))
        df['lead'] = lead
        df['lead_type'] = lead_type
        df.drop(columns=['actions'], inplace=True)
    
    if ('date_start' in df.columns) and ('date_stop' in df.columns):
        df.drop(columns=['date_start'], inplace=True)
        df.rename(columns={"date_stop":"date"}, inplace=True)
    
    df['status'] = status
    df['network'] = 'social'  
    
    columns = ['date','campaign_name', 'status', 'network','impressions','clicks','spend','ctr','cpc','lead_type','lead']
    df = df.reindex(columns=columns)
    
    return df


            
    




    