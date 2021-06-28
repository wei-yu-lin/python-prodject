def OracleDB_dic(db_name):
    code_dic = {
        'RP547A_TQC':'tqc/tqc@rp547a'
    }
    result_A = code_dic.get(db_name,'')
    return result_A    

if __name__ == "__main__":
    print ('This is main of module "DB_ORACLE.py"')

def OracleDB_dic2(db_name):
    code_dic = {
        'RP547B_ECUSER':'ecuser/ecuser@rp547b'
    }
    result_A = code_dic.get(db_name,'')
    return result_A    

if __name__ == "__main__":
    print ('This is main of module "DB_ORACLE.py"')