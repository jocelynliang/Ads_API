import pyodbc as pdb

def writeData(data):
    # Get connected
    conn = pdb.connect("DRIVER={Ingres CS};SERVER=@av-5MN7wYA8K.avprod.actiandatacloud.com,27832;DATABASE=db;UID=dbuser;PWD=dwhD454n1")
    cursor = conn.cursor()
    
    #cursor.execute("set autocommit off")
    
    # Write data
    create_table = "create table if not exists digital_ads_facebook(\
    date date not null,\
    campaign_name   varchar(250) not null,\
    status varchar(50)  not null,\
    network   varchar(50) not null,\
    impressions float not null,\
    clicks float not null,\
    spend float not null,\
    ctr float not null,\
    cpc float null,\
    lead_type varchar(50) null,\
    lead float null)\
    with nopartition;"
    cursor.execute(create_table)
    
    insert_value = "insert into digital_ads_facebook(\
                    date, campaign_name, status, network, impressions, clicks, spend, ctr, \
                    cpc, lead_type, lead) \
                    values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    cursor.executemany(insert_value, data)

    # End cursor
    conn.commit()
    conn.close()
  


