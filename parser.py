import csv
import urllib.request
import sys
import datetime

host = "admin.fotonx.ru"
path = "billing/paysys/osmp.cgi"
url_base = "http://{host}/{path}".format(host=host,path=path)

check = "command=check&account={account}&txn_id={txn_id}&sum={sum}"
pay = "command=pay&account={account}&txn_id={txn_id}&sum={sum}&txn_date={txn_date:%Y%m%d%H%M%S}"

#txn_date=20090815120133

filename = sys.argv[1]

print('Loading %s' % filename)

def push(to,row):
    q = to.format(**row)
    print(q)
    #urllib.request.urlopen()


def parse(row):


    row['txn_date'] = datetime.datetime.strptime( "%s %s" % (row['date'], row['time']), '%d-%m-%y %H-%M-%S')

    print(row['txn_date'], row['account'])

    if push(check,row):
        push(pay,row)


fieldnames = [
    'date',
    'time',
    'no_ot',
    'no_kas',
    'txn_id',
    'account',
    'fio',
    'address',
    'sum',
    'sum2',
    'commission'
]

import codecs

with codecs.open(filename,encoding='cp1251') as csvfile:
    reader = csv.DictReader(csvfile,fieldnames=fieldnames,delimiter=';')
    for row in reader:
        if "=" in row['date']:
            pass
        parse(row)
