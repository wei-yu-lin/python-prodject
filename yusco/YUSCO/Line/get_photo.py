import pyodbc 
import sys, os,io
from PIL import Image
from YUSCO.Core import DB_SQL

def cr_photo(photo_id):
    root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images") + "/"
    print(root_path)
    dsn_str = DB_SQL.SQLConn('NTSR12','ED')
    conn = pyodbc.connect(dsn_str)
    cursor = conn.cursor()

    #cursor.execute("SELECT @@version;") 
    s_sql = "select seqno, photo from qa_photo where photo_id = '" + photo_id + "' "
    cursor.execute(s_sql)
    row = cursor.fetchone() 
    i = 0
    while row: 
        i = i + 1
        image = Image.open(io.BytesIO(row[1]))
        image.save(root_path + photo_id + str(i) + '.png') 
        row = cursor.fetchone()

    cursor.close()
    conn.close()

    return i


def get_CombinePhoto(photo_id):

    root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images") + "/"
    photos = cr_photo(photo_id)
    result = False
    if photos > 0:
        pic_list = []
        for x in range(1,photos+1):
            pic_list.append(root_path + photo_id + str(x) + '.png')
        print(pic_list)

        images = map(Image.open, pic_list)
        widths, heights = zip(*(i.size for i in images))
        total_width = sum(widths)
        max_height = max(heights)

        new_im = Image.new('RGB', (total_width, max_height))
        x_offset = 0
        for im in pic_list:
            path = os.path.expanduser(im)
            img = Image.open(path)
            new_im.paste(img, (x_offset,0))
            x_offset += img.size[0]

        new_im.save(root_path + photo_id + '.png')
        result = True

    return result


def cr_pass(coil_no,station,schd_no,data_date):
    result = []
    try:
        dsn_str = DB_SQL.SQLConn('NTSR12','PER')
        conn = pyodbc.connect(dsn_str)
        cursor = conn.cursor()

        s_sql = (
                " select "  
                " coil_no, qc_remark, qc_sp_remark "
                " from cqca200m where "
                " coil_no ='" + coil_no + "' and station ='" + station + "' and schd_no ='" + schd_no + "' and data_date = '" + data_date + "'" 
        )
        cursor.execute(s_sql)
        result = list(cursor)
        cursor.close()
        conn.close()

    except Exception as e:
        print('Error: something worng, except message : ' + str(e))

    return result

