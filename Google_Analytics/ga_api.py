import googleanalytics as ga
import datetime
import os
import json

def readData(days=3):
    # get connected to Google Analytics
    if os.path.exists('./service_account.json'):
        credentials = json.load(open('service_account.json'))
    else:
        print("file not exist")
        # (this will be interactive, as you'll need to confirm in a browser window)
        credentials = ga.authorize()
        # turn the credentials object into a plain dictionary
        credentials = credentials.serialize()
        json.dump(credentials, open('service_account.json', 'w'))
    
    accounts = ga.authenticate(**credentials)
    
    # list of accounts, properties and views
    print("accounts size: " + str(len(accounts)))
    for idx,account in enumerate(accounts):
        print(idx, account.name)
        
    web_properties = accounts[0].webproperties
    print ("properties size:" + str(len(web_properties)))
    for idx, web_property in enumerate(web_properties):
        print(idx, web_property.name)
        
    profiles = accounts[0].webproperties[0].profiles
    print("profiles size: " + str(len(profiles)))
    for idx, profile in enumerate(profiles):
        print(idx, profile.name)
      
    # choose profile    
    profile = profiles['ACT 1 All Traffic']
        
    # define the time range for daily data of the last 3 days
    today = datetime.datetime.date(datetime.datetime.now())
    dates = []
    for count in range(1,(days+1)):
        date = today - datetime.timedelta(count)
        dates.append(date)
        
    # Pull data for organic traffic
    # 1. unique visitors    
    organic_unique_visitors = []
    for date in dates:
        unique_visitors = profile.core.query.set(metrics=['ga:users'])\
                          .segment('organic traffic').range(date).value
        organic_unique_visitors.append(unique_visitors)
        
    res_organic_unique_visitors = "\n".join("{} {}".format(x, y) for x, y in zip(dates, organic_unique_visitors))
    print("Organic unique visitors: ", res_organic_unique_visitors)
    
    # 2. average time on site
    organic_avg_time_on_site = []
    for date in dates:
        avg_time_on_site = profile.core.query.metrics('avgSessionDuration').segment('organic traffic')\
                           .range(date).value
        organic_avg_time_on_site.append(avg_time_on_site)
    
    res_organic_avg_time = "\n".join("{} {}".format(x, y) for x, y in zip(dates, organic_avg_time_on_site))
    print("Organic avg time on site: ", res_organic_avg_time)
    
    # 3. average pages viewed by each organic unique visitors
    organic_pages_viewed = []
    for date in dates:
        pages_viewed = profile.core.query.metrics('pageviews').segment('organic traffic')\
                      .range(date).value
        organic_pages_viewed.append(pages_viewed)
    
    organic_avg_pages_viewed = [x / y for x,y in zip(organic_pages_viewed, organic_unique_visitors)]
    res_organic_avg_pages_viewed = "\n".join("{} {}".format(x, y) for x, y in zip(dates, organic_avg_pages_viewed))
    print("Organic avg pages viewed: ", res_organic_avg_pages_viewed)
    
    # 4. return visitors
    organic_return_visitors = []
    for date in dates:
        return_visitors = profile.core.query.set(metrics=['ga:users']).set(dimensions=['ga:channelGrouping'])\
                          .segment('returning users').range(date).get()                  
        return_dict = {}
        for row in return_visitors.rows:
            key = row[0]
            value = row[1]
            return_dict[key] = value
        organic_return_visitors.append(return_dict['Organic Search'])
            
    res_organic_return_visitors = "\n".join("{} {}".format(x, y) for x, y in zip(dates, organic_return_visitors))
    print("Organic return visitors: ", res_organic_return_visitors)
    
    # Pull data for paid traffic (for the rest two metrics: unique vistiors, avg time on site)
    # 1. unique visitors    
    paid_unique_visitors = []
    for date in dates:
        unique_visitors = profile.core.query.set(metrics=['ga:users'])\
                          .segment('paid traffic').range(date).value
        paid_unique_visitors.append(unique_visitors)
        
    res_paid_unique_visitors = "\n".join("{} {}".format(x, y) for x, y in zip(dates, paid_unique_visitors))
    print("Paid unique visitors: ", res_paid_unique_visitors)
    
    # 2. average time on site    
    paid_avg_time_on_site = []
    for date in dates:
        avg_time_on_site = profile.core.query.metrics('avgSessionDuration').segment('paid traffic')\
                           .range(date).value
        paid_avg_time_on_site.append(avg_time_on_site)
    
    res_paid_avg_time = "\n".join("{} {}".format(x, y) for x, y in zip(dates, paid_avg_time_on_site))
    print("Paid avg time on site: ", res_paid_avg_time)
    
    # 3. return visitors
    paid_return_visitors = []
    for date in dates:
        unique_visitors = profile.core.query.set(metrics=['ga:users'])\
                          .segment('paid traffic').range(date).value
        new_visitors = profile.core.query.set(metrics=['ga:newUsers'])\
                       .segment('paid traffic').range(date).value
        return_visitors = unique_visitors - new_visitors
        paid_return_visitors.append(return_visitors)
    
    res_paid_return_visitors = "\n".join("{} {}".format(x, y) for x, y in zip(dates, paid_return_visitors))
    print("Paid return visitors: ", res_paid_return_visitors)
    
    # get output for writing into DWH
    final_res = []
    for i in range(len(dates)):
        tuple_organic = (dates[i], "organic", organic_unique_visitors[i], organic_avg_time_on_site[i], organic_avg_pages_viewed[i], \
                         organic_return_visitors[i])
        tuple_paid = (dates[i], "paid", paid_unique_visitors[i], paid_avg_time_on_site[i], None, \
                         paid_return_visitors[i])
            
        final_res.append(tuple_organic)
        final_res.append(tuple_paid)
    
    print(final_res)
    
    return final_res
