def OperCode_dic(oper_code):
    code_dic = {
        '10':'HSM',
        '14':'BAF',
        '15':'CRL',
        '21':'CPL',
        '31':'GPL1',
        '32':'GPL2',
        '41':'ZM1',
        '42':'ZM2',
        '43':'ZM3',
        '44':'ZM4',
        '45':'CR5(CR)',
        '46':'CR6',
        '49':'CR5(HR)',
        '51':'HAP',
        '52':'CAP',
        '53':'BAL',
        '54':'AP3(HR)',
        '55':'AP3(CR)',
        '56':'AP4',
        '61':'SPM1',
        '62':'SPM2',
        '63':'STL',
        '71':'TLL',
        '72':'CTL',
        '81':'OEM'
    }
    result_A = code_dic.get(oper_code,'')
    return result_A    

def OperCodePhoto_dic(oper_code):
    code_dic = {
#        '10':'HSM',
#        '14':'BAF',
#        '15':'CRL',
        '21':'CPL',
        '31':'GPL',
        '32':'GP2',
        '41':'CRM',
        '42':'ZM2',
        '43':'ZM3',
        '44':'CR4',
        '45':'CR5',
        '46':'CR6',
        '49':'CR5',
        '51':'HAP',
        '52':'CAP',
        '53':'BAL',
        '54':'AP3',
        '55':'AP3',
        '56':'AP4',
        '61':'SPM',
        '62':'SP2',
        '63':'STL',
        '71':'TLL',
        '72':'CTL',
        '81':'OEM'
    }
    result_A = code_dic.get(oper_code,'')
    return result_A    

if __name__ == "__main__":
    print ('This is main of module "Comm_code.py"')

def qc_ck_yn(prod_line):
    code_dic = {
        'HAP':'Y',
        'CAP':'Y',
        'CPL':'Y',
        'SPM':'Y',
        'GPL':'N',
        'TLL':'Y',
        'CRM':'N',
        'ZM2':'N',
        'ZM3':'N',
        'CR4':'N',
        'CR5':'N',
        'CR6':'N',
        'BAL':'Y',
        'CTL':'Y',
        'AP3':'Y',
        'AP4':'Y',
        'GP2':'N',
        'STL':'Y',
        'OEM':'N'
    }
    result_A = code_dic.get(prod_line,'')
    return result_A 