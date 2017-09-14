#coding:utf-8


#База данных
USER='root'
PASSWORD='iddqd'
DB='foton'

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
DOG_FIELD = "agrm_id"

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
    row['address'] = row['address'].replace(',,',',').replace(',,',',').strip()
    row['balance'] = math.ceil(row['balance'] or 0)
    writer.writerow(row)



with connection.cursor() as cursor:
    sql = ( "SELECT {}, name, address, balance FROM accounts"
        " JOIN agreements ON agreements.uid = accounts.uid"
        " LEFT JOIN accounts_addr ON  accounts_addr.uid = accounts.uid"
        " WHERE accounts.type = 2"
        ).format(DOG_FIELD)
    print(sql)
    cursor.execute(sql)
    name = '_'.join([INN,RS,X,D])+'.txt'
    print(name)
    with open(name, 'w', encoding="cp1251") as csvfile:
      writer = csv.DictWriter(csvfile,fieldnames=[DOG_FIELD,"name","address","balance"], delimiter=';',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
      for row in cursor.fetchall_unbuffered():
          process(writer,row)
        

