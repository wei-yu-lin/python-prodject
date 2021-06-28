def password_list(databasename):
    db_list =   [
                    ['PCM','yupcm00','pcm011376a'],
                    ['CPS','yucps00','cps111076a'],
                    ['CR2','yucps00','cps111076a'],
                    ['WIP','yuwip00','wip011376a'],
                    ['TQC','yutqc00','tqc062476a'],
                    ['MIC','yumic00','mic062476a'],
                    ['MPS','yumps00','mps062476a'],
                    ['HPS','yuhps00','hps072076a'],
                    ['SHP','yushp90','shp2000'],
                    ['ORD','yuord90','ord2000']
                ]
    result_A = []
    for i1, inner_l in enumerate(db_list):
        for i2, item in enumerate(inner_l):
            if (db_list[i1][0] == databasename): 
                result_A = db_list[i1]
                break
    return result_A    

def RDBConn(databasename):

    dsn_array = password_list(databasename)
    dsn = 'RDB' + databasename.upper() + "76"
    account = dsn_array[1]
    pwd = dsn_array[2]
    dsn_str = 'DSN=' + dsn + ';' + 'USERNAME=' + account +  ';' + 'PWD=' + pwd + ';'
    print(dsn_str)
    return dsn_str

if __name__ == "__main__":
    print ('This is main of module "DB_RDB.py"')