#coding:utf-8


#База данных
USER='root'
PASSWORD='pass'
DB='fotom'

#ИНН
INN="I"
#Расчетный счёт
RS="R"
#Номер реестра
X="001"

import pymysql.cursors
import csv
import datetime
import math

#Поле, по которому бъется платежка
DOG_FIELD = "number"
BALANCE_FIELD = "(amount - balance)"
td = datetime.date.today()
D=td.strftime("%m%d")

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user=USER,
                             password=PASSWORD,
                             db=DB,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.SSDictCursor)


def process(writer,row):
    print(row)
    row['address'] = row['address'].replace(',,',',').replace(',,',',').strip().strip(',')
    if row[DOG_FIELD]:
        row[DOG_FIELD] = row[DOG_FIELD].strip()
        if row.get(BALANCE_FIELD) and row[BALANCE_FIELD] > 0:
            row[BALANCE_FIELD] = "%.2f" % math.ceil(row[BALANCE_FIELD] or 0)
        else:
            row[BALANCE_FIELD]= "0.00"
        writer.writerow(row)
    else:
        print('bad number')



with connection.cursor() as cursor:
    sql = ( "SELECT {}, name, address, {} FROM accounts"
        " JOIN agreements ON agreements.uid = accounts.uid"
        " JOIN accounts_addr ON  accounts_addr.uid = accounts.uid"
        " join vgroups on agreements.agrm_id =  vgroups.agrm_id"
        " WHERE accounts.type = 2 and agreements.archive = 0 and accounts_addr.`type` = 0"
        ).format(DOG_FIELD,BALANCE_FIELD)
    #print(sql)
    cursor.execute(sql)
    name = '_'.join([INN,RS,X,D])+'.txt'
    print(name)
    with open(name, 'w', encoding="cp1251") as csvfile:
      writer = csv.DictWriter(csvfile,fieldnames=[DOG_FIELD,"name","address",BALANCE_FIELD], delimiter=';',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
      for row in cursor.fetchall_unbuffered():
          process(writer,row)
        

