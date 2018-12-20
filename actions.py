########################################
#Description : This fie is part of ayman_database_application  - this file used by another file called app.py in this project
#Created : 10/12/2018
#Last Update : 20/12/2018
#Author : khaledfathi@protonmail.com
#PGP Fingerprint : FC8C B81A 70AE 4998 EB62  6F1A 202C 2C62 E64C 0367 
########################################

#lib needed
import mysql.connector
from os import system

#################General###############
def get_numbers(string_form):
    "function read numbers in string with ',' and return it at integer list - somthing like this input >> '12,3,6,5' output >> [12,3,6,5]"
    res=[]
    txt=""
    for i in string_form :
        if i != ',':
            txt+=i
        else:
            res.append(int(txt))
            txt=""
    return res

######################################
############## CLASSES ###############
######################################

class database_actions :
    "handle database  (connection - insert - delete - update - query .. etc)"
    def __init__(self,config_file):
        "class Initilzation"
        #this must be change in real server
        self.config_file=config_file

    def config(self):
        f=open(self.config_file,'r') 
        lines=f.readlines()
        res=[]
        for i in lines :
            for n in i :
                if n != '#':
                    res.append(i.strip())
                break
        return res

    def connection (self):
        "connect to mysql server"
        return mysql.connector.connect (
        host = self.config()[0], 
        port = int(self.config()[1]),
        user = self.config()[2],
        password = self.config()[3],
        database = self.config()[4])

    def query (self,SQL_statment):
        'SQL query for only search (return rows)'
        db=self.connection()
        cur=db.cursor()
        cur.execute(SQL_statment)
        row = cur.fetchall()
        cur.nextset()
        cur.close()
        db.close()
        return row

    def sql(self,SQL_statment):
        'SQL for everything except search like (insert , update , delete ..etc)'
        db=self.connection()
        cur=db.cursor()
        cur.execute(SQL_statment)
        db.commit()
        cur.close()
        db.close()

#inser database config file into database class 
database=database_actions('db_config.txt')

###################################
######## for insert new data ######
###################################

#names of html elements - used to point data in html form 
data_entry_form_names = ["name","address","phone","cities","other_city","product_type","product_link","pic_file","pic_url","request_date","end_date","email","souq_password","request_status","notes"]

