def password_list(servername, databasename):   
    db_list =   [   
                    ['NTSR12','ED','100.1.1.25', 'sqluser', 'sqluser'],
                    ['NTSR12','PER','100.1.1.25', 'sqluser', 'sqluser'],
                    ['NTSR12','D212','100.1.1.25', 'yud212', 'yud212']
                ]
    result_A = []
    for i1, inner_l in enumerate(db_list):
        for i2, item in enumerate(inner_l):
            if (db_list[i1][0] == servername and db_list[i1][1] == databasename): 
                result_A = db_list[i1]
#                print(i1, i2, item, db_list[i1][i2])
    return result_A

def SQLConn(servername, databasename):

    dsn_array = password_list(servername, databasename)

    server = dsn_array[2] 
    database = databasename
    username = dsn_array[3]
    password = dsn_array[4]
    dsn_str = 'DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password

    return dsn_str


if __name__ == "__main__":
    print ('This is main of module "DB_SQL.py"')