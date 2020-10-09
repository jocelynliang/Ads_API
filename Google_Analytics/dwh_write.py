import pyodbc as pdb

def writeData(data):
    # get connected
    conn = pdb.connect("DRIVER={Ingres CS};SERVER=@av-5MN7wYA8K.avprod.actiandatacloud.com,27832;DATABASE=db;UID=dbuser;PWD=dwhD454n1")
    cursor = conn.cursor()
    
    #cursor.execute("set autocommit off")
    
    create_table = "create table if not exists ga_web_traffic(\
    createddate date not null,\
    user_type   varchar(20) not null,\
    unique_visitors int not null,\
    avg_time_on_site float not null,\
    avg_pages_viewed float null,\
    return_visitors int not null)\
    with nopartition;"
    cursor.execute(create_table)
    
    insert_value = "insert into ga_web_traffic(\
                    createddate, user_type, unique_visitors, avg_time_on_site,avg_pages_viewed, return_visitors) \
                    values(?, ?, ?, ?, ?, ?)"
    cursor.executemany(insert_value, data)

    conn.commit()
    conn.close()
    




    