#save data inro database
def insert_in_db(data_list):
    'get data HTML from (data_entry_form) and insert data into database'
    if data_list["cities"]=="--اخرى--":
        data_list["cities"]=data_list["other_city"]
    try :

        db=database
        db.sql("INSERT INTO orders (name,address,phone,cities,product_type,product_link,pic_file,pic_url,request_date,end_date,email,souq_password,request_status,notes) VALUES\
            ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format\
        (data_list["name"],\
        data_list["address"],\
        data_list["phone"],\
        data_list["cities"],\
        data_list["product_type"],\
        data_list["product_link"],\
        data_list["pic_file"],\
        data_list["pic_url"] ,\
        data_list["request_date"],\
        data_list["end_date"],\
        data_list["email"],\
        data_list["souq_password"],\
        data_list["request_status"],\
        data_list["notes"]))
        return True
    except Exception as error :
        print("Programming Error : " , error)
        return False

def return_id (data_list):
    "return query for last id in database plus 1 "
    db=database
    return db.query("SELECT id FROM orders WHERE \
    name = '{}' and\
    address = '{}' and \
    phone = '{}' and \
    cities = '{}' and \
    product_type = '{}' and \
    product_link = '{}' and\
    pic_file = '{}' and \
    pic_url = '{}' and \
    request_date = '{}' and \
    end_date = '{}' and \
    email = '{}' and \
    souq_password= '{}' and \
    request_status = '{}'and \
    notes = '{}'".format\
    (data_list["name"],\
    data_list["address"],\
    data_list["phone"],\
    data_list["cities"],\
    data_list["product_type"],\
    data_list["product_link"],\
    data_list["pic_file"],\
    data_list["pic_url"],\
    data_list["request_date"],\
    data_list["end_date"],\
    data_list["email"],\
    data_list["souq_password"],\
    data_list["request_status"],\
    data_list["notes"]))[0][0]

def new_id():
    "return next id in database , it will shown in HTML data_entry_form in new empty form"
    try :
        db=database
        return db.query("SELECT max(id) FROM orders")[0][0]+1
    except:
        return 1

#################################################
############### for query page ##################
#################################################

#names of all inputs field in query page
query_form_names=[
        "by_name",
        "pattern_1",
        "pattern_2",
        "pattern_3",
        "order_by",
        "az_za",
        "search",
        "search_from",
        "search_to",
        "pattern_selected"
        ]
#translate value in html to column names in database
translate={
        "ID":"id",
        "الاسم":"name",
        "العنوان":"address",
        "التليفون":"phone",
        "المحافظة":"cities",
        "نوع المنتج":"product_type",
        "تاريخ الطلب":"request_date",
        "تاريخ التسليم":"end_date",
        "البريد الالكترونى":"email",
        "الملاحظات":"notes",
        }

def send_to_query(data_dic):
    "it go to databas and do all query depend on input cases"
    
    #if input have two values
    if data_dic["search_from"] and data_dic["search_to"]:
        #pattern_1 (used for numbers only)
        if data_dic["pattern_selected"]=="pattern_1":
            try :
                search_from = int(data_dic["search_from"])
                search_to = int(data_dic["search_to"])
                # type 6 (between) in pattern 1
                if data_dic["pattern_1"]=="ما بين":
                    search_by = translate[data_dic["by_name"]]
                    order = translate[data_dic["order_by"]]
                    if data_dic["az_za"] =="تصاعدى":
                        a_z = "ASC"
                    elif data_dic["az_za"]== "تنازلى":
                        a_z ="DESC"
                    return database.query("SELECT * FROM orders WHERE {} BETWEEN {} AND {}  ORDER BY {} {}".format (search_by,search_from,search_to,order,a_z))
            except Exception as error:
                print("Programming Error : " , error)
        
        # pattern_3 (used for dates only) 
        elif data_dic["pattern_selected"]=="pattern_3":
            try :
                search_from = data_dic["search_from"]
                search_to = data_dic["search_to"]
                # type 4 (between) in pattern 3
                if data_dic["pattern_3"]=="الفترة من/الى":
                    search_by = translate[data_dic["by_name"]]
                    order = translate[data_dic["order_by"]]
                    if data_dic["az_za"] =="تصاعدى":
                        a_z = "ASC"
                    elif data_dic["az_za"]== "تنازلى":
                       a_z ="DESC"
                    return database.query("SELECT * FROM orders WHERE {} BETWEEN '{}' AND '{}'  ORDER BY {} {}".format (search_by,search_from,search_to,order,a_z))
            except Exception as error:
                print("Programming Error : " , error)

    #if input has one value
    elif data_dic["search"]:
        
        #for showing everthing in the tabe -
        if data_dic["search"] == "*all*":
            search_by = translate[data_dic["by_name"]]
            order = translate[data_dic["order_by"]]
            if data_dic["az_za"] =="تصاعدى":
                a_z = "ASC"
            elif data_dic["az_za"]== "تنازلى":
                a_z ="DESC"
            return database.query("SELECT * FROM orders ORDER BY {} {}".format (order,a_z))       
        
        #pattern_1 (used for Numbers only)
        elif data_dic["pattern_selected"]=="pattern_1":
            try :
                search = int(data_dic["search"])
                # type 1 (equal) in pattern 1
                if data_dic["pattern_1"]=="يساوى":
                    search_by = translate[data_dic["by_name"]]
                    order = translate[data_dic["order_by"]]
                    if data_dic["az_za"] =="تصاعدى":
                        a_z = "ASC"
                    elif data_dic["az_za"]== "تنازلى":
                        a_z ="DESC"
                    return database.query("SELECT * FROM orders WHERE {} = {}  ORDER BY {} {}".format (search_by,search,order,a_z))
                
                # type 2 (greater than) in pattern 1
                elif data_dic["pattern_1"]=="اكبر من":
                    search_by = translate[data_dic["by_name"]]
                    order = translate[data_dic["order_by"]]
                    if data_dic["az_za"] =="تصاعدى":
                        a_z = "ASC"
                    elif data_dic["az_za"]== "تنازلى":
                        a_z ="DESC"
                    return database.query("SELECT * FROM orders WHERE {} > {}  ORDER BY {} {}".format (search_by,search,order,a_z))
                
                # type 3 (greater than or qual) in pattern 1
                elif data_dic["pattern_1"]=="اكبر من او يساوى":
                    search_by = translate[data_dic["by_name"]]
                    order = translate[data_dic["order_by"]]
                    if data_dic["az_za"] =="تصاعدى":
                        a_z = "ASC"
                    elif data_dic["az_za"]== "تنازلى":
                        a_z ="DESC"
                    return database.query("SELECT * FROM orders WHERE {} >= {}  ORDER BY {} {}".format (search_by,search,order,a_z))

                # type 4 (less than) in pattern 1
                elif data_dic["pattern_1"]=="اصغر من":
                    search_by = translate[data_dic["by_name"]]
                    order = translate[data_dic["order_by"]]
                    if data_dic["az_za"] =="تصاعدى":
                        a_z = "ASC"
                    elif data_dic["az_za"]== "تنازلى":
                        a_z ="DESC"
                    return database.query("SELECT * FROM orders WHERE {} < {}  ORDER BY {} {}".format (search_by,search,order,a_z))

                # type 5 (greater than or equal) in pattern 1
                elif data_dic["pattern_1"]=="اصغر من او يساوى":
                    search_by = translate[data_dic["by_name"]]
                    order = translate[data_dic["order_by"]]
                    if data_dic["az_za"] =="تصاعدى":
                        a_z = "ASC"
                    elif data_dic["az_za"]== "تنازلى":
                        a_z ="DESC"
                    return database.query("SELECT * FROM orders WHERE {} <= {}  ORDER BY {} {}".format (search_by,search,order,a_z))

            except Exception as error:
                print("Programming Error : " , error)

        #pattern_2 (used for any thing else (as text))
        elif data_dic["pattern_selected"]=="pattern_2":
            try :
                search = data_dic["search"]
                # type 1 (contain) in pattern 2
                if data_dic["pattern_2"]=="يحتوى على":
                    search_by = translate[data_dic["by_name"]]
                    order = translate[data_dic["order_by"]]
                    if data_dic["az_za"] =="تصاعدى":
                        a_z = "ASC"
                    elif data_dic["az_za"]== "تنازلى":
                        a_z ="DESC"
                    return database.query("SELECT * FROM orders WHERE {} LIKE '%{}%'  ORDER BY {} {}".format (search_by,search,order,a_z))

                # type 2 (start with) in pattern 2
                if data_dic["pattern_2"]=="يبدأ بـ":
                    search_by = translate[data_dic["by_name"]]
                    order = translate[data_dic["order_by"]]
                    if data_dic["az_za"] =="تصاعدى":
                        a_z = "ASC"
                    elif data_dic["az_za"]== "تنازلى":
                        a_z ="DESC"
                    return database.query("SELECT * FROM orders WHERE {} LIKE '{}%'  ORDER BY {} {}".format (search_by,search,order,a_z))

                # type 3 (end with) in pattern 2
                if data_dic["pattern_2"]=="ينتهى بـ":
                    search_by = translate[data_dic["by_name"]]
                    order = translate[data_dic["order_by"]]
                    if data_dic["az_za"] =="تصاعدى":
                        a_z = "ASC"
                    elif data_dic["az_za"]== "تنازلى":
                        a_z ="DESC"
                    return database.query("SELECT * FROM orders WHERE {} LIKE '%{}'  ORDER BY {} {}".format (search_by,search,order,a_z))

                # type 4 (identical) in pattern 2
                if data_dic["pattern_2"]=="متطابق":
                    search_by = translate[data_dic["by_name"]]
                    order = translate[data_dic["order_by"]]
                    if data_dic["az_za"] =="تصاعدى":
                        a_z = "ASC"
                    elif data_dic["az_za"]== "تنازلى":
                        a_z ="DESC"
                    return database.query("SELECT * FROM orders WHERE {} = '{}'  ORDER BY {} {}".format (search_by,search,order,a_z))

            except Exception as error :
                print ("Programming Error : ", error)
        
        #pattern_3 (used for Date only)
        elif data_dic["pattern_selected"]=="pattern_3":
            try :
                search = data_dic["search"]
               
               # type 1 (in this date) in pattern 3
                if data_dic["pattern_3"]=="فى يوم":
                    search_by = translate[data_dic["by_name"]]
                    order = translate[data_dic["order_by"]]
                    if data_dic["az_za"] =="تصاعدى":
                        a_z = "ASC"
                    elif data_dic["az_za"]== "تنازلى":
                        a_z ="DESC"
                    return database.query("SELECT * FROM orders WHERE {} = '{}'  ORDER BY {} {}".format (search_by,search,order,a_z))
                # type 2 (before date) in pattern 3
                elif data_dic["pattern_3"]=="ما قبل":
                    search_by = translate[data_dic["by_name"]]
                    order = translate[data_dic["order_by"]]
                    if data_dic["az_za"] =="تصاعدى":
                        a_z = "ASC"
                    elif data_dic["az_za"]== "تنازلى":
                        a_z ="DESC"
                    return database.query("SELECT * FROM orders WHERE {} < '{}'  ORDER BY {} {}".format (search_by,search,order,a_z))
                # type 3 (after date) in pattern 3
                elif data_dic["pattern_3"]=="ما بعد":
                    search_by = translate[data_dic["by_name"]]
                    order = translate[data_dic["order_by"]]
                    if data_dic["az_za"] =="تصاعدى":
                        a_z = "ASC"
                    elif data_dic["az_za"]== "تنازلى":
                        a_z ="DESC"
                    return database.query("SELECT * FROM orders WHERE {} > '{}'  ORDER BY {} {}".format (search_by,search,order,a_z))
            except Exception as error:
                print ("Programming Error : ", error)

#generate HTML code for query as html tabel
def query_to_tabel (query):
    "arrangement output query into tabel - this function will return HTML code"
    count=0
    res=""
    for i in query :
        res+="<tr>"
        for n in i :
            if count==6:
                res+="<td> <a href= '{}' target = 'blank'>اضغط هنا</a></td>".format(n)
            elif count==8:
                res+="<td> <img src ='{}' alt='No Image' width='150' height='150'></td>".format(n)
            else:
                res+="<td>"+str(n)+"</td>"
            count+=1
        count=0
        res+="""
        <td class='edit_res' name='edit' >
            <input type='submit'  value='تعديل' onclick="update_delete_status.value='UPDATE'; update_delete_id.value='{}' ">
        </td>""".format(i[0])
        res+="""
        <td class='edit_res' name='del'>
            <input type='submit' value='حذف' onclick=" update_delete_status.value='DELETE';update_delete_id.value='{}' ">
        </td>""".format(i[0])
        res+="""<td>
            <input type='checkbox' name='del_check' value='{}'>
        </td>""".format(i[0])
        res+="</tr>"
    return res
#################################################
############### for UPDATE Rows #################
#################################################

update_form_names = ["id","name","address","phone","cities","other_city","product_type","product_link","pic_file","pic_url","request_date","end_date","email","souq_password","request_status","notes"]
def update(data_list):
    try :
        return database.sql("UPDATE orders SET name='{}' , address='{}',phone='{}',cities='{}',product_type='{}',product_link='{}',pic_file='{}',pic_url='{}',request_date='{}',end_date='{}',email='{}',souq_password='{}',request_status='{}',notes='{}' WHERE  id={}".format\
            (data_list["name"],\
            data_list["address"],\
            data_list["phone"],\
            data_list["cities"],\
            data_list["product_type"],\
            data_list["product_link"],\
            data_list["pic_file"],\
            data_list["pic_url"] ,\
            data_list["request_date"],\
            data_list["end_date"],\
            data_list["email"],\
            data_list["souq_password"],\
            data_list["request_status"],\
            data_list["notes"],\
            data_list["id"]))
    except Exception as e:
        print (e)

#################################################
############### for HELP page ###################
#################################################
#names of html elements - used to point data in html form 
help_form_names = ["import_file","host","port","user","password","database","action_type"]

#backup database > sql file
def db_backup():
    'backup database and save it in *.sql file'
    return system("mysqldump -u root -pcommand ayman > back_up.sql")

#backup database > html file
def html_export():
    'export all records in database in one html page as a table'
    data= database.query("SELECT * FROM orders ORDER BY id")
    query_all=""
    for i in data :
        query_all+="<tr>\n"
        for n in i :
            if not n:
                query_all+="<td>"+"EMPTY"+"</td>\n"
            else:
                query_all+="<td>"+ str(n)+"</td>\n"
        query_all+="</tr>\n"

    html="""
    <html dir="rtl">
        <head>
            <meta charset="utf-8">
            <title>Ayman-DATABASE-backup</title>
            <style>
            table{1}
            td{2}
            </style>
        </head>
        <body style="padding:20px">
        <h1>قاعدة بيانات Best Offer 2019</h1>
        <table>
            <tr>
                <td>ID</td>
                <td>الاسم</td>
                <td>العنوان</td>
                <td>التليفون</td>
                <td>المحافظة</td>
                <td>نوع المنتج</td>
                <td>رابط المنتج</td>
                <td>صورة</td>
                <td>رابط صورة</td>
                <td>تاريخ الطلب</td>
                <td>تاريخ التسليم</td>
                <td>البريد الالكترونى</td>
                <td>كلمة السر - سوق</td>
                <td>حالة الطلب</td>
                <td>ملاحظات</td>
            </tr>
            {0}
        </table>
        <body>
    </html>
    """
    res=html.format(query_all,"{border:1px solid black;border-collapse:collapse}","{border:1px solid black;}")
    f = open("export_html.html","w")
    f.write(res)
    f.close()

#check file extenstion (True or False)
def extenstion_allowed(filename,allowed_extenstions):
    'check extenstion of file if it in allowed extensions'
    return "." in filename and filename.rsplit(".",1)[1] in allowed_extenstions

#restore_database
def restore_database(filename):
    'destory old database and restore it by sql file'
    system("mysql -u root -pcommand ayman < "+filename)
    return True

#destroy data base
def destroy_database():
    "delete orders table"
    return database.sql("DROP TABLE IF EXISTS orders")

