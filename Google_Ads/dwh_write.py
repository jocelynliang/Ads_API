import pyodbc as pdb

def writeData(data):
    # get connected
    conn = pdb.connect("DRIVER={Ingres CS};SERVER=@av-5MN7wYA8K.avprod.actiandatacloud.com,27832;DATABASE=db;UID=dbuser;PWD=dwhD454n1")
    cursor = conn.cursor()
    
    #cursor.execute("set autocommit off")

    # write data
    create_table = "create table if not exists digital_ads_google(\
    date date not null,\
    campaign_name   varchar(200) not null,\
    campaign_status varchar(50)  not null,\
    network   varchar(20) not null,\
    impressions float not null,\
    clicks float not null,\
    cost float not null,\
    ctr float not null,\
    avg_cpc float not null,\
    conversion_type varchar(50) null,\
    conversions float null)\
    with nopartition;"
    cursor.execute(create_table)
    
    insert_value = "insert into digital_ads_google(\
                    date, campaign_name, campaign_status, network, impressions, clicks, cost, ctr, \
                    avg_cpc, conversion_type, conversions) \
                    values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    cursor.executemany(insert_value, data)

    # end cursor
    conn.commit()
    conn.close()
    
    
    
    
    
    
    
    
    
    
    

